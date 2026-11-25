"use strict";

const assert = require("node:assert/strict");
const { eventStatus, actionIsActive } = require("../assets/event-state.js");

const event = {
  starts_at: "2026-12-17T07:30:00-06:00",
  ends_at: "2026-12-17T09:30:00-06:00",
  timezone: "America/Chicago",
  archived: false
};
const start = Date.parse("2026-12-17T13:30:00Z");
const end = Date.parse("2026-12-17T15:30:00Z");
const cutoff = Date.parse("2026-12-16T18:00:00-06:00");
const action = { display_until: "2026-12-16T18:00:00-06:00" };
let passed = 0;

function test(name, run) {
  run();
  passed += 1;
  console.log(`PASS ${name}`);
}

test("event start is inclusive and end is exclusive", () => {
  assert.equal(eventStatus(event, start - 1), "upcoming");
  assert.equal(eventStatus(event, start), "ongoing");
  assert.equal(eventStatus(event, start + 1), "ongoing");
  assert.equal(eventStatus(event, end - 1), "ongoing");
  assert.equal(eventStatus(event, end), "past");
  assert.equal(eventStatus(event, end + 1), "past");
});

test("action expires exactly at its independent display cutoff", () => {
  assert.equal(actionIsActive(event, action, cutoff - 1), true);
  assert.equal(actionIsActive(event, action, cutoff), false);
  assert.equal(actionIsActive(event, action, cutoff + 1), false);
  assert.equal(eventStatus(event, cutoff), "upcoming");
});

test("an action never remains active after the event ends", () => {
  const lateAction = { display_until: "2026-12-18T00:00:00Z" };
  assert.equal(actionIsActive(event, lateAction, end - 1), true);
  assert.equal(actionIsActive(event, lateAction, end), false);
  assert.equal(actionIsActive(event, lateAction, end + 1), false);
});

test("different explicit offsets describe the same instant", () => {
  const equivalent = {
    ...event,
    starts_at: "2026-12-17T22:30:00+09:00",
    ends_at: "2026-12-17T15:30:00Z"
  };
  for (const now of [start - 1, start, end - 1, end]) {
    assert.equal(eventStatus(equivalent, now), eventStatus(event, now));
  }
  const utcAction = { display_until: "2026-12-17T00:00:00Z" };
  assert.equal(actionIsActive(event, utcAction, cutoff - 1), true);
  assert.equal(actionIsActive(event, utcAction, cutoff), false);
});

test("cancellation takes precedence over dates and archive state", () => {
  const cancelled = { ...event, status: "cancelled", archived: true };
  for (const now of [start - 1, start, end + 1]) {
    assert.equal(eventStatus(cancelled, now), "cancelled");
    assert.equal(actionIsActive(cancelled, action, now), false);
  }
});

test("archived events are past even when exact times are unavailable", () => {
  const archived = { archived: true, starts_at: null, ends_at: null };
  assert.equal(eventStatus(archived, cutoff - 1), "past");
  assert.equal(actionIsActive(archived, action, cutoff - 1), false);
  assert.equal(eventStatus({ ...event, archived: true }, start - 1), "past");
});

test("missing, malformed, or timezone-free dates fail closed", () => {
  const invalid = [undefined, null, "", "not-a-date", "2026-12-17",
    "2026-12-17T07:30:00", "2026-12-17T07:30:00-25:00",
    "2026-12-17T07:30:00-06:60", "2026-02-30T07:30:00Z",
    "2026-13-17T07:30:00Z", "2026-12-17T24:30:00Z"];
  for (const value of invalid) {
    assert.equal(eventStatus({ ...event, starts_at: value }, start - 1), "details");
    assert.equal(eventStatus({ ...event, ends_at: value }, start - 1), "details");
    assert.equal(actionIsActive(event, { display_until: value }, cutoff - 1), false);
  }
  assert.equal(eventStatus(null, start), "details");
  assert.equal(eventStatus({}, start), "details");
  assert.equal(actionIsActive(event, null, cutoff - 1), false);
});

test("reversed and zero-length event ranges are neutral", () => {
  assert.equal(eventStatus({ ...event, ends_at: event.starts_at }, start), "details");
  assert.equal(eventStatus({ ...event, starts_at: event.ends_at, ends_at: event.starts_at }, start), "details");
});

test("leap days are validated without Date.parse normalization", () => {
  const leapEvent = { starts_at: "2028-02-29T10:00:00Z", ends_at: "2028-02-29T12:00:00Z" };
  assert.equal(eventStatus(leapEvent, Date.parse("2028-02-29T11:00:00Z")), "ongoing");
  assert.equal(eventStatus({ ...leapEvent, starts_at: "2026-02-29T10:00:00Z" }, start), "details");
});

test("unknown statuses and invalid current times do not enable actions", () => {
  const postponed = { ...event, status: "postponed" };
  assert.equal(eventStatus(postponed, cutoff - 1), "details");
  assert.equal(actionIsActive(postponed, action, cutoff - 1), false);
  assert.equal(eventStatus({ ...event, status: "scheduled" }, start), "ongoing");
  for (const now of [NaN, Infinity, null, "2026-12-16"]) {
    assert.equal(eventStatus(event, now), "details");
    assert.equal(actionIsActive(event, action, now), false);
  }
});

test("omitting now uses the current clock for both functions", () => {
  const originalNow = Date.now;
  try {
    Date.now = () => cutoff - 1;
    assert.equal(eventStatus(event), "upcoming");
    assert.equal(actionIsActive(event, action), true);
    Date.now = () => end;
    assert.equal(eventStatus(event), "past");
    assert.equal(actionIsActive(event, action), false);
  } finally {
    Date.now = originalNow;
  }
});

console.log(`\n${passed} event-state checks passed.`);
