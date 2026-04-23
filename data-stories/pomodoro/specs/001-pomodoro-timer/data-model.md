# Data Model: Pomodoro Timer Website

## Timer Session

Represents the current study or break flow.

**Fields**:
- `phase`: `study`, `break`, or `ended`
- `studyDurationSeconds`: positive integer total seconds
- `breakDurationSeconds`: positive integer total seconds
- `remainingSeconds`: non-negative integer derived from wall-clock time while running
- `phaseEndAt`: timestamp used to calculate remaining time while running
- `isRunning`: boolean
- `endedPhase`: `study` or `break` when a phase has ended
- `endedAt`: timestamp used to auto-start the next phase after one waiting minute
- `alarmDismissed`: boolean for the current ended phase

**Validation Rules**:
- Study and break durations must each be greater than zero.
- Custom duration fields must be whole numbers.
- Minute and second fields must be 0 through 59.
- Decimal, negative, missing, non-numeric, and all-zero durations are invalid.

**State Transitions**:
- `idle study` -> `running study` when the user starts a study phase.
- `running study` -> `ended study` when the wall-clock end time is reached.
- `ended study` -> `running break` when the user starts the break or one waiting minute passes.
- `running break` -> `ended break` when the wall-clock end time is reached.
- `ended break` -> `running study` when the user starts the next study phase or one waiting minute passes.
- Any running phase -> paused state when the user pauses.
- Any state -> idle study duration when the user resets.

## Preset

Represents a built-in study/break pair.

**Fields**:
- `id`: stable identifier
- `label`: user-facing preset label, such as `25/5`
- `studyDurationSeconds`: positive integer
- `breakDurationSeconds`: positive integer

**Initial Presets**:
- `25/5`: 25 minutes study, 5 minutes break
- `50/10`: 50 minutes study, 10 minutes break

## Duration Input

Represents the editable custom duration for study or break.

**Fields**:
- `hours`: whole number, zero or greater
- `minutes`: whole number from 0 through 59
- `seconds`: whole number from 0 through 59

**Display Rule**:
- Show `HH:MM:SS` when hours are one or greater.
- Hide the hour segment and show `MM:SS` when hours are zero.

## Task

Represents a user-entered study task.

**Fields**:
- `id`: stable local identifier
- `text`: non-empty trimmed task text
- `completed`: boolean
- `createdAt`: timestamp for stable ordering
- `completedAt`: timestamp or blank value

**Validation Rules**:
- Empty or whitespace-only task text is invalid.
- Completing one task must not change other task states.
- Tasks and completion states persist across reloads on the same computer.

## Sound Alert

Represents feedback for timer completion or task completion.

**Fields**:
- `type`: `timer-alarm` or `task-complete`
- `startedAt`: timestamp
- `dismissedAt`: timestamp or blank value
- `visibleFeedback`: boolean

**Rules**:
- Timer alarms repeat until dismissed or until 10 seconds pass.
- Timer alarm feedback remains visible at phase end.
- Task completion feedback plays within one second when audio is allowed and
  also shows visible completion feedback.
