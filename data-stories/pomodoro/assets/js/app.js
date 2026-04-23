(function () {
  "use strict";

  var TASK_STORAGE_KEY = "assignment3PomodoroTasks";
  var PRESETS = {
    "25-5": { study: 25 * 60, break: 5 * 60 },
    "50-10": { study: 50 * 60, break: 10 * 60 }
  };

  var els = {};
  var tasks = [];
  var audioContext = null;
  var alarmIntervalId = null;
  var alarmStopId = null;
  var autoStartId = null;
  var tickId = null;
  var feedbackClearId = null;

  var state = {
    phase: "study",
    studyDurationSeconds: PRESETS["25-5"].study,
    breakDurationSeconds: PRESETS["25-5"].break,
    remainingSeconds: PRESETS["25-5"].study,
    phaseEndAt: null,
    isRunning: false,
    endedPhase: null,
    endedAt: null,
    alarmDismissed: false
  };

  document.addEventListener("DOMContentLoaded", init);

  function init() {
    cacheElements();
    bindEvents();
    tasks = loadTasks();
    renderTasks();
    updateDurationInputs();
    renderTimer();
    showFeedback("Ready when you are.", "neutral");
  }

  function cacheElements() {
    els.phaseLabel = document.getElementById("phase-label");
    els.nextPhaseNote = document.getElementById("next-phase-note");
    els.statusStrip = document.getElementById("status-strip");
    els.timerDisplay = document.getElementById("timer-display");
    els.startPauseButton = document.getElementById("start-pause-button");
    els.resetButton = document.getElementById("reset-button");
    els.nextPhaseButton = document.getElementById("next-phase-button");
    els.dismissAlarmButton = document.getElementById("dismiss-alarm-button");
    els.feedbackRegion = document.getElementById("feedback-region");
    els.durationForm = document.getElementById("duration-form");
    els.durationMessage = document.getElementById("duration-message");
    els.presetButtons = Array.prototype.slice.call(document.querySelectorAll(".preset-button"));
    els.studyHours = document.getElementById("study-hours");
    els.studyMinutes = document.getElementById("study-minutes");
    els.studySeconds = document.getElementById("study-seconds");
    els.breakHours = document.getElementById("break-hours");
    els.breakMinutes = document.getElementById("break-minutes");
    els.breakSeconds = document.getElementById("break-seconds");
    els.taskForm = document.getElementById("task-form");
    els.taskInput = document.getElementById("task-input");
    els.taskMessage = document.getElementById("task-message");
    els.taskList = document.getElementById("task-list");
    els.taskCount = document.getElementById("task-count");
  }

  function bindEvents() {
    els.startPauseButton.addEventListener("click", handleStartPause);
    els.resetButton.addEventListener("click", resetTimer);
    els.nextPhaseButton.addEventListener("click", startNextPhase);
    els.dismissAlarmButton.addEventListener("click", dismissAlarm);
    els.durationForm.addEventListener("submit", applyCustomDurations);
    els.taskForm.addEventListener("submit", addTask);
    els.presetButtons.forEach(function (button) {
      button.addEventListener("click", function () {
        applyPreset(button.dataset.preset);
      });
    });
    document.addEventListener("visibilitychange", function () {
      if (!document.hidden) {
        updateTimerFromClock();
      }
    });
  }

  function handleStartPause() {
    unlockAudio();
    if (state.phase === "ended") {
      startNextPhase();
      return;
    }
    if (state.isRunning) {
      pauseTimer();
    } else {
      startCurrentPhase();
    }
  }

  function startCurrentPhase() {
    clearEndedWait();
    dismissAlarm();
    state.isRunning = true;
    state.phaseEndAt = Date.now() + state.remainingSeconds * 1000;
    startTicker();
    renderTimer();
    showFeedback(capitalize(state.phase) + " timer running.", "neutral");
  }

  function pauseTimer() {
    updateTimerFromClock();
    state.isRunning = false;
    state.phaseEndAt = null;
    stopTicker();
    renderTimer();
    showFeedback("Timer paused.", "neutral");
  }

  function resetTimer() {
    stopTicker();
    stopAlarm();
    clearEndedWait();
    state.phase = "study";
    state.isRunning = false;
    state.endedPhase = null;
    state.endedAt = null;
    state.alarmDismissed = false;
    state.remainingSeconds = state.studyDurationSeconds;
    state.phaseEndAt = null;
    renderTimer();
    showFeedback("Timer reset to study.", "neutral");
  }

  function startNextPhase() {
    stopAlarm();
    clearEndedWait();
    var nextPhase = state.endedPhase === "study" ? "break" : "study";
    state.phase = nextPhase;
    state.endedPhase = null;
    state.endedAt = null;
    state.alarmDismissed = false;
    state.remainingSeconds = nextPhase === "study" ? state.studyDurationSeconds : state.breakDurationSeconds;
    renderTimer();
    startCurrentPhase();
  }

  function startTicker() {
    stopTicker();
    tickId = window.setInterval(updateTimerFromClock, 250);
  }

  function stopTicker() {
    if (tickId) {
      window.clearInterval(tickId);
      tickId = null;
    }
  }

  function updateTimerFromClock() {
    if (!state.isRunning || !state.phaseEndAt) {
      renderTimer();
      return;
    }
    var remaining = Math.max(0, Math.ceil((state.phaseEndAt - Date.now()) / 1000));
    state.remainingSeconds = remaining;
    if (remaining <= 0) {
      endPhase();
    } else {
      renderTimer();
    }
  }

  function endPhase() {
    stopTicker();
    state.isRunning = false;
    state.endedPhase = state.phase;
    state.phase = "ended";
    state.endedAt = Date.now();
    state.remainingSeconds = 0;
    state.phaseEndAt = null;
    state.alarmDismissed = false;
    renderTimer();
    startAlarm();
    scheduleAutoStart();
    showFeedback("Time is up. The next phase will start in one minute.", "alarm");
  }

  function scheduleAutoStart() {
    clearEndedWait();
    autoStartId = window.setTimeout(function () {
      if (state.phase === "ended") {
        startNextPhase();
      }
    }, 60 * 1000);
  }

  function clearEndedWait() {
    if (autoStartId) {
      window.clearTimeout(autoStartId);
      autoStartId = null;
    }
  }

  function applyPreset(presetId) {
    var preset = PRESETS[presetId];
    if (!preset) {
      return;
    }
    state.studyDurationSeconds = preset.study;
    state.breakDurationSeconds = preset.break;
    resetTimer();
    updateDurationInputs();
    setSelectedPreset(presetId);
    els.durationMessage.textContent = "";
    showFeedback("Preset " + presetId.replace("-", " / ") + " applied.", "neutral");
  }

  function setSelectedPreset(presetId) {
    els.presetButtons.forEach(function (button) {
      button.classList.toggle("is-selected", button.dataset.preset === presetId);
    });
  }

  function applyCustomDurations(event) {
    event.preventDefault();
    var study = readDuration("study");
    var breakTime = readDuration("break");
    if (!study.ok) {
      els.durationMessage.textContent = "Study time: " + study.message;
      return;
    }
    if (!breakTime.ok) {
      els.durationMessage.textContent = "Break time: " + breakTime.message;
      return;
    }
    state.studyDurationSeconds = study.seconds;
    state.breakDurationSeconds = breakTime.seconds;
    setSelectedPreset("");
    resetTimer();
    els.durationMessage.textContent = "Custom times applied.";
  }

  function readDuration(prefix) {
    var values = {
      hours: document.getElementById(prefix + "-hours").value.trim(),
      minutes: document.getElementById(prefix + "-minutes").value.trim(),
      seconds: document.getElementById(prefix + "-seconds").value.trim()
    };
    var parsed = {};
    var fields = ["hours", "minutes", "seconds"];
    for (var i = 0; i < fields.length; i += 1) {
      var field = fields[i];
      if (!/^\d+$/.test(values[field])) {
        return { ok: false, message: "Use whole numbers only." };
      }
      parsed[field] = Number(values[field]);
    }
    if (parsed.minutes > 59 || parsed.seconds > 59) {
      return { ok: false, message: "Minutes and seconds must be 0 through 59." };
    }
    var total = parsed.hours * 3600 + parsed.minutes * 60 + parsed.seconds;
    if (total <= 0) {
      return { ok: false, message: "Duration must be greater than zero." };
    }
    return { ok: true, seconds: total };
  }

  function updateDurationInputs() {
    writeDuration("study", state.studyDurationSeconds);
    writeDuration("break", state.breakDurationSeconds);
  }

  function writeDuration(prefix, totalSeconds) {
    var parts = splitDuration(totalSeconds);
    document.getElementById(prefix + "-hours").value = String(parts.hours);
    document.getElementById(prefix + "-minutes").value = String(parts.minutes);
    document.getElementById(prefix + "-seconds").value = String(parts.seconds);
  }

  function renderTimer() {
    var displaySeconds = state.phase === "ended" ? 0 : state.remainingSeconds;
    els.timerDisplay.textContent = formatDuration(displaySeconds);
    els.statusStrip.dataset.phase = state.phase;
    if (state.phase === "ended") {
      var next = state.endedPhase === "study" ? "break" : "study";
      els.phaseLabel.textContent = capitalize(state.endedPhase || "phase") + " complete";
      els.nextPhaseNote.textContent = "Start " + next + " now or it will start in one minute.";
      els.startPauseButton.textContent = "Start " + next;
      els.nextPhaseButton.textContent = "Start " + next;
      els.nextPhaseButton.disabled = false;
      els.dismissAlarmButton.hidden = state.alarmDismissed;
      return;
    }
    els.phaseLabel.textContent = capitalize(state.phase) + " phase";
    els.nextPhaseNote.textContent = state.phase === "study" ? "Break is ready after this round." : "Study starts after this break.";
    els.startPauseButton.textContent = state.isRunning ? "Pause" : "Start";
    els.nextPhaseButton.textContent = state.phase === "study" ? "Start break" : "Start study";
    els.nextPhaseButton.disabled = true;
    els.dismissAlarmButton.hidden = true;
  }

  function formatDuration(totalSeconds) {
    var parts = splitDuration(totalSeconds);
    var minutes = pad(parts.minutes);
    var seconds = pad(parts.seconds);
    if (parts.hours > 0) {
      return pad(parts.hours) + ":" + minutes + ":" + seconds;
    }
    return minutes + ":" + seconds;
  }

  function splitDuration(totalSeconds) {
    var safeTotal = Math.max(0, Math.floor(totalSeconds));
    var hours = Math.floor(safeTotal / 3600);
    var minutes = Math.floor((safeTotal % 3600) / 60);
    var seconds = safeTotal % 60;
    return { hours: hours, minutes: minutes, seconds: seconds };
  }

  function pad(value) {
    return String(value).padStart(2, "0");
  }

  function loadTasks() {
    try {
      var stored = window.localStorage.getItem(TASK_STORAGE_KEY);
      return stored ? JSON.parse(stored) : [];
    } catch (error) {
      return [];
    }
  }

  function saveTasks() {
    window.localStorage.setItem(TASK_STORAGE_KEY, JSON.stringify(tasks));
  }

  function addTask(event) {
    event.preventDefault();
    var text = els.taskInput.value.trim();
    if (!text) {
      els.taskMessage.textContent = "Enter a task before adding it.";
      return;
    }
    tasks.push({
      id: String(Date.now()) + "-" + String(Math.random()).slice(2),
      text: text,
      completed: false,
      createdAt: Date.now(),
      completedAt: null
    });
    els.taskInput.value = "";
    els.taskMessage.textContent = "";
    saveTasks();
    renderTasks();
  }

  function renderTasks() {
    els.taskList.innerHTML = "";
    tasks.forEach(function (task) {
      var item = document.createElement("li");
      item.className = "task-item" + (task.completed ? " is-complete" : "");

      var button = document.createElement("button");
      button.type = "button";
      button.className = "task-check";
      button.setAttribute("aria-label", task.completed ? "Mark task incomplete" : "Complete task");
      button.textContent = task.completed ? "✓" : "";
      button.addEventListener("click", function () {
        toggleTask(task.id);
      });

      var text = document.createElement("span");
      text.className = "task-text";
      text.textContent = task.text;

      item.appendChild(button);
      item.appendChild(text);
      els.taskList.appendChild(item);
    });
    var completeCount = tasks.filter(function (task) { return task.completed; }).length;
    els.taskCount.textContent = tasks.length + " tasks, " + completeCount + " done";
  }

  function toggleTask(id) {
    var task = tasks.find(function (candidate) {
      return candidate.id === id;
    });
    if (!task) {
      return;
    }
    var wasComplete = task.completed;
    task.completed = !task.completed;
    task.completedAt = task.completed ? Date.now() : null;
    saveTasks();
    renderTasks();
    if (!wasComplete && task.completed) {
      playCompleteSound();
      showFeedback("Task complete. Nice work.", "success");
    }
  }

  function unlockAudio() {
    if (!audioContext) {
      var Context = window.AudioContext || window.webkitAudioContext;
      if (Context) {
        audioContext = new Context();
      }
    }
    if (audioContext && audioContext.state === "suspended") {
      audioContext.resume();
    }
  }

  function startAlarm() {
    unlockAudio();
    stopAlarm();
    playAlarmTone();
    alarmIntervalId = window.setInterval(playAlarmTone, 650);
    alarmStopId = window.setTimeout(stopAlarm, 10 * 1000);
  }

  function stopAlarm() {
    if (alarmIntervalId) {
      window.clearInterval(alarmIntervalId);
      alarmIntervalId = null;
    }
    if (alarmStopId) {
      window.clearTimeout(alarmStopId);
      alarmStopId = null;
    }
  }

  function dismissAlarm() {
    stopAlarm();
    if (state.phase === "ended") {
      state.alarmDismissed = true;
      renderTimer();
      showFeedback("Alarm dismissed. Start the next phase or wait for auto-start.", "neutral");
    }
  }

  function playAlarmTone() {
    playTone(880, 0.18, 0.72, "square");
    window.setTimeout(function () {
      playTone(660, 0.18, 0.72, "square");
    }, 190);
  }

  function playCompleteSound() {
    unlockAudio();
    playTone(523.25, 0.08, 0.25, "sine");
    window.setTimeout(function () {
      playTone(659.25, 0.1, 0.25, "sine");
    }, 90);
    window.setTimeout(function () {
      playTone(783.99, 0.12, 0.25, "sine");
    }, 190);
  }

  function playTone(frequency, duration, gainValue, waveType) {
    if (!audioContext) {
      return;
    }
    var oscillator = audioContext.createOscillator();
    var gain = audioContext.createGain();
    oscillator.type = waveType;
    oscillator.frequency.value = frequency;
    gain.gain.setValueAtTime(gainValue, audioContext.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.001, audioContext.currentTime + duration);
    oscillator.connect(gain);
    gain.connect(audioContext.destination);
    oscillator.start();
    oscillator.stop(audioContext.currentTime + duration);
  }

  function showFeedback(message, kind) {
    window.clearTimeout(feedbackClearId);
    els.feedbackRegion.textContent = message;
    els.feedbackRegion.classList.toggle("is-alarm", kind === "alarm");
    els.feedbackRegion.classList.toggle("is-success", kind === "success");
    if (kind === "success") {
      feedbackClearId = window.setTimeout(function () {
        showFeedback("Keep going.", "neutral");
      }, 2200);
    }
  }

  function capitalize(value) {
    return value.charAt(0).toUpperCase() + value.slice(1);
  }
}());
