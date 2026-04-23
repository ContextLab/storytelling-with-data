# Tasks: Pomodoro Timer Website

**Input**: Design documents from `specs/001-pomodoro-timer/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, quickstart.md

**Tests**: Manual browser verification tasks are included because the spec requires local browser verification and visible/audio behavior checks.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Static website**: `index.html`, `assets/css/styles.css`, `assets/js/app.js`, and `docs/workflow-notes.md`
- All demo files must function locally in a computer web browser without a server setup step

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Establish the static website files and workflow evidence location.

- [X] T001 Create static website directories `assets/css/`, `assets/js/`, `assets/data/`, `assets/images/`, and `docs/`
- [X] T002 Create initial HTML shell in `index.html`
- [X] T003 [P] Create base stylesheet in `assets/css/styles.css`
- [X] T004 [P] Create JavaScript entry file in `assets/js/app.js`
- [X] T005 Create workflow evidence notes in `docs/workflow-notes.md`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Build shared layout, state, utilities, and local persistence used by all stories.

**CRITICAL**: No user story work can begin until this phase is complete.

- [X] T006 Link `assets/css/styles.css` and `assets/js/app.js` from `index.html`
- [X] T007 Create responsive page layout regions for timer, controls, custom durations, tasks, and feedback in `index.html`
- [X] T008 Define core app state, preset constants, duration conversion helpers, and DOM references in `assets/js/app.js`
- [X] T009 Implement browser local storage helpers for task persistence in `assets/js/app.js`
- [X] T010 Implement local Web Audio feedback helpers and visible feedback helper in `assets/js/app.js`
- [X] T011 Add base visual design, responsive layout, focus states, and feedback styles in `assets/css/styles.css`

**Checkpoint**: Static page opens locally and exposes the required UI regions without server setup.

---

## Phase 3: User Story 1 - Run a Pomodoro Session (Priority: P1)

**Goal**: User can run a Pomodoro phase, pause/resume/reset it, leave the tab without timer drift, hear/see phase-end feedback, and get automatic next-phase start after one waiting minute.

**Independent Test**: Start a short timer, switch tabs, return, verify real elapsed time, let the phase end, confirm alarm/visible feedback, dismiss alarm, and confirm next phase can start manually or automatically after one minute.

### Implementation for User Story 1

- [X] T012 [US1] Add timer display, phase label, preset buttons, and start/pause/resume/reset controls in `index.html`
- [X] T013 [US1] Implement timer phase state transitions and wall-clock countdown calculation in `assets/js/app.js`
- [X] T014 [US1] Implement start, pause, resume, and reset control handlers in `assets/js/app.js`
- [X] T015 [US1] Implement loud repeating alarm, dismiss control behavior, 10-second alarm maximum, and visible alarm feedback in `assets/js/app.js`
- [X] T016 [US1] Implement one-minute ended-phase wait and automatic next-phase start in `assets/js/app.js`
- [X] T017 [US1] Style timer display, phase states, alarm state, and controls in `assets/css/styles.css`
- [X] T018 [US1] Document US1 verification steps and results in `docs/workflow-notes.md`
- [X] T019 [US1] Verify US1 manually by opening `index.html` locally and following quickstart timer scenarios

**Checkpoint**: User Story 1 is fully functional and testable independently.

---

## Phase 4: User Story 2 - Customize Study and Break Times (Priority: P2)

**Goal**: User can choose 25/5 or 50/10 presets, or enter custom whole-number HH:MM:SS study and break durations with validation and correct display.

**Independent Test**: Select both presets, enter valid and invalid custom durations, confirm timer uses valid custom values, and confirm hour segment hides when zero.

### Implementation for User Story 2

- [X] T020 [US2] Add HH:MM:SS-style whole-number study and break duration inputs and validation message area in `index.html`
- [X] T021 [US2] Implement preset selection and custom duration application in `assets/js/app.js`
- [X] T022 [US2] Implement validation for missing, all-zero, negative, decimal, non-numeric, and minute/second values over 59 in `assets/js/app.js`
- [X] T023 [US2] Implement timer display formatting that hides the hour segment when hours are zero in `assets/js/app.js`
- [X] T024 [US2] Style duration inputs, preset states, and validation messages in `assets/css/styles.css`
- [X] T025 [US2] Document US2 verification steps and results in `docs/workflow-notes.md`
- [X] T026 [US2] Verify US2 manually by opening `index.html` locally and following quickstart custom duration scenarios

**Checkpoint**: User Stories 1 and 2 both work independently.

---

## Phase 5: User Story 3 - Track and Complete Study Tasks (Priority: P3)

**Goal**: User can add tasks, reject empty tasks, complete tasks with satisfying audio/visible feedback, distinguish completed tasks, and keep task state after reload.

**Independent Test**: Add at least five tasks, complete one, confirm only that task changes, reload the page, and confirm task text and completion state persist.

### Implementation for User Story 3

- [X] T027 [US3] Add task input, add button, task list, and task validation message area in `index.html`
- [X] T028 [US3] Implement task create, render, validation, completion toggle, and local storage persistence in `assets/js/app.js`
- [X] T029 [US3] Implement satisfying completion sound and visible completion feedback in `assets/js/app.js`
- [X] T030 [US3] Style active tasks, completed tasks, task controls, and completion feedback in `assets/css/styles.css`
- [X] T031 [US3] Document US3 verification steps and results in `docs/workflow-notes.md`
- [X] T032 [US3] Verify US3 manually by opening `index.html` locally and following quickstart task scenarios

**Checkpoint**: All user stories are independently functional.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Final validation, explainability, and assignment-readiness cleanup.

- [X] T033 Run full quickstart validation from `specs/001-pomodoro-timer/quickstart.md` and record results in `docs/workflow-notes.md`
- [X] T034 Review `index.html`, `assets/css/styles.css`, and `assets/js/app.js` for explainability and remove unused code
- [X] T035 Confirm the demo opens directly from local `index.html` without a server and document this in `docs/workflow-notes.md`
- [X] T036 Confirm workflow evidence includes prompts, AI responses, debugging notes, and verification notes in `docs/workflow-notes.md`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies
- **Foundational (Phase 2)**: Depends on Setup completion and blocks all user stories
- **User Story 1 (Phase 3)**: Depends on Foundational
- **User Story 2 (Phase 4)**: Depends on Foundational and integrates with timer display/control code from US1
- **User Story 3 (Phase 5)**: Depends on Foundational and can proceed after local storage helpers exist
- **Polish (Phase 6)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: MVP and core timer behavior
- **User Story 2 (P2)**: Builds on timer state and display from US1
- **User Story 3 (P3)**: Independent task tracking after foundational storage helpers

### Within Each User Story

- Markup before JavaScript event wiring
- State logic before UI styling polish
- Core behavior before verification
- Verification notes after manual testing

### Parallel Opportunities

- T003 and T004 can run in parallel after T002
- Styling tasks can proceed after related markup exists
- Documentation tasks can proceed after each story behavior is implemented

---

## Parallel Example: User Story 3

```bash
Task: "Implement task create, render, validation, completion toggle, and local storage persistence in assets/js/app.js"
Task: "Style active tasks, completed tasks, task controls, and completion feedback in assets/css/styles.css"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: User Story 1
4. Stop and validate timer behavior independently

### Incremental Delivery

1. Timer shell and shared utilities
2. User Story 1 timer lifecycle and alarm behavior
3. User Story 2 presets and custom duration input
4. User Story 3 persistent tasks and completion feedback
5. Full quickstart validation and workflow notes

## Notes

- Each completed task must be marked `[X]`.
- No task requires a local server or package installation.
- Browser audio may require prior user interaction; visible feedback remains required.
