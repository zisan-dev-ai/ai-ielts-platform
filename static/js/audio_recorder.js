/* WebAudio & MediaRecorder Speaking Recording Engine */
class SpeakingAudioRecorder {
  constructor() {
    this.mediaRecorder = null;
    this.audioChunks = [];
    this.recordingTimer = null;
    this.secondsRecorded = 0;
    this.audioBlob = null;
  }

  async startRecording(onTickCallback) {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      this.mediaRecorder = new MediaRecorder(stream);
      this.audioChunks = [];
      this.secondsRecorded = 0;

      this.mediaRecorder.ondataavailable = (e) => {
        if (e.data.size > 0) {
          this.audioChunks.push(e.data);
        }
      };

      this.mediaRecorder.start();

      this.recordingTimer = setInterval(() => {
        this.secondsRecorded++;
        if (onTickCallback) onTickCallback(this.secondsRecorded);
      }, 1000);

      return true;
    } catch (err) {
      alert("Microphone permission required for IELTS Speaking practice.");
      return false;
    }
  }

  stopRecording() {
    return new Promise((resolve) => {
      if (!this.mediaRecorder) return resolve(null);

      clearInterval(this.recordingTimer);

      this.mediaRecorder.onstop = () => {
        this.audioBlob = new Blob(this.audioChunks, { type: 'audio/wav' });
        const audioUrl = URL.createObjectURL(this.audioBlob);
        resolve({ blob: this.audioBlob, audioUrl: audioUrl, duration: this.secondsRecorded });
      };

      this.mediaRecorder.stop();
    });
  }
}

window.speakingAudioRecorder = new SpeakingAudioRecorder();
