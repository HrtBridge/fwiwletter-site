/* Small progressive enhancements; all essential content is already in the HTML. */
(function () {
  'use strict';

  var header = document.querySelector('.site-header');
  var menu = document.querySelector('.menu-toggle');
  var navigation = document.querySelector('#primary-nav');
  if (header && menu && navigation) {
    function closeMenu(restoreFocus) {
      menu.setAttribute('aria-expanded', 'false');
      menu.querySelector('span').textContent = 'Menu';
      navigation.classList.remove('is-open');
      if (restoreFocus) menu.focus();
    }
    menu.addEventListener('click', function () {
      var open = menu.getAttribute('aria-expanded') !== 'true';
      menu.setAttribute('aria-expanded', String(open));
      menu.querySelector('span').textContent = open ? 'Close' : 'Menu';
      navigation.classList.toggle('is-open', open);
    });
    document.addEventListener('keydown', function (event) {
      if (event.key === 'Escape' && menu.getAttribute('aria-expanded') === 'true') closeMenu(true);
    });
    document.addEventListener('click', function (event) {
      if (!header.contains(event.target)) closeMenu(false);
    });
    navigation.addEventListener('click', function (event) {
      if (event.target.closest('a')) closeMenu(false);
    });
    window.matchMedia('(min-width: 801px)').addEventListener('change', function (event) {
      if (event.matches) closeMenu(false);
    });
    menu.hidden = false;
    header.classList.add('nav-ready');
  }

  var filters = document.querySelector('.event-filters');
  var cards = Array.from(document.querySelectorAll('[data-event-card]'));
  var activeFilter = 'all';
  var labels = { upcoming: 'Upcoming', ongoing: 'Happening now', past: 'Past event', cancelled: 'Cancelled', details: 'Event details' };

  function eventFrom(element) {
    return {
      starts_at: element.dataset.startsAt,
      ends_at: element.dataset.endsAt,
      archived: element.dataset.archived === 'true',
      status: element.dataset.status || 'scheduled'
    };
  }

  function filterCards(announce) {
    var count = 0;
    cards.forEach(function (card) {
      var status = card.dataset.currentStatus;
      var visible = activeFilter === 'all' || status === activeFilter || (activeFilter === 'upcoming' && status === 'ongoing');
      card.hidden = !visible;
      if (visible) count += 1;
    });
    var empty = document.querySelector('.empty-state');
    if (empty) empty.hidden = count !== 0;
    if (announce) {
      var result = document.querySelector('[data-filter-status]');
      if (result) result.textContent = count + (count === 1 ? ' event shown.' : ' events shown.');
    }
  }

  function refreshEvents() {
    if (!window.KnotEvents) return;
    var now = Date.now();
    document.querySelectorAll('[data-event-record], [data-event-card]').forEach(function (element) {
      var event = eventFrom(element);
      var status = window.KnotEvents.eventStatus(event, now);
      element.dataset.currentStatus = status;
      element.querySelectorAll('[data-event-status]').forEach(function (badge) { badge.textContent = labels[status]; });
      element.querySelectorAll('[data-event-action]').forEach(function (action) {
        action.hidden = !window.KnotEvents.actionIsActive(event, {display_until: action.dataset.displayUntil}, now);
      });
      var ended = element.querySelector('[data-ended-message]');
      if (ended) ended.hidden = status !== 'past';
    });
    if (filters) filterCards(false);
  }

  refreshEvents();
  if (filters && window.KnotEvents) {
    filters.hidden = false;
    filters.addEventListener('click', function (event) {
      var button = event.target.closest('[data-filter]');
      if (!button) return;
      activeFilter = button.dataset.filter;
      filters.querySelectorAll('button').forEach(function (item) { item.setAttribute('aria-pressed', String(item === button)); });
      filterCards(true);
    });
  }
  // Refresh on a long-lived page and when returning to the tab, without reloads.
  window.setInterval(refreshEvents, 30000);
  document.addEventListener('visibilitychange', function () { if (!document.hidden) refreshEvents(); });

  var contactTopic = document.querySelector('[data-contact-topic]');
  var emailLaunch = document.querySelector('[data-email-launch]');
  if (contactTopic && emailLaunch) {
    var emailAddress = emailLaunch.getAttribute('href');
    function updateContactTopic() {
      var subject = Array.from((new URLSearchParams(window.location.search).get('subject') || '')
        .replace(/[\u0000-\u001f\u007f]/g, ' ').trim()).slice(0, 160).join('');
      contactTopic.textContent = subject ? 'Your topic: ' + subject : '';
      contactTopic.hidden = !subject;
      emailLaunch.setAttribute('href', emailAddress + (subject ? '?subject=' + encodeURIComponent(subject) : ''));
    }
    updateContactTopic();
    window.addEventListener('pageshow', updateContactTopic);
    window.addEventListener('popstate', updateContactTopic);
  }

  var copyButton = document.querySelector('[data-copy-email]');
  var copyStatus = document.querySelector('[data-copy-status]');
  if (copyButton && navigator.clipboard && window.isSecureContext) {
    copyButton.hidden = false;
    copyButton.addEventListener('click', async function () {
      try {
        await navigator.clipboard.writeText(copyButton.dataset.copyEmail);
        copyStatus.textContent = 'Email address copied.';
      } catch (_) {
        copyStatus.textContent = 'Please select and copy the email address above.';
      }
    });
  }
  document.querySelectorAll('[data-current-year]').forEach(function (element) {
    element.textContent = new Date().getFullYear();
  });
}());
