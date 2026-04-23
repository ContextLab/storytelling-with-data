# Quickstart: Pomodoro Timer Website

## Run Locally

1. Open `index.html` directly in a desktop browser.
2. Do not start a local server.
3. Interact with the page once before expecting sound; browsers may block audio
   before user interaction.

## Verify Core Timer

1. Select the `25/5` preset.
2. Start the timer and confirm the study phase begins.
3. Pause, resume, and reset the timer.
4. Use a short custom duration with whole-number `HH:MM:SS` fields for faster
   testing, such as `00:00:05`.
5. Confirm the hour segment is hidden when hours are zero.

## Verify Phase End Behavior

1. Start a short study timer.
2. Let it reach zero.
3. Confirm a loud repeating alarm plays for no more than 10 seconds.
4. Confirm visible alarm feedback appears.
5. Dismiss the alarm before 10 seconds and confirm playback stops.
6. Let another phase end without manual action and confirm the next phase starts
   automatically after one minute of waiting.

## Verify Inactive Tab Accuracy

1. Start a timer for at least one minute.
2. Switch to another browser tab or window for at least one minute.
3. Return to the timer tab.
4. Confirm the displayed remaining time is within two seconds of the expected
   elapsed wall-clock time.

## Verify Custom Duration Validation

1. Try missing, all-zero, negative, decimal, and non-numeric values.
2. Try minute or second values greater than 59.
3. Confirm invalid values show a clear message and preserve the last valid
   timer state.

## Verify Tasks

1. Add at least five tasks.
2. Complete one task and confirm only that task changes state.
3. Confirm satisfying audio and visible completion feedback appear.
4. Reload the page in the same browser.
5. Confirm tasks and completion states are restored.

## Verify Assignment Evidence

1. Update `docs/workflow-notes.md` with prompts, AI responses, debugging notes,
   and verification results.
2. Confirm the demo and workflow notes support the final video narrative.
