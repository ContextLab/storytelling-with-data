# Feature Specification: Pomodoro Timer Website

**Feature Branch**: `001-pomodoro-timer`  
**Created**: 2026-04-19  
**Status**: Draft  
**Input**: User description: "Build me a pomodoro timer website. User can set a timer to study in the class pomodoro fashion. There are pre-built in times like 50/10 or 25/5, but the user should be able to input whatever times they want for the study and break. The user should also be able to input tasks, when these tasks are complete they can check them off. When time has ended it should play a very loud alarm noise. Every time a user completes a task there should be a very satisfactory completion noise."

## Clarifications

### Session 2026-04-19

- Q: What should happen after a study or break phase reaches zero? -> A: Stop at each phase end, play alarm, and wait up to one minute before automatically starting the next phase.
- Q: Should tasks persist after the page reloads? -> A: Tasks persist across browser reloads on the same computer.
- Q: Should sound feedback have a visual fallback? -> A: Audio plus visible alarm/completion feedback.
- Q: How should the loud timer alarm stop? -> A: Alarm repeats until dismissed, stops after 10 seconds, then auto-starts the next phase after one waiting minute.
- Q: What duration input format should custom timers use? -> A: HH:MM:SS-style whole-number hours, minutes, and seconds fields; hide the hour segment when it is zero.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Run a Pomodoro Session (Priority: P1)

A student starts a focused study session using a preset Pomodoro pattern, watches
the timer count down, and receives a loud alarm when the study or break period
ends.

**Why this priority**: The timer cycle is the core value of the website and must
work before task tracking or extra customization matters.

**Independent Test**: Start a preset session, let the visible countdown reach
zero, and confirm the session transitions and a loud alarm plays.

**Acceptance Scenarios**:

1. **Given** the website is open with the 25/5 preset selected, **When** the user starts the timer, **Then** the study timer begins counting down from 25 minutes.
2. **Given** a study or break timer is running, **When** the countdown reaches zero, **Then** the website plays a loud repeating alarm for up to 10 seconds, shows visible alarm feedback, clearly indicates the ended phase, and waits for the user to start the next phase.
3. **Given** a phase has ended and the user has not started the next phase, **When** one minute passes after the ended phase, **Then** the website automatically starts the next phase.
4. **Given** a timer is running, **When** the user pauses and resumes it, **Then** the countdown stops and restarts without losing the remaining time.
5. **Given** a timer is running, **When** the user resets it, **Then** the countdown returns to the currently selected study duration.
6. **Given** a timer is running, **When** the user switches to another tab or window and later returns, **Then** the timer reflects the real elapsed time instead of pausing or drifting.

---

### User Story 2 - Customize Study and Break Times (Priority: P2)

A student chooses either a built-in preset such as 50/10 or 25/5, or enters
their own study and break durations before starting a session.

**Why this priority**: Different classes and study habits use different work and
break lengths, so customization makes the timer useful beyond one fixed pattern.

**Independent Test**: Enter custom study and break durations, start the timer,
and confirm the countdown uses those values.

**Acceptance Scenarios**:

1. **Given** the website offers built-in timing presets, **When** the user selects 50/10, **Then** the study duration is 50 minutes and the break duration is 10 minutes.
2. **Given** the user enters custom positive whole-number hours, minutes, and seconds for study and break durations, **When** the user applies them, **Then** the timer uses the custom durations for the next session.
3. **Given** the user enters an invalid custom duration, **When** the user tries to apply it, **Then** the website explains the problem and keeps the last valid duration.
4. **Given** a selected duration has zero hours, **When** the timer is displayed, **Then** the hour segment is hidden and the timer shows only minutes and seconds.

---

### User Story 3 - Track and Complete Study Tasks (Priority: P3)

A student adds tasks for the study session, checks tasks off as they complete
them, and hears a satisfying completion sound for each completed task.

**Why this priority**: Task tracking adds focus and progress feedback, but it is
secondary to the timer itself.

**Independent Test**: Add a task, mark it complete, and confirm it visibly moves
to a completed state while a satisfying sound plays.

**Acceptance Scenarios**:

1. **Given** the user has typed a task, **When** the user adds it, **Then** the task appears in the active task list.
2. **Given** an active task is visible, **When** the user checks it off, **Then** the task is marked complete, a satisfying completion sound plays, and visible completion feedback appears.
3. **Given** multiple tasks exist, **When** the user completes one task, **Then** only that task changes completion state.
4. **Given** the user has added tasks, **When** the user reloads the page in the same browser on the same computer, **Then** the task list is restored with each task's completion status.

---

### Edge Cases

- What happens when a user tries to start the timer with missing, all-zero,
  negative, decimal, or non-numeric custom duration fields?
- What happens when the browser blocks sound before the user has interacted with
  the page?
- What visible feedback appears if alarm or completion sounds cannot play?
- How does the website avoid multiple overlapping alarms if the timer ends while
  the user repeatedly presses controls?
- What happens when a phase ends and the user does not respond to the alarm or
  start the next phase manually?
- How does the timer stay accurate when the browser tab is hidden, inactive, or
  throttled by the browser?
- What happens when a user adds an empty task or a task containing only spaces?
- How does the timer display durations shorter than one minute?
- How does the timer display custom durations with zero hours versus one or more
  hours?
- What happens if the user reloads the page after adding or completing tasks?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The website MUST provide at least two built-in Pomodoro presets: 25 minutes study / 5 minutes break and 50 minutes study / 10 minutes break.
- **FR-002**: The website MUST allow users to enter custom study and break durations with HH:MM:SS-style whole-number hour, minute, and second fields before starting a timer session.
- **FR-003**: The website MUST validate custom durations and reject missing, all-zero, negative, decimal, or non-numeric values with a clear message. Minute and second fields MUST accept only values from 0 through 59.
- **FR-004**: The website MUST display the current session type as study or break.
- **FR-005**: The website MUST display the remaining time in a format users can read quickly.
- **FR-006**: The website MUST hide the hour segment in the timer display when the remaining duration has zero hours and show the hour segment when the remaining duration is one hour or more.
- **FR-007**: Users MUST be able to start, pause, resume, and reset the timer.
- **FR-008**: When a study or break period reaches zero, the website MUST play a loud repeating alarm sound for up to 10 seconds, show visible alarm feedback, clearly show that the period ended, and allow the user to start the next phase manually.
- **FR-009**: The website MUST prevent repeated control presses from creating overlapping countdowns or overlapping alarm playback.
- **FR-010**: While a timer is running, the website MUST keep countdown progress accurate when the user switches to another tab, another window, or otherwise leaves the page inactive.
- **FR-011**: When the user returns to the tab after a timer period should have ended, the website MUST show the ended state, show visible alarm feedback, and play or present the timer alarm as soon as browser audio rules allow.
- **FR-012**: If the user does not manually start the next phase within one minute after a phase ends, the website MUST automatically start the next phase.
- **FR-013**: Users MUST be able to dismiss the timer alarm before the 10-second maximum duration ends.
- **FR-014**: Users MUST be able to add study tasks with visible task text.
- **FR-015**: Users MUST be able to check tasks off as complete.
- **FR-016**: When a user completes a task, the website MUST play a satisfying completion sound and show visible completion feedback.
- **FR-017**: The website MUST reject empty or whitespace-only tasks.
- **FR-018**: The website MUST keep completed tasks visually distinguishable from active tasks.
- **FR-019**: The website MUST persist tasks and each task's completion status across browser reloads on the same computer.
- **FR-020**: Demo MUST include a clear runnable path that can be shown in the final video.
- **FR-021**: Workflow notes MUST capture prompts, AI responses, iterations, and debugging evidence needed for the final video.
- **FR-022**: Implementation MUST remain explainable by the author at the level of major code sections and design choices.
- **FR-023**: Demo MUST be a static HTML website that opens and functions from local files in a computer web browser.
- **FR-024**: Demo MUST NOT require iOS, Android, backend services, deployment infrastructure, or a local server setup.

### Key Entities *(include if feature involves data)*

- **Timer Session**: The current study or break period, including selected study duration, selected break duration, whole-number hour/minute/second duration inputs, remaining time, running state, current phase, ended-phase waiting state, and the wall-clock time needed to remain accurate while the tab is inactive.
- **Preset**: A built-in pair of study and break durations that the user can select quickly.
- **Task**: A user-entered study item with text and completion status that persists across browser reloads on the same computer.
- **Sound Alert**: A user-feedback event for either timer completion or task completion, paired with visible feedback so the event remains clear if audio cannot play. Timer alarms repeat until dismissed or until the 10-second maximum duration ends.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A user can start a preset 25/5 or 50/10 session in no more than two interactions after opening the website.
- **SC-002**: A user can set custom study and break durations with HH:MM:SS-style whole-number hour, minute, and second fields and begin a session using those durations in under 30 seconds.
- **SC-003**: The timer visibly updates at least once per second while running.
- **SC-004**: The timer alarm is clearly audible in a normal room when the browser allows sound playback, repeats for no more than 10 seconds unless dismissed earlier, and visible alarm feedback appears even if audio is blocked.
- **SC-005**: A user can add, complete, and visually identify at least five tasks during one session.
- **SC-006**: Completing a task produces audible positive feedback within one second when the browser allows sound playback, and visible completion feedback appears even if audio is blocked.
- **SC-007**: Invalid custom durations and empty tasks are rejected without changing the current valid timer or task list state.
- **SC-008**: If the user leaves the timer tab inactive for at least one minute and returns, the displayed remaining time is within two seconds of the expected real elapsed time.
- **SC-009**: After a page reload in the same browser on the same computer, previously added tasks and their completion states are restored.
- **SC-010**: If the user does not start the next phase manually after a phase ends, the next phase starts automatically after one minute of waiting.
- **SC-011**: Timer display hides the hour segment whenever the remaining duration has zero hours and shows the hour segment whenever the remaining duration is one hour or more.
- **SC-012**: Demo can be run from the documented setup path and verified with the acceptance scenarios.
- **SC-013**: Video outline has concrete workflow evidence for what was built, how AI was used, and what was learned.
- **SC-014**: Demo opens directly in a local computer web browser without starting a server.

## Assumptions

- The user interacts with the page before expecting audio, because many browsers
  block sound until after a user gesture.
- Loud and satisfying sounds can be generated or included locally as repository
  assets.
- Timer durations are entered as HH:MM:SS-style whole-number hours, minutes, and seconds.
- Mobile support, backend services, deployment, and local server setup are out of scope.
- Task data persists across reloads in the same browser on the same computer.
