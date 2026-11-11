/* Computer-Based Test (CBT) Engine */
class CBTEngine {
  constructor(totalMins = 60) {
    this.remainingSeconds = totalMins * 60;
    this.timerInterval = null;
    this.flaggedQuestions = new Set();
  }

  startTimer(displayElementId, onTimeUpCallback) {
    const displayEl = document.getElementById(displayElementId);
    if (!displayEl) return;

    this.timerInterval = setInterval(() => {
      if (this.remainingSeconds <= 0) {
        clearInterval(this.timerInterval);
        displayEl.innerText = "00:00:00";
        if (onTimeUpCallback) onTimeUpCallback();
        return;
      }

      this.remainingSeconds--;
      const hrs = Math.floor(this.remainingSeconds / 3600);
      const mins = Math.floor((this.remainingSeconds % 3600) / 60);
      const secs = this.remainingSeconds % 60;

      const pad = (n) => n.toString().padStart(2, '0');
      displayEl.innerText = `${pad(hrs)}:${pad(mins)}:${pad(secs)}`;
    }, 1000);
  }

  toggleFlag(questionId) {
    if (this.flaggedQuestions.has(questionId)) {
      this.flaggedQuestions.delete(questionId);
    } else {
      this.flaggedQuestions.add(questionId);
    }
    this.updatePaletteUI();
  }

  highlightSelectedText() {
    const selection = window.getSelection();
    if (!selection.rangeCount || selection.isCollapsed) return;

    const range = selection.getRangeAt(0);
    const span = document.createElement('span');
    span.className = 'highlighted-text';
    range.surroundContents(span);
  }

  updatePaletteUI() {
    this.flaggedQuestions.forEach((qId) => {
      const btn = document.getElementById(`nav-btn-${qId}`);
      if (btn) btn.classList.add('flagged');
    });
  }

  bindKeyboardShortcuts(onNext, onPrev, onFlag) {
    document.addEventListener('keydown', (e) => {
      if (e.altKey && e.key.toLowerCase() === 'n') {
        e.preventDefault();
        if (onNext) onNext();
      } else if (e.altKey && e.key.toLowerCase() === 'p') {
        e.preventDefault();
        if (onPrev) onPrev();
      } else if (e.altKey && e.key.toLowerCase() === 'f') {
        e.preventDefault();
        if (onFlag) onFlag();
      }
    });
  }
}

window.cbtEngine = new CBTEngine();
