# Research: Pomodoro Timer Website

## Decision: Use Browser-Native HTML/CSS/JavaScript

**Rationale**: The constitution requires a local static HTML website with no
server setup. Plain browser files satisfy that constraint, keep the code
explainable, and avoid dependency installation or build steps.

**Alternatives considered**:
- Frontend framework: rejected because it adds package and build complexity for
  a small single-page demo.
- Python or server-backed app: rejected because the project scope forbids server
  setup.

## Decision: Track Timer Progress From Wall-Clock Timestamps

**Rationale**: Browsers throttle timers in inactive tabs. Calculating remaining
time from a stored phase end timestamp avoids drift when the tab is hidden and
lets the display catch up when the user returns.

**Alternatives considered**:
- Decrementing a counter every second: rejected because inactive tabs can pause
  or delay interval callbacks.
- Web Worker timer: rejected because it adds complexity and can still be
  throttled depending on browser behavior.

## Decision: Store Tasks In Browser Local Storage

**Rationale**: Tasks must persist across reloads on the same computer. Browser
local storage is available from local static files, requires no backend, and is
simple to explain.

**Alternatives considered**:
- Session-only state: rejected because clarified requirements require reload
  persistence.
- Downloaded/exported file: rejected because it complicates the core workflow.

## Decision: Generate Sounds Locally With Browser Audio

**Rationale**: The demo needs a loud alarm and satisfying completion sound while
keeping all required assets local. Browser audio can generate tones without
external media files. Visible feedback covers browsers that block or mute audio.

**Alternatives considered**:
- Downloaded audio files: rejected because they add asset sourcing and licensing
  concerns.
- Audio-only feedback: rejected because browser autoplay rules can block sound.

## Decision: Use HH:MM:SS-Style Whole-Number Inputs

**Rationale**: Clarification requires separate whole-number hour, minute, and
second fields. This supports fast testing with seconds while preserving normal
Pomodoro presets.

**Alternatives considered**:
- Decimal minutes: rejected by clarification.
- Whole minutes only: rejected because the user requested hour/minute/second
  sections.

## Decision: No External Interface Contracts

**Rationale**: The feature exposes no API, CLI, service endpoint, or data import
format to other systems. The user-facing behavior is already captured in the
spec acceptance scenarios and quickstart.

**Alternatives considered**:
- UI contract file: rejected because it would duplicate the spec without adding
  a separate external interface.
