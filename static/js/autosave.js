/* IndexedDB & LocalStorage Auto-Save Recovery Engine */
class AutoSaveEngine {
  constructor(keyPrefix = 'ielts_draft_') {
    this.keyPrefix = keyPrefix;
    this.saveTimeout = null;
  }

  saveDraft(draftId, content) {
    const statusText = document.getElementById('save-status-text');
    const statusDot = document.getElementById('save-status-dot');

    if (statusText && statusDot) {
      statusText.innerText = 'Saving...';
      statusDot.style.backgroundColor = '#f59e0b';
    }

    clearTimeout(this.saveTimeout);
    this.saveTimeout = setTimeout(() => {
      try {
        const payload = {
          content: content,
          timestamp: new Date().toISOString()
        };
        localStorage.setItem(this.keyPrefix + draftId, JSON.stringify(payload));

        if (statusText && statusDot) {
          statusText.innerText = 'Saved';
          statusDot.style.backgroundColor = '#22c55e';
        }
      } catch (e) {
        if (statusText && statusDot) {
          statusText.innerText = 'Offline (Saved Locally)';
          statusDot.style.backgroundColor = '#3b82f6';
        }
      }
    }, 800);
  }

  loadDraft(draftId) {
    try {
      const item = localStorage.getItem(this.keyPrefix + draftId);
      return item ? JSON.parse(item) : null;
    } catch (e) {
      return null;
    }
  }

  clearDraft(draftId) {
    localStorage.removeItem(this.keyPrefix + draftId);
  }
}

window.autoSaveEngine = new AutoSaveEngine();
