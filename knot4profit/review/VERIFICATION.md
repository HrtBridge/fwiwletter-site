# Website preview verification

Reviewed November 24, 2026 (America/Chicago).

## Scope

Eight generated pages, self-contained under `knot4profit/`: home, events, how we help, about, get involved, and three event-detail pages. No changes to the existing FWIW pages, domain configuration, deployment workflow, or other applications.

## Checks completed

- `python3 knot4profit/tools/check-site.py`: passed for all eight pages. Checks local links, anchors, assets, metadata, relative paths at both hosting mounts, and agreement with a fresh build.
- `node knot4profit/tools/test-event-state.cjs`: 11 test groups passed, including event/action boundaries, explicit time-zone offsets, impossible/missing dates, cancellation, and archive behavior.
- JavaScript syntax and Python compilation checks passed.
- Compared every existing tracked file with the original main revision: all 25 unchanged.
- Viewed the actual browser-rendered homepage at 1440, 768, and 390 CSS pixels. Reviewed the event page on desktop and phone; also checked its tablet and narrow-width geometry.
- Checked homepage and event-page overflow at 320 pixels, including 200% text: document width matched viewport width after the refinement pass.
- Tested mobile menu activation by keyboard, Escape dismissal, upcoming/past filters, and the copy-email success state. Reviewed email destinations without sending messages.
- Verified the no-JavaScript event fallback retains visible navigation and official event information while time-sensitive action buttons remain hidden.
- Loaded the site at `/knot4profit/`, then served a separate export at `/`. Navigated to the nested event page and refreshed it successfully with ticket links available.
- Smoke-loaded the existing FWIW homepage, archive, mortgage tool, and cold-call tool in the local preview.
- Reviewed site-console output; no errors from the Knot-4-Profit application files were observed. Browser-extension messages and the separate responsive-review harness are outside the application.
- Checked the main text/background color pairs mathematically: contrast ranged from 5.33:1 to 12.65:1. This is a focused check, not an accessibility certification.

## Screenshots

These are actual Chromium screenshots of the implemented pages. Responsive sizes were rendered in same-origin review frames with the stated CSS viewport widths; these are not physical-device tests. Screenshots omit the private review toolbar.

- [Homepage, 1440 px](home-desktop.jpg)
- [Homepage, 390 px](home-mobile.jpg)
- [Event, 1440 px](event-desktop.jpg)
- [Event, 390 px](event-mobile.jpg)

## Boundaries

- This is a branch/local preview, not a verified production deployment. Merge and publication remain subject to the agreed release approval.
- No automated Lighthouse score or full accessibility conformance claim is made. Field performance and production-host read-back remain future checks.
- Core content is static, with local fonts and small progressive-enhancement scripts. There is no service worker, runtime framework, analytics, payment processing, or contact-form submission service.
- The original published organization banner is included on About. The header uses a plain text name treatment; the palette and typesetting are design proposals for review. No documentary photography or unapproved board portraits are used.
- The event editor is not configured. The README explains the source format and the additional requirements for a usable visual-editor handoff.
- Preview pages retain `noindex, nofollow`. Final origin, social metadata, indexing, and domain migration must be set deliberately at an approved launch.
