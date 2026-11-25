#!/usr/bin/env python3
"""Generate committed, build-free pages from public content. Python 3.10+."""
import argparse
from datetime import datetime
from html import escape
import json
from pathlib import Path
from urllib.parse import quote, urlparse

ROOT = Path(__file__).resolve().parents[1]
SITE = json.loads((ROOT / 'content/site.json').read_text())
EVENTS = json.loads((ROOT / 'content/events.json').read_text())
PAGES = []


def esc(value):
    return escape(str(value), quote=True)


def relative(page, target=''):
    return '../' * len(page.strip('/').split('/')) + target if page else './' + target


def contact_link(page, subject):
    return relative(page, 'get-involved/') + '?subject=' + quote(subject[:160], safe='') + '#contact'


def button(label, href, style='primary', extra=''):
    return f'<a class="button button--{style}" href="{esc(href)}" {extra}>{esc(label)}</a>'


def event_attributes(event):
    return ' '.join(f'data-{key.replace("_", "-")}="{esc(value)}"' for key, value in {
        'starts_at': event.get('starts_at') or '', 'ends_at': event.get('ends_at') or '',
        'archived': str(event.get('archived', False)).lower(), 'status': event.get('status', '')
    }.items())


def event_status(event):
    return 'Past event' if event.get('archived') else 'Event details'


def page_shell(page, title, description, content, active='', body_class=''):
    base = relative(page)
    canonical = SITE['site_url'].rstrip('/') + '/' + (page.strip('/') + '/' if page else '')
    navigation = [('events/', 'Events', 'events'), ('how-we-help/', 'How we help', 'help'),
                  ('about/', 'About', 'about'), ('get-involved/', 'Get involved', 'involved')]
    links = ''.join(f'<a href="{base}{path}"' + (' aria-current="page"' if key == active else '') + f'>{label}</a>' for path, label, key in navigation)
    robots = '<meta name="robots" content="noindex, nofollow">' if SITE['preview'] else '<meta name="robots" content="index, follow">'
    html = f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#2C6D91">
  <title>{esc(title)} | Knot-4-Profit Collaborations</title>
  <meta name="description" content="{esc(description)}">
  {robots}
  <link rel="canonical" href="{esc(canonical)}">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Knot-4-Profit Collaborations">
  <meta property="og:title" content="{esc(title)}">
  <meta property="og:description" content="{esc(description)}">
  <meta property="og:url" content="{esc(canonical)}">
  <meta property="og:image" content="{esc(SITE['site_url'].rstrip('/') + '/assets/brand-banner.jpg')}">
  <meta property="og:image:width" content="1440">
  <meta property="og:image:height" content="348">
  <meta property="og:image:alt" content="Knot-4-Profit Collaborations — nonprofit funding solutions">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="icon" href="{base}assets/brand-logo.png" type="image/png">
  <link rel="preload" href="{base}assets/fonts/barlow-condensed-800.ttf" as="font" type="font/ttf" crossorigin>
  <link rel="stylesheet" href="{base}assets/site.css">
  <script src="{base}assets/event-state.js" defer></script>
  <script src="{base}assets/site.js" defer></script>
</head>
<body class="{esc(body_class)}">
  <a class="skip-link" href="#main">Skip to content</a>
  <header class="site-header">
    <div class="container header-inner">
      <a class="wordmark" href="{base}" aria-label="Knot-4-Profit Collaborations home"><img class="brand-logo" src="{base}assets/brand-logo.png" width="300" height="250" alt="Knot-4-Profit Collaborations"></a>
      <button class="menu-toggle" type="button" aria-controls="primary-nav" aria-expanded="false" hidden><span>Menu</span><span class="menu-icon" aria-hidden="true"></span></button>
      <nav class="primary-nav" id="primary-nav" aria-label="Main navigation">{links}</nav>
    </div>
  </header>
  <main id="main" tabindex="-1">{content}</main>
  <footer class="site-footer">
    <div class="container footer-top">
      <div><p class="footer-name">Knot-4-Profit<br>Collaborations.</p><p class="footer-description">Good causes. Stronger connections.<br>Savannah, St. Joseph &amp; beyond.</p></div>
      <div class="footer-connect"><p class="eyebrow">Let’s connect</p><a class="email-link" href="{base}get-involved/#contact">{SITE['email']}</a><a class="text-link" href="{SITE['facebook']}">Find us on Facebook</a></div>
      <nav class="footer-nav" aria-label="Footer navigation">{links}</nav>
    </div>
    <div class="container footer-bottom"><p>© <span data-current-year>2026</span> Knot-4-Profit Collaborations</p><p>Bringing people together for good.</p></div>
  </footer>
</body>
</html>
'''
    PAGES.append((page, html))


def event_card(event, page, compact=False):
    href = relative(page, 'events/' + event['slug'] + '/')
    date = datetime.fromisoformat(event['date'])
    return f'''<article class="event-card theme-{event['theme']} {'event-card--compact' if compact else ''}" data-event-card {event_attributes(event)}>
      <div class="event-card-date"><time datetime="{event['date']}"><span>{date.strftime('%b')}</span><strong>{date.day:02}</strong><span>{date.year}</span></time><span class="event-state" data-event-status>{event_status(event)}</span></div>
      <div class="event-card-content"><p class="eyebrow">{esc(event['category'])}</p><h3><a href="{href}">{esc(event['short_title'])}</a></h3><p>{esc(event['summary'])}</p><p class="event-role">Our role <strong>{esc(event['role'])}</strong></p><a class="text-link" href="{href}">View event details<span class="sr-only">: {esc(event['short_title'])}</span></a></div>
    </article>'''


def invitation(page, title='Let’s make a good idea happen.'):
    return f'''<section class="invitation"><div class="container invitation-inner"><div><p class="eyebrow">A cause worth gathering for</p><h2>{title}</h2></div><div><p>Bring your organization, your idea, or your willingness to help. We’ll start with a conversation.</p>{button('Let’s connect', relative(page, 'get-involved/'), 'light')}</div></div></section>'''


def home():
    event = next(e for e in EVENTS if e.get('featured'))
    detail = './events/' + event['slug'] + '/'
    date = datetime.fromisoformat(event['date'])
    past = ''.join(event_card(e, '', True) for e in EVENTS if e.get('archived'))
    content = f'''
    <section class="home-hero container">
      <div class="hero-copy"><p class="eyebrow"><span class="small-spark" aria-hidden="true">✳</span> Rooted here. Bringing people together.</p><h1>Good causes.<br><span>Great company.</span></h1><p class="hero-lead">We help nonprofits bring fundraising events to life, connecting the planning, promotion, and people around a shared cause.</p><div class="button-group">{button('Explore events', './events/')}{button('Plan an event', './how-we-help/', 'outline')}</div><p class="hero-local">Savannah, St. Joseph &amp; the surrounding communities.</p></div>
      <aside class="hero-event" aria-labelledby="hero-event-title" data-event-record {event_attributes(event)}>
        <div class="hero-event-top"><span class="eyebrow">A reason to come together</span><span class="event-state" data-event-status>{event_status(event)}</span></div>
        <div class="hero-date"><span class="date-month">{date.strftime('%B')}</span><strong>{date.day}</strong><span class="date-year">{date.year}</span><div class="connection-rings" aria-hidden="true"><i></i><i></i></div></div>
        <div class="hero-event-bottom"><p class="eyebrow">{esc(event['time_label'] or event['date_label'])} · {esc(event['venue'])}</p><h2 id="hero-event-title">{esc(event['short_title'])}</h2><p>Benefiting {esc(event['beneficiary'])}</p><a class="text-link" href="{detail}">Discover the event</a></div>
      </aside>
    </section>
    <div class="purpose-band" aria-label="Our focus"><div class="container"><span>Fundraising</span><span aria-hidden="true">✳</span><span>Collaboration</span><span aria-hidden="true">✳</span><span>Community</span></div></div>
    <section class="section container how-section"><div class="section-heading"><p class="eyebrow">How we help</p><h2>Your cause.<br>A plan to bring <br>people together.</h2><a class="text-link" href="./how-we-help/">See how collaboration works</a></div><div class="service-list"><p class="section-intro">You know the work your organization wants to do. We help shape an event that gives people a way to take part.</p><article><h3>Shape the idea.</h3><p>Find an event approach that fits the cause, the community, and the people you want to reach.</p></article><article><h3>Bring the pieces together.</h3><p>Connect the planning, collaborators, and practical details that help an event take shape.</p></article><article><h3>Get the word out.</h3><p>Help people understand the cause, discover the event, and know how to participate.</p></article></div></section>
    <section class="section work-section"><div class="container"><div class="section-topline"><div><p class="eyebrow">Community in action</p><h2>Different events.<br>A shared spirit.</h2></div><a class="text-link" href="./events/">Explore all events</a></div><div class="past-grid">{past}</div></div></section>
    {invitation('')}
    '''
    page_shell('', 'Good causes. Great company.', 'Fundraising events, meaningful collaboration, and stronger community connections in Savannah, St. Joseph, and the surrounding area.', content, body_class='home')


def events_page():
    cards = ''.join(event_card(e, 'events') for e in EVENTS)
    content = f'''<section class="page-intro container"><p class="eyebrow">Find your next reason to show up</p><h1>Good things<br>happen together.</h1><p class="lead">Explore community events and the causes behind them. Come for the gathering. Be part of something good.</p></section>
    <section class="container events-section" aria-labelledby="events-heading"><div class="events-toolbar"><h2 id="events-heading">Events &amp; collaborations</h2><div class="event-filters" role="group" aria-label="Filter events" hidden><button type="button" data-filter="all" aria-pressed="true">All events</button><button type="button" data-filter="upcoming" aria-pressed="false">Upcoming</button><button type="button" data-filter="past" aria-pressed="false">Past events</button></div></div><p class="sr-only" data-filter-status role="status" aria-live="polite"></p><div class="event-list">{cards}</div><div class="empty-state" hidden><h3>More good things to come.</h3><p>There are no events in this view right now. Explore our past collaborations or get in touch about a future event.</p><a class="text-link" href="../get-involved/">Talk about an event</a></div></section>
    <section class="container event-note"><p>Every event has its own cause and collaborators. Our role is listed on each event, and registration stays with the event’s official provider.</p></section>{invitation('events', 'Have a cause to bring people around?')}'''
    page_shell('events', 'Events & collaborations', 'Find community events, explore the causes they support, and see Knot-4-Profit’s role in each collaboration.', content, 'events')


def detail_page(event):
    page = 'events/' + event['slug']
    base = relative(page)
    actions = ''.join(button(action['label'], action['url'], 'primary' if i == 0 else 'outline', f'data-event-action data-display-until="{esc(action["display_until"])}" hidden') for i, action in enumerate(event['actions']))
    paragraphs = ''.join(f'<p>{esc(p)}</p>' for p in event['description'])
    time = f'<span>{esc(event["time_label"])}</span>' if event['time_label'] else ''
    date = datetime.fromisoformat(event['date'])
    archive = '<p class="archive-note">This event has ended. The official website may include information about future editions.</p>' if event.get('archived') else '<p class="archive-note" data-ended-message hidden>This event has ended. Visit the official event page for any updates.</p>'
    content = f'''<section class="event-detail container" data-event-record {event_attributes(event)}><nav class="breadcrumb" aria-label="Breadcrumb"><a href="{base}events/">All events</a><span aria-hidden="true">/</span><span>Event details</span></nav><div class="event-detail-heading"><div><div class="event-kicker"><p class="eyebrow">{esc(event['category'])}</p><span class="event-state" data-event-status>{event_status(event)}</span></div><h1>{esc(event['title'])}</h1><p class="lead">{esc(event['summary'])}</p><div class="button-group event-actions">{actions}</div></div><div class="event-date-stamp theme-{event['theme']}"><time datetime="{event['date']}"><span>{date.strftime('%B')}</span><strong>{date.day:02}</strong><span>{date.year}</span></time></div></div>
    <div class="event-detail-body"><div class="event-story"><h2>{'A look at the collaboration.' if event.get('archived') else esc(event.get('story_heading', 'The cause behind the gathering.'))}</h2>{paragraphs}{archive}<a class="text-link" href="{esc(event['official_url'])}">{esc(event['official_label'])}</a><div class="event-question"><h3>Have a question?</h3><p>Connect with Terra about this event or ways to get involved.</p><a class="text-link" href="{contact_link(page, event['short_title'] + ' — question')}">Contact Terra</a></div></div><aside class="event-facts" aria-labelledby="event-facts-title"><h2 id="event-facts-title">The details</h2><dl><div><dt>When</dt><dd><time datetime="{event['date']}">{esc(event['date_label'])}</time>{time}</dd></div><div><dt>Where</dt><dd>{esc(event['venue'])}<span>{esc(event['address'])}</span></dd></div><div><dt>Benefiting</dt><dd>{esc(event['beneficiary'])}</dd></div><div><dt>Knot-4-Profit’s role</dt><dd>{esc(event['role'])}</dd></div></dl></aside></div></section>{invitation(page, 'There’s a place for you in the next one.')}'''
    page_shell(page, event['title'], event['summary'], content, 'events', 'event-page')


def help_page():
    content = f'''<section class="page-intro container"><p class="eyebrow">How we help</p><h1>Bring the cause.<br>Let’s build<br>the gathering.</h1><p class="lead">We help nonprofits and community organizations shape fundraising events, coordinate the moving parts, and connect with the people who can help.</p>{button('Talk about your event', contact_link('how-we-help', 'Let’s plan an event'))}</section>
    <section class="section container process-section"><div class="section-heading"><p class="eyebrow">From idea to invitation</p><h2>Purpose first.<br>People always.</h2><p>Every collaboration starts with understanding the cause. From there, we work together on what the event needs.</p></div><div class="service-list"><article><h3>Start with the purpose.</h3><p>What are you supporting? Who do you want to bring together? What would make the event useful for your organization? We start with those questions.</p></article><article><h3>Build the event around it.</h3><p>Explore the format, collaborators, promotion, and practical details that fit the idea. Agree on the work and responsibilities together.</p></article><article><h3>Make it easy to join in.</h3><p>Give people clear event information and connect them with the right registration, sponsorship, or support options.</p></article></div></section>
    <section class="support-section"><div class="container support-inner"><p class="eyebrow">The work around the event</p><h2>A little more connected.<br>A lot more possible.</h2><div class="support-grid"><article><h3>Event planning</h3><p>Turn an early idea into a gathering with a clear purpose and a practical plan.</p></article><article><h3>Collaboration</h3><p>Bring organizations, businesses, and supporters into a shared conversation.</p></article><article><h3>Promotion</h3><p>Help people find the event, understand the cause, and see how to take part.</p></article></div></div></section>
    <section class="section container conversation-section"><div><p class="eyebrow">Start wherever you are</p><h2>An idea is <br>enough to begin.</h2></div><div><p class="lead">You don’t need every detail figured out before you reach out.</p><p>Tell us about your organization, the cause you’re supporting, and the event you have in mind. If there’s a date or a particular challenge, include that too.</p>{button('Start a conversation', contact_link('how-we-help', 'An event idea for Knot-4-Profit'))}</div></section>'''
    page_shell('how-we-help', 'How we help', 'Bring a cause or an event idea. Knot-4-Profit helps connect planning, collaborators, and promotion around it.', content, 'help')


def about_page():
    content = f'''<section class="page-intro container"><p class="eyebrow">About Knot-4-Profit</p><h1>Community is<br>something<br>we do together.</h1><p class="lead">Good causes need people. Good gatherings give those people a way to show up.</p></section>
    <section class="section container about-story"><div class="about-name-block"><p class="eyebrow">The name behind the gathering</p><h2>Knot-4-Profit<br>Collaborations.</h2><p>Savannah, Missouri<br>Connected to the community around us.</p><div class="about-linework" aria-hidden="true"><span></span><span></span><span></span></div></div><div class="prose"><h2>Helping ideas become shared experiences.</h2><p>Founded by Terra James, Knot-4-Profit Collaborations works with nonprofits and community groups in Savannah, St. Joseph, and the surrounding area.</p><p>Our role is to help turn a cause or an idea into an event people can understand, support, and take part in. That means connecting the planning, promotion, and collaborators around the work.</p><p>Every event has its own purpose and partners. We keep the benefiting organization and its mission clear, whether we’re organizing a gathering, facilitating a fundraiser, or supporting an event as a sponsor.</p><div class="founder-note"><p class="eyebrow">Meet your first connection</p><h3>Terra James</h3><p>Founder &amp; President</p><a class="text-link" href="{contact_link('about', 'Let’s connect with Knot-4-Profit')}">Say hello to Terra</a></div></div></section>
    <section class="brand-section container"><img src="../assets/brand-banner.jpg" width="1440" height="348" loading="lazy" alt="Knot-4-Profit Collaborations: fundraising, collaboration, marketing, and community impact. Stronger nonprofits. Brighter communities."></section>
    {invitation('about', 'Good work starts with a connection.')}'''
    page_shell('about', 'About Knot-4-Profit', 'Meet Knot-4-Profit Collaborations, founded by Terra James to help nonprofits and community groups bring fundraising ideas to life.', content, 'about')


def involved_page():
    content = f'''<section class="page-intro container"><p class="eyebrow">Get involved</p><h1>A cause.<br>A connection.<br>A place for you.</h1><p class="lead">Bring your organization, your business, or your willingness to help. There’s more than one way to be part of a good thing.</p></section>
    <section class="container involvement-list" aria-label="Ways to get involved"><article><p class="eyebrow">Nonprofits &amp; community groups</p><div><h2>Bring your cause.</h2><p>Have an event idea or a fundraising goal? Tell us what you’re supporting and where you could use a collaborator.</p><a class="text-link" href="{contact_link('get-involved', 'Let’s discuss an event')}">Discuss an event</a></div></article><article><p class="eyebrow">Businesses &amp; sponsors</p><div><h2>Bring your support.</h2><p>Connect your business with a local cause. Ask about events and the ways you could help make one happen.</p><a class="text-link" href="{contact_link('get-involved', 'Sponsorship opportunities')}">Ask about sponsorship</a></div></article><article><p class="eyebrow">Volunteers &amp; neighbors</p><div><h2>Bring yourself.</h2><p>Tell us what interests you and how you’d like to help. Or find an event and come be part of it.</p><div class="inline-links"><a class="text-link" href="{contact_link('get-involved', 'I’d like to get involved')}">Explore ways to help</a><a class="text-link" href="../events/">Find an event</a></div></div></article></section>
    <section class="contact-panel" id="contact" tabindex="-1" aria-labelledby="contact-heading"><div class="container contact-inner"><div><p class="eyebrow">Let’s start a conversation</p><h2 id="contact-heading">Hello is a<br>good place to start.</h2><p>Connect directly with Terra James,<br>Founder &amp; President.</p></div><div class="contact-actions"><p class="contact-topic" data-contact-topic hidden></p><p class="contact-email">{SITE['email']}</p><div class="button-group">{button('Open email app', 'mailto:' + SITE['email'], 'light', 'data-email-launch')}<button type="button" class="button button--outline-light" data-copy-email="{SITE['email']}" hidden>Copy email address</button></div><p class="contact-help">Use your email app, or copy the address into the email service you use. If no app opens, you can still reach Terra at the address above.</p><p class="contact-feedback" role="status" data-copy-status aria-live="polite"></p><a class="text-link" href="{SITE['facebook']}">Follow Knot-4-Profit on Facebook</a></div></div></section>'''
    page_shell('get-involved', 'Get involved', 'Plan an event, ask about sponsorship, volunteer, or connect with Terra James at Knot-4-Profit Collaborations.', content, 'involved')


def validate():
    if not SITE['site_url'].startswith(('https://', 'http://')):
        raise ValueError('site_url must be an absolute HTTP(S) URL')
    seen = set()
    if sum(bool(event.get('featured')) for event in EVENTS) != 1:
        raise ValueError('Select exactly one featured event')
    for event in EVENTS:
        if event['slug'] in seen or any(c not in 'abcdefghijklmnopqrstuvwxyz0123456789-' for c in event['slug']):
            raise ValueError('Each event needs a unique lowercase URL slug')
        seen.add(event['slug'])
        datetime.fromisoformat(event['date'])
        for key in ('starts_at', 'ends_at'):
            if event.get(key) and datetime.fromisoformat(event[key]).tzinfo is None:
                raise ValueError(f'{key} requires a timezone offset')
        if event.get('starts_at') and event.get('ends_at') and datetime.fromisoformat(event['ends_at']) <= datetime.fromisoformat(event['starts_at']):
            raise ValueError('Event end must follow its start')
        for url in [event['official_url']] + [a['url'] for a in event['actions']]:
            if urlparse(url).scheme != 'https':
                raise ValueError('Event destinations must use https')
        for action in event['actions']:
            if datetime.fromisoformat(action['display_until']).tzinfo is None:
                raise ValueError('Action display cutoff requires a timezone offset')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--site-url', help='Override absolute canonical/social base URL for an export')
    parser.add_argument('--output', type=Path, default=ROOT, help='Output directory for generated HTML')
    parser.add_argument('--indexable', action='store_true', help='Remove preview noindex only for an approved launch')
    args = parser.parse_args()
    if args.site_url:
        SITE['site_url'] = args.site_url.rstrip('/') + '/'
    if args.indexable:
        SITE['preview'] = False
    validate()
    home()
    events_page()
    help_page()
    about_page()
    involved_page()
    for event in EVENTS:
        detail_page(event)
    for page, html in PAGES:
        destination = args.output / page / 'index.html'
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(html, encoding='utf-8')
    print(f'Generated {len(PAGES)} static pages at {args.output}; preview={SITE["preview"]}')


if __name__ == '__main__':
    main()
