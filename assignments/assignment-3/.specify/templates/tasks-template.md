---

description: "Task list template for feature implementation"
---

# Tasks: [FEATURE NAME]

**Input**: Design documents from `/specs/[###-feature-name]/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Static website**: `index.html`, `assets/css/`, `assets/js/`,
  `assets/data/`, `assets/images/`, and `docs/workflow-notes.md`
- All demo files must function locally in a computer web browser without a
  server setup step

<!-- 
  ============================================================================
  IMPORTANT: The tasks below are SAMPLE TASKS for illustration purposes only.
  
  The /speckit.tasks command MUST replace these with actual tasks based on:
  - User stories from spec.md (with their priorities P1, P2, P3...)
  - Feature requirements from plan.md
  - Local data/content from data-model.md
  - Browser interactions and static assets from plan.md
  
  Tasks MUST be organized by user story so each story can be:
  - Implemented independently
  - Tested independently
  - Demonstrated as an MVP increment
  
  DO NOT keep these sample tasks in the generated tasks.md file.
  ============================================================================
-->

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create project structure per implementation plan
- [ ] T002 Create local static website entry point in index.html
- [ ] T003 [P] Configure optional local linting or formatting tools

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

Examples of foundational tasks (adjust based on your project):

- [ ] T004 Create local CSS and JavaScript asset structure
- [ ] T005 [P] Add required local data files, images, fonts, or other assets
- [ ] T006 [P] Implement shared browser-side state or data loading utilities
- [ ] T007 Create base UI structure that all stories depend on
- [ ] T008 Configure browser-side error handling and console diagnostics
- [ ] T009 Document how to open the site locally without a server
- [ ] T010 Create workflow evidence notes file for prompts, AI responses, iteration decisions, and debugging observations

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - [Title] (Priority: P1) 🎯 MVP

**Goal**: [Brief description of what this story delivers]

**Independent Test**: [How to verify this story works on its own]

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T011 [P] [US1] Browser behavior test for [interaction] in tests/browser/test_[name].js
- [ ] T012 [P] [US1] Manual verification steps for [user journey] in docs/workflow-notes.md

### Implementation for User Story 1

- [ ] T013 [P] [US1] Add local data or content for [feature] in assets/data/[file].json
- [ ] T014 [P] [US1] Add styling for [feature] in assets/css/[file].css
- [ ] T015 [US1] Implement browser-side logic in assets/js/[file].js (depends on T013, T014)
- [ ] T016 [US1] Integrate [feature] markup in index.html
- [ ] T017 [US1] Add validation and error handling
- [ ] T018 [US1] Capture workflow evidence for user story 1 in [notes path]
- [ ] T019 [US1] Verify user story 1 with its independent demo or test path

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - [Title] (Priority: P2)

**Goal**: [Brief description of what this story delivers]

**Independent Test**: [How to verify this story works on its own]

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

- [ ] T020 [P] [US2] Browser behavior test for [interaction] in tests/browser/test_[name].js
- [ ] T021 [P] [US2] Manual verification steps for [user journey] in docs/workflow-notes.md

### Implementation for User Story 2

- [ ] T022 [P] [US2] Add local data or content for [feature] in assets/data/[file].json
- [ ] T023 [US2] Implement browser-side logic in assets/js/[file].js
- [ ] T024 [US2] Integrate [feature] markup in index.html
- [ ] T025 [US2] Integrate with User Story 1 components (if needed)
- [ ] T026 [US2] Capture workflow evidence for user story 2 in [notes path]
- [ ] T027 [US2] Verify user story 2 with its independent demo or test path

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - [Title] (Priority: P3)

**Goal**: [Brief description of what this story delivers]

**Independent Test**: [How to verify this story works on its own]

### Tests for User Story 3 (OPTIONAL - only if tests requested) ⚠️

- [ ] T028 [P] [US3] Browser behavior test for [interaction] in tests/browser/test_[name].js
- [ ] T029 [P] [US3] Manual verification steps for [user journey] in docs/workflow-notes.md

### Implementation for User Story 3

- [ ] T030 [P] [US3] Add local data or content for [feature] in assets/data/[file].json
- [ ] T031 [US3] Implement browser-side logic in assets/js/[file].js
- [ ] T032 [US3] Integrate [feature] markup in index.html
- [ ] T033 [US3] Capture workflow evidence for user story 3 in [notes path]
- [ ] T034 [US3] Verify user story 3 with its independent demo or test path

**Checkpoint**: All user stories should now be independently functional

---

[Add more user story phases as needed, following the same pattern]

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] TXXX [P] Documentation updates in docs/
- [ ] TXXX Code cleanup and refactoring
- [ ] TXXX Performance optimization across all stories
- [ ] TXXX [P] Additional unit tests (if requested) in tests/unit/
- [ ] TXXX Browser compatibility cleanup for local desktop browsers
- [ ] TXXX Run quickstart.md or local-open validation
- [ ] TXXX Verify the working demo by opening index.html locally without a server
- [ ] TXXX Assemble video outline with workflow evidence, prompts, iterations, debugging, and lessons learned
- [ ] TXXX Confirm the author can explain each major code section and design choice

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Local data/assets before browser-side logic
- Browser-side logic before final UI integration
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Local data, styling, and asset tasks within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together (if tests requested):
Task: "Browser behavior test for [interaction] in tests/browser/test_[name].js"
Task: "Manual verification steps for [user journey] in docs/workflow-notes.md"

# Launch local asset tasks for User Story 1 together:
Task: "Add local data or content for [feature] in assets/data/[file].json"
Task: "Add styling for [feature] in assets/css/[file].css"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Demo (MVP!)
3. Add User Story 2 → Test independently → Demo
4. Add User Story 3 → Test independently → Demo
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
