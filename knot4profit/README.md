# Knot-4-Profit website

This is a self-contained static website for Knot-4-Profit Collaborations. The intended temporary hosting location is `https://fwiwletter.com/knot4profit/`. A branch or local preview is not a production deployment.

All deployable files live in this directory. The existing FWIW site, its domain configuration, and its other applications have no dependency on this website. There is no service worker, payment backend, contact-form backend, or runtime framework.

## Build and review

Requirements: Python 3.10 or later. Node.js is needed only for the event-state checks.

From the repository root:

```sh
python3 knot4profit/tools/build.py
python3 knot4profit/tools/check-site.py
node knot4profit/tools/test-event-state.cjs
```

The build script generates the HTML pages from `content/site.json`, `content/events.json`, and the page templates in `tools/build.py`. **Commit the generated HTML together with its source changes.** The current GitHub Pages deployment does not run this Python script; it publishes the committed static files through the repository's existing Pages/Jekyll workflow.

For a normal local development environment, start a static server from the repository root:

```sh
python3 -m http.server 8000 --directory .
```

Open `http://localhost:8000/knot4profit/`. In managed development environments, use that environment's supported preview service instead of starting an additional server.

The checker verifies local links, anchors, assets, basic page metadata, both possible hosting mounts, and agreement between the generated HTML and its source. It does not verify third-party availability, run a browser, or establish accessibility conformance. Also review the actual pages at phone, tablet, and desktop widths, with keyboard navigation and JavaScript disabled. Verify outbound destinations without submitting inquiries or transactions.

## Update content

| Location | Purpose |
| --- | --- |
| `content/site.json` | Organization contact details, canonical site URL, and preview/indexing setting |
| `content/events.json` | Public event information, roles, dates, destinations, and source links |
| `tools/build.py` | Shared page layout and general website copy |
| `assets/site.css` | Responsive presentation and local font declarations |
| `assets/site.js` | Mobile menu, event filters, date-state display, and email copying |
| `assets/event-state.js` | Pure date/status and action-visibility rules |

Edit source files, regenerate, and review the resulting HTML. Changes made only to generated HTML will be replaced by the next build. These source files are a technical maintenance interface; they are not a completed nontechnical editor.

Only public-safe information belongs in this repository, including JSON and source comments. Do not commit private meeting transcripts, credentials, private source documents, unpublished plans, personal stories, or internal commercial arrangements.

### Add or update an event

1. Add or edit an entry in `content/events.json`. An existing entry shows the complete field structure.
2. Choose a unique lowercase `slug` with hyphens. Its URL is `events/<slug>/`. Keep an existing slug stable to preserve shared links.
3. Set the title, summary, description paragraphs, venue, address, beneficiary, and **Knot-4-Profit's exact role**. Organizer, facilitator, and sponsor are different roles; an individual's involvement does not establish an organizational role.
4. Set the calendar `date` as `YYYY-MM-DD`. For a scheduled event with known times, set `starts_at` and `ends_at` to complete ISO timestamps with explicit offsets, such as `2026-12-17T07:30:00-06:00`. Keep the human-readable `date_label` and `time_label` consistent. The `timezone` field records the event's named zone, normally `America/Chicago`; the explicit timestamp offsets must reflect daylight-saving time on the actual event date.
5. Link `official_url` and any action to the correct organization- or event-controlled destination. Preserve existing registration providers. Keep public `sources` and `verified_on` current. Do not invent prices, proceeds claims, or deadlines.
6. Use `featured: true` for exactly one event to populate the homepage feature. Update that selection when the highlighted event changes. The available visual themes are `blue`, `yellow`, and `peach`.
7. Regenerate and run the checks. Open the event directly, refresh it, and check the homepage and event listing.

### Archive, cancel, or remove an event

- Set `archived: true` to retain a past event and its original URL. Remove actions that are no longer relevant. Archived records may use `null` for exact start/end times if only the historical date is verified.
- Set `status: "cancelled"` when an event is canceled, and update the visible description with verified information. The status disables event actions. An omitted status means scheduled; unsupported states are shown neutrally until the content is resolved.
- Prefer archiving to deleting a previously shared event page. The build writes current pages but does not delete old directories automatically. If intentionally removing an event, remove its old generated directory as well and address any incoming links. The checker reports generated pages that no longer match the content model.

### Action visibility and deadlines

Each optional action has a label, HTTPS destination, kind, and `display_until` timestamp with an explicit offset. **`display_until` is this website's UI cutoff. It is not a claim about the organizer's official closing time.** Set it deliberately and verify the actual destination separately.

An event can remain upcoming while a nomination, ticket, or sponsorship action has closed. Actions disappear at their individual cutoff, when the event ends, or when it is archived/canceled. Invalid or timezone-free timestamps fail closed. Date-state labels refresh while the page remains open and when a visitor returns to the tab.

The generated HTML uses neutral event labels and keeps the official information link available without JavaScript. Time-sensitive action buttons are progressively enabled by JavaScript. No site interaction claims that an email was sent or a payment was completed.

## A future editing workflow

Terra's ability to add, edit, and archive events through a usable interface remains a separate handoff requirement. A form-based Git editor such as [Pages CMS](https://pagescms.org/docs/) is a candidate; it has not been installed or configured for this site.

A complete setup would require a suitable repository, the [Pages CMS GitHub App](https://pagescms.org/docs/quick-start/), a root `.pages.yml` content/media schema, appropriate access, and an agreed preview/publish process. Its [collaborator interface](https://pagescms.org/docs/configuration/collaborators/) supports email-invited editors without requiring them to learn Git. Its [Marketplace listing](https://github.com/marketplace/pages-cms) advertises a free plan as checked on November 24, 2026; verify current terms before adoption.

**Editing JSON through a UI is not sufficient by itself:** this site's generated HTML must also be rebuilt and published. Automatic regeneration is not configured in this repository. A dedicated client repository can add a small build workflow or use a compatible static host during the later handoff. Complete the editor handoff only after Terra can perform the agreed add, edit, and archive tasks, or the maintenance arrangement is explicitly revised. This first preview does not establish a subscription, permanent hosting cost, or training arrangement.

## Export and move to a standalone site

Local navigation and asset paths are document-relative, so the site can work under `/knot4profit/` or at a standalone `/`. Canonical and social-sharing URLs are absolute and must be regenerated for the destination.

For a separate preview export, from the repository root:

```sh
mkdir -p ../knot4profit-export
cp -R knot4profit/. ../knot4profit-export/
python3 knot4profit/tools/build.py --site-url https://preview.example.org/ --output ../knot4profit-export
python3 ../knot4profit-export/tools/check-site.py --site-url https://preview.example.org/
python3 -m http.server 8001 --directory ../knot4profit-export
```

Replace the example URL with the actual destination. The build's `--output` option writes HTML only; copying the directory first includes assets, content, and maintenance tools. Open `http://localhost:8001/`, including nested event pages, to inspect the standalone mount. The exported configuration still retains its original default URL until `content/site.json` is updated; use the same `--site-url` override for subsequent export builds or update that file for the new repository.

**Do not copy the parent FWIW repository's CNAME into the standalone site.** Leave the current FWIW domain and DNS settings intact. The later domain/hosting transition is a separate operation. A domain's registrar and the website's hosting provider can be different services.

Before an approved final launch:

- Set the final origin in `content/site.json`, regenerate canonical/social metadata, and verify the sharing image URL.
- Confirm navigation, fonts, imagery, downloads, nested-page refreshes, and any required redirects on the actual host.
- Remove preview `noindex` only when indexing is approved. Set `preview: false` in the final configuration, or use `--indexable` for an approved export and pass the same flag to the checker.
- Publish through the agreed branch/review process, verify the successful deployment, and read back the actual public pages.

This preview's `noindex` metadata is a search-engine instruction, not access control. Everything committed or published must remain appropriate for public access.

## Assets and credits

- `assets/brand-logo.png` is the unmodified 300 × 250 PNG identified as Knot-4-Profit Collaborations’ logo in the [Pony Express 5K sponsor listing](https://runsignup.com/Race/Sponsors/MO/SaintJoseph/PonyExpressRun5KandHalfMarathon), corroborated by the organization’s [Facebook profile](https://www.facebook.com/Knot4Profit/). [Original PNG](https://d368g9lw5ileu7.cloudfront.net/races/race45985-racesponsor-0.bPZ9ny.png). Retrieved November 24, 2026. The header background matches the image’s pale blue edges; the original image is not cropped, redrawn, recolored, or upscaled. A larger original can replace this modest-resolution source later.

- `assets/brand-banner.jpg` is an unmodified copy of the organization's published brand artwork, sourced from the [Knot-4-Profit Collaborations Zeffy profile](https://www.zeffy.com/en-US/organizations/knot-4-profit-collaborations).
- Barlow Condensed ExtraBold (800) and DM Sans Regular (400)/Bold (700) are served locally. The original font files came from Google Fonts; their SIL Open Font License files are retained as `assets/fonts/OFL-Barlow-Condensed.txt` and `assets/fonts/OFL-DM-Sans.txt`.
- Official license sources: [Barlow Condensed](https://github.com/google/fonts/blob/main/ofl/barlowcondensed/OFL.txt) and [DM Sans](https://github.com/google/fonts/blob/main/ofl/dmsans/OFL.txt).
- Public event-source links are retained with each record in `content/events.json`. Keep the organization's role and the benefiting cause distinct when updating copy.

## Contact navigation

Topic-specific contact links and footer email addresses navigate to the Get involved contact panel. A bounded `subject` query parameter preserves the topic for the explicitly labelled **Open email app** action. The panel also exposes the address as selectable text and a progressive copy button. No form submission or email backend is configured. Native contact navigation and the readable address remain usable without JavaScript.
