#!/usr/bin/env python3
"""Check the static website's local routes, metadata, assets, and generated output."""
import argparse
from collections import Counter
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import subprocess
import sys
from tempfile import TemporaryDirectory
from urllib.parse import unquote, urljoin, urlsplit

ROOT = Path(__file__).resolve().parents[1]


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.path = path
        self.source = path.read_text(encoding="utf-8")
        self.ids = Counter()
        self.h1_count = 0
        self.in_title = False
        self.title = ""
        self.meta = {}
        self.canonicals = []
        self.references = []
        self.base_tags = 0
        self.feed(self.source)

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if attrs.get("id"):
            self.ids[attrs["id"]] += 1
        if tag == "h1":
            self.h1_count += 1
        if tag == "title":
            self.in_title = True
        if tag == "base":
            self.base_tags += 1
        if tag == "meta":
            key = attrs.get("name") or attrs.get("property")
            if key:
                self.meta.setdefault(key.lower(), []).append(attrs.get("content", ""))
        if tag == "link" and "canonical" in attrs.get("rel", "").split():
            self.canonicals.append(attrs.get("href", ""))
        elif tag in ("a", "link") and "href" in attrs:
            self.references.append((attrs["href"], tag == "a"))
        if tag in ("img", "script", "source", "video", "audio", "iframe") and "src" in attrs:
            self.references.append((attrs["src"], False))

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False

    def handle_data(self, data):
        if self.in_title:
            self.title += data


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--site-url", help="Canonical/social base used for an export")
    parser.add_argument("--indexable", action="store_true", help="Expect an approved indexable export")
    args = parser.parse_args()
    site = json.loads((ROOT / "content/site.json").read_text())
    events = json.loads((ROOT / "content/events.json").read_text())
    site_url = (args.site_url or site["site_url"]).rstrip("/") + "/"
    preview = site["preview"] and not args.indexable
    errors = []

    def fail(path, message):
        errors.append(f"{path.relative_to(ROOT)}: {message}")

    pages = {path: Page(path) for path in sorted(ROOT.rglob("*.html"))}
    expected = {"index.html", "events/index.html", "about/index.html",
                "how-we-help/index.html", "get-involved/index.html"}
    expected.update(f"events/{event['slug']}/index.html" for event in events)
    actual = {path.relative_to(ROOT).as_posix() for path in pages}
    if actual != expected:
        errors.append(f"Page set differs from content: missing={sorted(expected - actual)}, unexpected={sorted(actual - expected)}")

    def local_reference(source, value, is_navigation=False):
        if not value:
            fail(source, "empty link or asset path")
            return
        parsed = urlsplit(value)
        if parsed.scheme in ("mailto", "tel") and is_navigation:
            return
        if parsed.scheme in ("https", "http"):
            if not is_navigation:
                fail(source, f"runtime asset is not self-hosted: {value}")
            elif value.startswith(site_url):
                fail(source, f"local navigation must remain relative: {value}")
            return
        if parsed.scheme or parsed.netloc or value.startswith("/"):
            fail(source, f"nonportable or unsupported URL: {value}")
            return
        destination = (source.parent / unquote(parsed.path)).resolve() if parsed.path else source
        if not destination.is_relative_to(ROOT):
            fail(source, f"path escapes the site directory: {value}")
            return
        if destination.is_dir():
            destination /= "index.html"
        if not destination.is_file():
            fail(source, f"missing local target: {value}")
            return
        if parsed.fragment and destination in pages and unquote(parsed.fragment) not in pages[destination].ids:
            fail(source, f"missing anchor in {destination.relative_to(ROOT)}: #{parsed.fragment}")

        # Resolve as a browser would at each mount. Neither may escape the site
        # or select a different file merely because the host path changed.
        for mount in ("/", "/knot4profit/"):
            source_url = "https://preview.invalid" + mount + source.relative_to(ROOT).as_posix()
            resolved_path = unquote(urlsplit(urljoin(source_url, value)).path)
            if not resolved_path.startswith(mount):
                fail(source, f"URL escapes {mount} hosting mount: {value}")
                continue
            mounted = (ROOT / resolved_path[len(mount):]).resolve()
            if mounted.is_dir():
                mounted /= "index.html"
            if mounted != destination:
                fail(source, f"URL resolves differently at {mount}: {value}")

    titles = Counter(page.title.strip() for page in pages.values())
    for path, page in pages.items():
        if page.source.lstrip("\ufeff\r\n ").startswith("---"):
            fail(path, "generated HTML unexpectedly contains Jekyll front matter")
        if page.base_tags:
            fail(path, "a base element would change portable relative-path behavior")
        if page.h1_count != 1:
            fail(path, f"expected one h1, found {page.h1_count}")
        if not page.title.strip() or titles[page.title.strip()] != 1:
            fail(path, "page title is empty or duplicated")
        descriptions = page.meta.get("description", [])
        if len(descriptions) != 1 or not descriptions[0].strip():
            fail(path, "expected one nonempty description")
        robots = page.meta.get("robots", [])
        if len(robots) != 1:
            fail(path, "expected one robots declaration")
        elif preview != ("noindex" in [token.strip() for token in robots[0].lower().split(",")]):
            fail(path, "robots indexing state disagrees with the build configuration")
        route = path.relative_to(ROOT).as_posix().removesuffix("index.html")
        canonical = site_url + route
        if page.canonicals != [canonical] or page.meta.get("og:url") != [canonical]:
            fail(path, "canonical or social URL disagrees with the configured site URL")
        for image in page.meta.get("og:image", []):
            if not image.startswith(site_url) or not (ROOT / unquote(image[len(site_url):])).is_file():
                fail(path, "social-sharing image is missing or uses the wrong site origin/path")
        for identifier, count in page.ids.items():
            if count > 1:
                fail(path, f"duplicate id: {identifier}")
        for value, navigation in page.references:
            local_reference(path, value, navigation)

    assets = ROOT / "assets"
    for path in sorted(assets.rglob("*")):
        if not path.is_file():
            continue
        if any(part.startswith(("_", ".")) for part in path.relative_to(assets).parts):
            fail(path, "asset path may be omitted by the existing Jekyll publishing behavior")
        if path.suffix == ".css":
            for match in re.finditer(r"url\(\s*(['\"]?)(.*?)\1\s*\)", path.read_text(), re.IGNORECASE):
                local_reference(path, match.group(2))
        if path.suffix == ".js":
            source = path.read_text()
            if re.search(r"\.\s*serviceWorker\b", source) or path.name.lower() in {"sw.js", "service-worker.js", "serviceworker.js"}:
                fail(path, "service workers are outside this site's static hosting scope")

    with TemporaryDirectory(prefix="knot4profit-check-") as directory:
        output = Path(directory)
        command = [sys.executable, str(ROOT / "tools/build.py"), "--output", str(output)]
        if args.site_url:
            command.extend(["--site-url", args.site_url])
        if args.indexable:
            command.append("--indexable")
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode:
            errors.append("Build validation failed:\n" + result.stderr.strip())
        else:
            for generated in output.rglob("*.html"):
                committed = ROOT / generated.relative_to(output)
                if not committed.is_file() or committed.read_bytes() != generated.read_bytes():
                    errors.append(f"{committed.relative_to(ROOT)}: generated HTML is stale; rerun tools/build.py")

    if errors:
        print("Static site checks failed:")
        for error in errors:
            print("- " + error)
        return 1
    print(f"PASS: {len(pages)} pages; local links, anchors, assets, metadata, and both hosting mounts.")
    print("PASS: committed HTML matches the current generator and public content.")
    print("Browser layout, accessibility, and external destinations still require separate review.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
