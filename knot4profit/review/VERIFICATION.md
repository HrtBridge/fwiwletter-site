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

## Link audit and contact-flow update

Reviewed November 24, 2026 (America/Chicago), using the exact private-deployment files in the managed local browser preview.

- Clicked all 97 visible internal page links in the original package, including every header/footer placement and event-detail link. Each reached the expected route and page heading. The additional events empty-state link was hidden under the current event data; its target passed the static route check.
- Clicked all six distinct external destinations. Breakfast tickets, the sponsorship form, the official Voices of Courage event page, RunSignup, and the past Hurts Donuts fundraiser loaded correctly. The fundraiser correctly reported sales closed. Facebook reached the organization’s page and displayed a dismissible login prompt. No forms, registrations, payments, or messages were submitted.
- Activated all eight skip-to-content links and confirmed focus on each page’s main element.
- Checked the All / Upcoming / Past event filters: 3 / 1 / 2 visible event cards, respectively, at the review date.
- Replaced nine topic-specific email CTAs and eight footer email links with native navigation to the visible contact panel. Clicked all 17 revised links and confirmed the correct contact anchor, focus, topic, and encoded email subject.
- Tested all four mobile-menu destinations at a 390-pixel CSS viewport, along with menu closure after navigation and Escape dismissal.
- Verified the mobile copy-email success feedback. Verified that the contact section remains reachable and its address readable with JavaScript disabled. The optional copy button correctly stays hidden without JavaScript.
- The contact panel now labels the actual mail-handler action “Open email app” and keeps a readable address and copy option beside it. The review browser cannot launch mailto URLs; delivery through a visitor’s configured mail application remains device dependent.
- The private-host browser click-through remains unverified because authentication could not be completed in the review browser. Local click-through and native deployment success do not prove the production host’s folder-routing behavior. No hosting-routing changes were made without evidence of a defect.

[Revised mobile contact panel](contact-mobile.jpg)

## Original logo update

Reviewed November 24, 2026 (America/Chicago), against the exact private-deployment files in the managed local browser preview.

- Replaced the temporary text header with the original Knot-4-Profit Collaborations PNG recovered from the Pony Express sponsor listing and corroborated against the organization's Facebook profile. The original image is included without cropping, recoloring, redrawing, or enlargement; source details are in the README.
- Checked the header at desktop and 390-pixel phone frame widths. At a 320-pixel frame width, reduced the logo to 148 pixels and tightened the gap so the Menu button stays beside it. The 320-pixel frame's usable document width and scroll width both measured 305 pixels, with no horizontal overflow.
- Confirmed the image loads at its original 300-by-250 intrinsic dimensions on the homepage and nested event page. Clicked the nested page's logo to return home, and checked mobile menu opening and Escape dismissal.
- All eight generated pages resolve both the header logo and PNG favicon. The static link, asset, metadata, mount-path, and generator-consistency checks passed again. The small logo lettering and favicon remain limited by the recovered asset's modest resolution.

[Updated mobile header](logo-home-mobile.jpg)

## Logo-based palette update

Reviewed November 24, 2026 (America/Chicago), against the exact private-deployment files in the managed local browser preview.

- Applied the agreed seven-color palette across all eight pages: Logo Sky `#B4E3F7`, Knot Blue `#2C6D91`, Ink `#203139`, Cloud `#F5FAFC`, Mist `#E4F3FA`, Slate `#526A76`, and Deep Blue `#204D67`. Replaced the former yellow and peach themes with `sky`, `deep`, and `mist`; regenerated browser theme-color metadata.
- Original logo and banner bytes, page content, navigation destinations, layout dimensions, and JavaScript behavior are unchanged. CSS now keeps small text on Logo Sky in Ink or Deep Blue, and places Slate copy on lighter surfaces.
- Reviewed the homepage at 1440- and 390-pixel frame widths, the event listing and selected filter hover state on desktop, and the contact panel with keyboard focus on a phone. Checked the narrow 320-pixel header, menu opening, and Escape dismissal. No horizontal overflow: the narrow document measured 305/305 pixels and the phone contact document 375/375 pixels for client/scroll width.
- Read back computed browser colors for the header, page, selected filters, event date panels, status badges, contact buttons, supporting copy, footer, and keyboard focus. Confirmed the selected event filter stays white on Knot Blue and changes to Deep Blue while hovered.
- Focused mathematical contrast checks passed: Ink on Logo Sky 9.79:1; Deep Blue on Logo Sky 6.59:1; Slate on Cloud 5.42:1 and Mist 5.02:1; white on Knot Blue 5.67:1 and Deep Blue 9.06:1; Mist on Knot Blue 5.00:1. The Logo Sky focus ring on Knot Blue is 4.12:1. These checks do not establish full accessibility conformance.
- The eight-page static link, anchor, asset, metadata, mount-path, and generator-consistency checks passed. A separate read-only code review found no accidental content, link, or layout changes.

Current palette screenshots: [desktop home](palette-home-desktop.jpg), [phone home](palette-home-mobile.jpg), and [phone contact with keyboard focus](palette-contact-mobile.jpg).

## Screenshots

These are actual Chromium screenshots of the implemented pages. Responsive sizes were rendered in same-origin review frames with the stated CSS viewport widths; these are not physical-device tests. Screenshots omit the private review toolbar. The initial-build and original-logo screenshots predate the palette update; use the palette screenshots above for current colors and branding.

- [Homepage, 1440 px](home-desktop.jpg)
- [Homepage, 390 px](home-mobile.jpg)
- [Event, 1440 px](event-desktop.jpg)
- [Event, 390 px](event-mobile.jpg)

## Boundaries

- The GitHub change remains a draft branch; the FWIW production path has not been published. A separate owner-private Site is deployed for review. GitHub merge and FWIW publication remain subject to the agreed release approval.
- No automated Lighthouse score or full accessibility conformance claim is made. Field performance and production-host read-back remain future checks.
- Core content is static, with local fonts and small progressive-enhancement scripts. There is no service worker, runtime framework, analytics, payment processing, or contact-form submission service.
- The original published organization banner is included on About, and the original organization logo is now used in the header and browser icon. The remaining palette and typesetting are design proposals for review. No documentary photography or unapproved board portraits are used.
- The event editor is not configured. The README explains the source format and the additional requirements for a usable visual-editor handoff.
- Preview pages retain `noindex, nofollow`. Final origin, social metadata, indexing, and domain migration must be set deliberately at an approved launch.
