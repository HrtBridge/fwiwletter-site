(function (root, factory) {
  if (typeof module === "object" && module.exports) {
    module.exports = factory();
  } else {
    root.KnotEvents = factory();
  }
})(typeof globalThis !== "undefined" ? globalThis : this, function () {
  "use strict";

  // Only accept complete ISO dates with an explicit offset or Z. Date.parse
  // alone normalizes impossible dates such as February 30 in some browsers.
  function timestamp(value) {
    if (typeof value !== "string") return NaN;
    var match = /^(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2})(?::(\d{2})(?:\.(\d+))?)?(Z|([+-])(\d{2}):(\d{2}))$/.exec(value);
    if (!match) return NaN;

    var year = Number(match[1]);
    var month = Number(match[2]);
    var day = Number(match[3]);
    var leap = year % 4 === 0 && (year % 100 !== 0 || year % 400 === 0);
    var days = [31, leap ? 29 : 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];

    if (month < 1 || month > 12 || day < 1 || day > days[month - 1] ||
        Number(match[4]) > 23 || Number(match[5]) > 59 ||
        Number(match[6] || 0) > 59 ||
        (match[8] !== "Z" && (Number(match[10]) > 23 || Number(match[11]) > 59))) {
      return NaN;
    }
    return Date.parse(value);
  }

  function eventStatus(event, now = Date.now()) {
    if (!event || typeof event !== "object") return "details";
    if (event.status === "cancelled") return "cancelled";
    if (event.archived === true) return "past";

    // Unknown statuses (for example, postponed) must not advertise availability.
    // An omitted status is scheduled, matching content/events.json.
    if (event.status != null && event.status !== "scheduled") return "details";

    var start = timestamp(event.starts_at);
    var end = timestamp(event.ends_at);
    if (!Number.isFinite(now) || !Number.isFinite(start) ||
        !Number.isFinite(end) || end <= start) return "details";
    if (now >= end) return "past";
    if (now >= start) return "ongoing";
    return "upcoming";
  }

  function actionIsActive(event, action, now = Date.now()) {
    var status = eventStatus(event, now);
    if (status !== "upcoming" && status !== "ongoing") return false;
    if (!action || typeof action !== "object") return false;
    var cutoff = timestamp(action.display_until);
    // display_until is this site's display cutoff, not a claim about when the
    // organizer's registration or sponsorship service officially closes.
    return Number.isFinite(cutoff) && now < cutoff;
  }

  return { eventStatus: eventStatus, actionIsActive: actionIsActive };
});
