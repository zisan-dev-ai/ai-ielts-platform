
function changeLangPref(val) {
    currentLangPref = val || 'both';
}
window.changeLangPref = changeLangPref;

function changeTargetBand(val) {
    currentTargetBand = parseFloat(val) || 7.5;
}
window.changeTargetBand = changeTargetBand;


function activatePlanItem(el, skill, topic) {
    syncDOM();
    document.querySelectorAll('.plan-item').forEach(function(item) {
        item.classList.remove('active');
    });
    if (el) el.classList.add('active');
    
    currentSkill = skill || 'Reading';
    currentSubTag = topic || 'True / False / Not Given';
    
    var displayLabel = currentSkill + ': ' + currentSubTag;
    if (currentSkillBadge) currentSkillBadge.textContent = displayLabel;
    
    switchModTab(null, currentSkill.toLowerCase());
    
    addStudentMsg('I want to start: ' + displayLabel);
    sendTeacherChat('Hello ARIA! Let us focus on ' + currentSkill + ' today: "' + currentSubTag + '". Break down the essential Band 9 Cambridge strategy and give me an authentic question to practice right now.');
}
window.activatePlanItem = activatePlanItem;

// ARIA IELTS AI Master Class — Unified Reliable Script (v250)

var currentSkill = 'General';
var currentSubTag = '';
var currentLangPref = 'both';
var voiceEnabled = true;
var micEnabled = false;
var recognition = null;
var teacherInitialized = false;
var globalSeqId = 0;
var audioCtx = null;
var callSeconds = 252;
var callTimerInterval = null;
var currentTargetBand = 7.5;
window.chatHistory = window.chatHistory || [];

var finalTranscript = '';
var isRecognizing = false;
var isSending = false;

var chatContainer, typingDots, voiceToggle, micToggle, mainChatInput, chatSendBtn, currentSkillBadge;

function syncDOM() {
    chatContainer     = document.getElementById('chat-messages') || document.getElementById('chat-container');
    typingDots        = document.getElementById('typing-indicator') || document.getElementById('typing-dots');
    voiceToggle       = document.getElementById('voice-toggle-btn') || document.getElementById('voice-toggle');
    micToggle         = document.getElementById('mic-toggle-btn') || document.getElementById('mic-toggle') || document.getElementById('mic-btn');
    mainChatInput     = document.getElementById('main-chat-input') || document.getElementById('chat-input') || document.getElementById('text-answer');
    chatSendBtn       = document.getElementById('chat-send-btn') || document.getElementById('send-btn') || document.getElementById('submit-btn');
    currentSkillBadge = document.getElementById('current-skill-badge') || document.getElementById('topic-label');
}

// ----------------------------------------------------
// UI & Mic Helpers
// ----------------------------------------------------
function updateMicUI(active) {
    micEnabled = active;
    var headerBtn = document.getElementById('mic-toggle-btn');
    var dockBtn = document.getElementById('mic-dock-btn');
    var banner = document.getElementById('listening-indicator');
    var box = document.getElementById('input-pill-box');

    if (headerBtn) headerBtn.classList.toggle('active', active);
    if (dockBtn) dockBtn.classList.toggle('recording-active', active);
    if (box) box.classList.toggle('recording-active', active);
    if (banner) banner.style.display = active ? 'flex' : 'none';
}
window.updateMicUI = updateMicUI;

function initSpeechRecognition() {
    window.SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!window.SpeechRecognition) return;

    try {
        if (recognition) {
            try { recognition.abort(); } catch(e) {}
        }
        recognition = new window.SpeechRecognition();
        recognition.continuous = true;
        recognition.interimResults = true;
        recognition.lang = (currentLangPref === 'mother') ? 'bn-BD' : 'en-US';

        recognition.onstart = function() {
            isRecognizing = true;
            updateMicUI(true);
        };

        recognition.onresult = function(event) {
            var interimTranscript = '';
            for (var i = event.resultIndex; i < event.results.length; ++i) {
                if (event.results[i].isFinal) {
                    finalTranscript += (finalTranscript ? ' ' : '') + event.results[i][0].transcript.trim();
                } else {
                    interimTranscript += event.results[i][0].transcript;
                }
            }
            if (mainChatInput) {
                var combined = (finalTranscript + (interimTranscript ? ' ' + interimTranscript : '')).trim();
                mainChatInput.value = combined;
                mainChatInput.style.height = 'auto';
                mainChatInput.style.height = Math.min(mainChatInput.scrollHeight, 100) + 'px';
            }
        };

        recognition.onerror = function(event) {
            console.warn("Speech recognition error:", event.error);
            if (event.error === 'not-allowed') {
                alert('Microphone access is blocked. Please allow microphone permission in your browser URL bar.');
                micEnabled = false;
                isRecognizing = false;
                updateMicUI(false);
            }
        };

        recognition.onend = function() {
            isRecognizing = false;
            if (micEnabled) {
                try {
                    recognition.lang = (currentLangPref === 'mother') ? 'bn-BD' : 'en-US';
                    recognition.start();
                } catch(e) {
                    micEnabled = false;
                    updateMicUI(false);
                }
            } else {
                updateMicUI(false);
            }
        };
    } catch(e) {
        console.error("SpeechRecognition init error:", e);
    }
}
window.initSpeechRecognition = initSpeechRecognition;

// ----------------------------------------------------
// Core Initialization
// ----------------------------------------------------
function initTeacher() {
    syncDOM();
    if (teacherInitialized) return;
    teacherInitialized = true;
    setTeacherVideoState(false);

    // Call Timer
    if (!callTimerInterval) {
        callTimerInterval = setInterval(function() {
            callSeconds++;
            var m = Math.floor(callSeconds / 60);
            var s = callSeconds % 60;
            var display = (m < 10 ? '0' + m : m) + ':' + (s < 10 ? '0' + s : s) + ' HD';
            var el = document.getElementById('call-timer-display');
            if (el) el.textContent = display;
        }, 1000);
    }

    // Band Select & Lang Setup
    setupBandSelects();

    // Audio Unlock gesture
    document.addEventListener('click', function unlockAudio() {
        try {
            if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
            if (audioCtx.state === 'suspended') audioCtx.resume();
        } catch(e) {}
    }, { once: true });

    // Initialize Speech Recognition
    initSpeechRecognition();

    // Button and keydown listeners
    if (chatSendBtn) {
        chatSendBtn.onclick = function(e) {
            e.preventDefault();
            sendMessage();
        };
    }

    // Sidebar question items click handler
    document.querySelectorAll('.qt-item').forEach(function(item) {
        item.addEventListener('click', function() {
            var skill = this.getAttribute('data-skill') || 'Reading';
            var qType = this.getAttribute('data-type') || this.textContent.trim();
            document.querySelectorAll('.qt-item').forEach(function(el) { el.classList.remove('active'); });
            this.classList.add('active');
            
            var welcomeHero = document.getElementById('welcome-hero');
            if (welcomeHero) welcomeHero.style.display = 'none';
            
            currentSkill = skill;
            currentSubTag = qType;
            if (currentSkillBadge) currentSkillBadge.textContent = skill + ': ' + qType;
            
            var prompt = "Hello ARIA, let's learn and practice IELTS " + skill + " — " + qType + ". Please coach me!";
            addStudentMsg(prompt);
            sendTeacherChat(prompt);
        });
    });

    var sidebarToggle = document.getElementById('sidebar-toggle');
    var qtSidebar = document.getElementById('qt-sidebar');
    if (sidebarToggle && qtSidebar) {
        sidebarToggle.addEventListener('click', function() {
            qtSidebar.classList.toggle('collapsed');
        });
    }

    if (mainChatInput) {
        mainChatInput.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                sendMessage();
            }
        });
        mainChatInput.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = Math.min(this.scrollHeight, 100) + 'px';
        });
    }

    // Check URL parameters for direct topic practice (e.g. from Grammar / Vocabulary Hub)
    var urlParams = new URLSearchParams(window.location.search);
    var reqSkill = urlParams.get('skill');
    var reqTopic = urlParams.get('topic');

    if (reqSkill && reqTopic) {
        var modKey = reqSkill.toLowerCase();
        if (modKey === 'vocab') modKey = 'vocabulary';
        switchModTab(null, modKey);

        currentSkill = reqSkill;
        currentSubTag = reqTopic;
        var displayLabel = currentSkill + ': ' + currentSubTag;
        if (currentSkillBadge) currentSkillBadge.textContent = displayLabel;

        setTimeout(function() {
            var matchingChip = null;
            document.querySelectorAll('#tab-' + modKey + ' .topic-chip').forEach(function(chip) {
                if (chip.textContent.toLowerCase().indexOf(reqTopic.toLowerCase()) >= 0) {
                    matchingChip = chip;
                }
            });
            if (matchingChip) {
                document.querySelectorAll('.topic-chip').forEach(function(c) { c.classList.remove('active'); });
                matchingChip.classList.add('active');
                try { matchingChip.scrollIntoView({ behavior: 'smooth', block: 'nearest' }); } catch(e) {}
            }

            addStudentMsg('I want to learn and practice ' + displayLabel);
            var customPrompt = '';
            if (currentSkill.toLowerCase() === 'grammar') {
                customPrompt = 'Hello ARIA, I want to learn and practice English Grammar: "' + currentSubTag + '". Please explain the core rules in simple, friendly words, highlight common exam traps, and give me a practice sentence to correct.';
            } else if (currentSkill.toLowerCase() === 'vocabulary') {
                customPrompt = 'Hello ARIA, I want to master IELTS Academic Vocabulary for the theme: "' + currentSubTag + '". Please teach me high-scoring words, collocations, and give me a sentence to upgrade with Band 8+ vocabulary.';
            } else {
                customPrompt = 'Hello ARIA, I want to learn and practice IELTS ' + currentSkill + ': "' + currentSubTag + '". Please teach me naturally and give me a practice question.';
            }
            sendTeacherChat(customPrompt);
        }, 500);
    } else {
        currentSkill = 'Reading';
        currentSubTag = 'True / False / Not Given';
        if (currentSkillBadge) currentSkillBadge.textContent = 'Reading: True / False / Not Given';
        switchModTab(null, 'reading');

        if (chatContainer && chatContainer.children.length === 0) {
            addTeacherMsg("Hello! I am **ARIA**, your IELTS Masterclass Examiner. 🎓\n\nWelcome to your full-screen private classroom! I know every Cambridge exam type and scoring rule inside out.\n\nSelect any topic from **Today's Teaching Plan** on the left, or ask me any question below to get started!", true);
        }
    }
}
window.initTeacher = initTeacher;

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initTeacher);
} else {
    initTeacher();
}

// ----------------------------------------------------
// Band & Language Selectors
// ----------------------------------------------------
function setupBandSelects() {
    var headerSelect = document.getElementById('header-target-band');
    var statusSelect = document.getElementById('band-select');
    var langSelect   = document.getElementById('lang-select');

    function onBandChange(newVal) {
        currentTargetBand = parseFloat(newVal);
        if (headerSelect) headerSelect.value = newVal;
        if (statusSelect) statusSelect.value = newVal;

        addSystemMsg('🎯 Target Band updated to Band ' + newVal + '. ARIA will now tailor all feedback for this goal.');

        fetch('/api/v1/user/update-band-profile', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ user_id: 1, target_band: currentTargetBand, current_level: 6.0 })
        }).then(function(r) { return r.json(); }).then(function(d) {
            console.log('Target Band score updated:', d);
        }).catch(function(e) {
            console.error('Band update error:', e);
        });
    }

    function onLangChange(newVal) {
        currentLangPref = newVal;
        var langDisplay = {'english':'🇬🇧 English Only','both':'🇧🇩 Banglish (Mixed)','mother':'বাংলা Only'};
        addSystemMsg('🌐 Language changed to ' + (langDisplay[newVal] || newVal) + '. ARIA will respond in this language.');
        if (recognition && isRecognizing) {
            try {
                recognition.lang = (newVal === 'mother') ? 'bn-BD' : 'en-US';
            } catch(e) {}
        }
    }

    if (headerSelect) {
        headerSelect.onchange = function() { onBandChange(this.value); };
    }
    if (statusSelect) {
        statusSelect.onchange = function() { onBandChange(this.value); };
    }
    if (langSelect) {
        langSelect.onchange = function() { onLangChange(this.value); };
    }
}
window.setupBandSelects = setupBandSelects;

function addSystemMsg(text) {
    syncDOM();
    var row = document.createElement('div');
    row.style.cssText = 'text-align:center; margin: 6px 0;';
    row.innerHTML = '<span style="background:rgba(99,102,241,0.15);border:1px solid rgba(99,102,241,0.3);color:#a5b4fc;font-size:0.75em;padding:4px 14px;border-radius:20px;display:inline-block;">' + text + '</span>';
    if (chatContainer) {
        chatContainer.appendChild(row);
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }
}
window.addSystemMsg = addSystemMsg;

// ----------------------------------------------------
// Video State Management
// ----------------------------------------------------
function setTeacherVideoState(isSpeaking, subtitleText) {
    var stage = document.getElementById('video-card-container') || document.querySelector('.video-card');
    var badge = document.getElementById('call-status-badge');
    var badgeText = document.getElementById('status-badge-text');
    var vid   = document.getElementById('teacher-video-player');
    var img   = document.getElementById('teacher-idle-img');
    
    if (isSpeaking) {
        if (stage) stage.classList.add('speaking-active');
        if (badge) badge.className = 'call-badge speaking';
        if (badgeText) badgeText.textContent = 'ARIA SPEAKING (LIVE)';
        if (img) img.style.display = 'none';
        if (vid) {
            vid.style.display = 'block';
            try { 
                vid.play().catch(function(){}); 
            } catch(e) {}
        }
    } else {
        if (stage) stage.classList.remove('speaking-active');
        if (badge) badge.className = 'call-badge';
        if (badgeText) badgeText.textContent = 'ARIA READY (STANDBY)';
        if (vid) {
            try { 
                vid.pause();
                vid.currentTime = 0;
            } catch(e) {}
            vid.style.display = 'none';
        }
        if (img) img.style.display = 'block';
    }
}
window.setTeacherVideoState = setTeacherVideoState;window.setTeacherVideoState = setTeacherVideoState;

function toggleTeacherFullscreen() {
    var stage = document.getElementById('video-stage-container');
    if (!stage) return;

    var isFs = stage.classList.contains('fullscreen-active') || document.fullscreenElement === stage;
    var icon = document.getElementById('fs-icon');
    var txt  = document.getElementById('fs-text');

    if (!isFs) {
        stage.classList.add('fullscreen-active');
        if (icon) icon.textContent = '✕';
        if (txt)  txt.textContent  = 'Exit Full Screen';
        if (stage.requestFullscreen) {
            stage.requestFullscreen().catch(function(){});
        }
    } else {
        stage.classList.remove('fullscreen-active');
        if (icon) icon.textContent = '⛶';
        if (txt)  txt.textContent  = 'Full Screen';
        if (document.fullscreenElement && document.exitFullscreen) {
            document.exitFullscreen().catch(function(){});
        }
    }
}
window.toggleTeacherFullscreen = toggleTeacherFullscreen;

function toggleVideoStage() {
    var stage = document.getElementById('video-stage-container');
    var arrow = document.getElementById('stage-toggle-arrow');
    if (!stage) return;
    stage.classList.toggle('collapsed-stage');
    if (arrow) {
        arrow.textContent = stage.classList.contains('collapsed-stage') ? '▼' : '▲';
    }
}
window.toggleVideoStage = toggleVideoStage;

document.addEventListener('fullscreenchange', function() {
    var stage = document.getElementById('video-stage-container');
    var icon = document.getElementById('fs-icon');
    var txt  = document.getElementById('fs-text');
    if (!document.fullscreenElement && stage) {
        stage.classList.remove('fullscreen-active');
        if (icon) icon.textContent = '⛶';
        if (txt)  txt.textContent  = 'Full Screen';
    }
});

document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        var stage = document.getElementById('video-stage-container');
        if (stage && stage.classList.contains('fullscreen-active')) {
            toggleTeacherFullscreen();
        }
    }
});

// ----------------------------------------------------
// Message Handling & Sending
// ----------------------------------------------------
function sendMessage() {
    syncDOM();
    var welcomeHero = document.getElementById('welcome-hero');
    if (welcomeHero) welcomeHero.style.display = 'none';
    if (!mainChatInput) return;
    var txt = mainChatInput.value.trim();
    if (!txt) return;

    if (micEnabled) {
        micEnabled = false;
        updateMicUI(false);
        if (recognition) {
            try { recognition.stop(); } catch(e) {}
        }
    }

    addStudentMsg(txt);
    mainChatInput.value = '';
    mainChatInput.style.height = 'auto';
    finalTranscript = '';
    sendTeacherChat(txt);
}
window.sendMessage = sendMessage;
window.handleSend = sendMessage;

function switchModTab(btn, modName) {
    document.querySelectorAll('.mod-tab-btn, .tab-btn').forEach(function(t) { t.classList.remove('active'); });
    var targetMod = (modName || 'reading').toLowerCase();
    
    if (btn) {
        btn.classList.add('active');
    } else {
        var match = document.querySelector('.mod-tab-btn[onclick*="' + targetMod + '"], .tab-btn[onclick*="' + targetMod + '"]');
        if (match) match.classList.add('active');
    }

    document.querySelectorAll('.mod-content').forEach(function(c) { c.style.display = 'none'; });
    var target = document.getElementById('tab-' + targetMod);
    if (target) target.style.display = 'block';
}
window.switchModTab = switchModTab;

function selectSyllabus(chipEl, skill, section, topic) {
    syncDOM();
    currentSkill = skill || 'Reading';
    currentSubTag = topic || 'True / False / Not Given';
    
    var displayLabel = skill + ': ' + currentSubTag;
    if (currentSkillBadge) currentSkillBadge.textContent = displayLabel;

    document.querySelectorAll('.topic-chip, .chip').forEach(function(c) { c.classList.remove('active'); });
    if (chipEl) {
        chipEl.classList.add('active');
    }

    var modKey = currentSkill.toLowerCase();
    if (modKey === 'vocab') modKey = 'vocabulary';
    switchModTab(null, modKey);

    addStudentMsg('I want to practice ' + displayLabel);

    var prompt = '';
    if (currentSkill.toLowerCase() === 'grammar') {
        prompt = 'Hello ARIA, let us learn and practice English Grammar: "' + currentSubTag + '". Please explain the core rules in simple, friendly words, highlight common exam traps, and give me a sentence to correct or practice.';
    } else if (currentSkill.toLowerCase() === 'vocabulary') {
        prompt = 'Hello ARIA, let us master IELTS Academic Vocabulary for the theme: "' + currentSubTag + '". Please teach me high-scoring words, collocations, and give me an essay sentence to upgrade with Band 8+ vocabulary.';
    } else {
        prompt = 'Hello ARIA, let us learn and practice "' + currentSubTag + '" for IELTS ' + currentSkill + '. Please teach me naturally and give me a question or cue card.';
    }

    sendTeacherChat(prompt);
}
window.selectSyllabus = selectSyllabus;

function filterSyllabus(query) {
    var q = (query || '').toLowerCase().trim();
    document.querySelectorAll('.topic-chip, .chip').forEach(function(c) {
        var match = !q || c.textContent.toLowerCase().indexOf(q) >= 0;
        c.style.display = match ? 'inline-block' : 'none';
    });
}
window.filterSyllabus = filterSyllabus;

function mdRender(str) {
    if (!str) return '';
    return str
        .replace(/^### (.+)$/gim, '<h3 style="font-weight:700;margin:6px 0 2px;">$1</h3>')
        .replace(/^## (.+)$/gim,  '<h2 style="font-weight:800;margin:8px 0 3px;">$1</h2>')
        .replace(/^# (.+)$/gim,   '<h1 style="font-weight:800;margin:10px 0 4px;">$1</h1>')
        .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
        .replace(/\*(.+?)\*/g,     '<em>$1</em>')
        .replace(/`(.+?)`/g,       '<code>$1</code>')
        .replace(/^&gt; (.+)$/gim, '<blockquote>$1</blockquote>')
        .replace(/\n/g, '<br>');
}
window.mdRender = mdRender;

function addStudentMsg(text) {
    syncDOM();
    var row = document.createElement('div');
    row.className = 'msg-row user';
    row.innerHTML = '<div class="msg-avatar user">You</div><div class="msg-bubble">' + mdRender(text) + '</div>';
    if (chatContainer) {
        chatContainer.appendChild(row);
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }
    window.chatHistory = window.chatHistory || [];
    window.chatHistory.push({ role: 'user', content: text });
}
window.addStudentMsg = addStudentMsg;

function addTeacherMsg(engText, skipVoice) {
    syncDOM();
    var eng = (engText || '').trim();
    var row = document.createElement('div');
    row.className = 'msg-row ai';
    
    row.innerHTML = '<div class="msg-avatar ai">AI</div>' +
        '<div class="msg-bubble">' + mdRender(eng) +
        '<div style="margin-top:8px;">' +
        '<button class="translate-bn-btn" onclick="translateMsg(this)">বাংলায় দেখো</button>' +
        '<button class="play-audio-btn" onclick="playBubbleAudio(this)">🔊 শুনুন</button>' +
        '<div class="bn-text-box"></div></div></div>';

    if (chatContainer) {
        chatContainer.appendChild(row);
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }
    window.chatHistory = window.chatHistory || [];
    window.chatHistory.push({ role: 'assistant', content: eng });

    if (voiceEnabled && !skipVoice && eng) speakTeacher(eng);
}
window.addTeacherMsg = addTeacherMsg;

function playBubbleAudio(btnEl) {
    if (!btnEl) return;
    var bubble = btnEl.closest('.msg-bubble');
    if (!bubble) return;
    var clone = bubble.cloneNode(true);
    clone.querySelectorAll('button, .bn-text-box').forEach(function(el) { el.remove(); });
    var text = clone.innerText.trim();
    if (text) speakTeacher(text);
}
window.playBubbleAudio = playBubbleAudio;

function translateMsg(btnEl) {
    if (!btnEl) return;
    var parent = btnEl.parentElement;
    var bnBox = parent.querySelector('.bn-text-box');
    if (!bnBox) return;

    if (bnBox.style.display === 'block') {
        bnBox.style.display = 'none';
        btnEl.textContent = 'বাংলায় দেখো';
        return;
    }

    if (bnBox.textContent.trim().length > 0) {
        bnBox.style.display = 'block';
        btnEl.textContent = 'লুকাও';
        return;
    }

    var bubble = btnEl.closest('.msg-bubble');
    var clone = bubble.cloneNode(true);
    clone.querySelectorAll('button, .bn-text-box').forEach(function(el) { el.remove(); });
    var rawText = clone.innerText.trim();

    btnEl.textContent = 'অনুবাদ হচ্ছে...';
    btnEl.disabled = true;

    fetch('/api/v1/ai/translate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: rawText.substring(0, 1000) })
    })
    .then(function(r) { return r.json(); })
    .then(function(d) {
        bnBox.textContent = d.translation || 'অনুবাদ পাওয়া যায়নি।';
        bnBox.style.display = 'block';
        btnEl.textContent = 'লুকাও';
        btnEl.disabled = false;
        if (chatContainer) chatContainer.scrollTop = chatContainer.scrollHeight;
    })
    .catch(function() {
        bnBox.textContent = 'অনুবাদ করতে সমস্যা হয়েছে।';
        bnBox.style.display = 'block';
        btnEl.textContent = 'আবার চেষ্টা করো';
        btnEl.disabled = false;
    });
}
window.translateMsg = translateMsg;

async function sendTeacherChat(text) {
    syncDOM();
    if (isSending) return;
    isSending = true;

    var row = document.createElement('div');
    row.className = 'msg-row ai';
    var bubble = document.createElement('div');
    bubble.className = 'msg-bubble';
    row.innerHTML = '<div class="msg-avatar ai">AI</div>';
    row.appendChild(bubble);

    if (chatContainer) {
        chatContainer.appendChild(row);
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }

    var full = '';
    try {
        var res = await fetch('/api/v1/ai/chat/stream', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                user_message: text,
                history: (window.chatHistory || []).slice(-10),
                context: { current_skill: currentSkill, current_topic: currentSubTag, target_band: currentTargetBand },
                lang_pref: currentLangPref
            })
        });

        if (!res.ok) throw new Error('HTTP ' + res.status);
        var reader = res.body.getReader();
        var decoder = new TextDecoder('utf-8');
        var buf = '';

        while (true) {
            var chunk = await reader.read();
            if (chunk.done) break;
            buf += decoder.decode(chunk.value, { stream: true });
            var lines = buf.split('\n\n');
            buf = lines.pop() || '';
            for (var i = 0; i < lines.length; i++) {
                var line = lines[i];
                if (!line.startsWith('data: ')) continue;
                var ds = line.slice(6).trim();
                if (ds === '[DONE]') break;
                try {
                    var obj = JSON.parse(ds);
                    if (obj.text) {
                        full += obj.text;
                        bubble.innerHTML = mdRender(full);
                        if (chatContainer) chatContainer.scrollTop = chatContainer.scrollHeight;
                    }
                } catch(e) {}
            }
        }

        bubble.innerHTML = mdRender(full) +
            '<div style="margin-top:8px;">' +
            '<button class="translate-bn-btn" onclick="translateMsg(this)">বাংলায় দেখো</button>' +
            '<button class="play-audio-btn" onclick="playBubbleAudio(this)">🔊 শুনুন</button>' +
            '<div class="bn-text-box"></div></div>';

        if (chatContainer) chatContainer.scrollTop = chatContainer.scrollHeight;
        window.chatHistory = window.chatHistory || [];
        window.chatHistory.push({ role: 'assistant', content: full });

        if (voiceEnabled && full) speakTeacher(full);

    } catch(e) {
        console.error("sendTeacherChat error:", e);
        var errText = full ? full : "Hello! I am ready to guide you step-by-step. Ask me anything or choose a topic on the left!";
        bubble.innerHTML = mdRender(errText) +
            '<div style="margin-top:8px;">' +
            '<button class="translate-bn-btn" onclick="translateMsg(this)">বাংলায় দেখো</button>' +
            '<button class="play-audio-btn" onclick="playBubbleAudio(this)">🔊 শুনুন</button>' +
            '<div class="bn-text-box"></div></div>';
        if (voiceEnabled && errText) speakTeacher(errText);
    } finally {
        isSending = false;
    }
}
window.sendTeacherChat = sendTeacherChat;

function sendQuickMessage(text) {
    syncDOM();
    addStudentMsg(text);
    sendTeacherChat(text);
}
window.sendQuickMessage = sendQuickMessage;

function toggleVoice() {
    syncDOM();
    voiceEnabled = !voiceEnabled;
    if (voiceToggle) voiceToggle.classList.toggle('active', voiceEnabled);
    if (!voiceEnabled) {
        globalSeqId++;
        setTeacherVideoState(false);
        if (typeof window !== 'undefined' && window.speechSynthesis) {
            try { window.speechSynthesis.cancel(); } catch(e) {}
        }
        var player = document.getElementById('aria-audio-player') || audioPlayer;
        try { player.pause(); } catch(e) {}
    }
}
window.toggleVoice = toggleVoice;

function toggleMic() {
    syncDOM();
    if (!recognition) {
        initSpeechRecognition();
    }
    if (!recognition) {
        alert('Voice recognition is not supported in this browser. Please use Google Chrome or Microsoft Edge.');
        return;
    }

    if (micEnabled) {
        micEnabled = false;
        updateMicUI(false);
        try { recognition.stop(); } catch(e) {}
        if (mainChatInput && mainChatInput.value.trim()) {
            mainChatInput.focus();
        }
    } else {
        if (typeof window !== 'undefined' && window.speechSynthesis) {
            try { window.speechSynthesis.cancel(); } catch(e) {}
        }
        var player = document.getElementById('aria-audio-player') || audioPlayer;
        try { player.pause(); } catch(e) {}
        setTeacherVideoState(false);

        finalTranscript = mainChatInput ? mainChatInput.value.trim() : '';
        micEnabled = true;
        updateMicUI(true);

        try {
            recognition.lang = (currentLangPref === 'mother') ? 'bn-BD' : 'en-US';
            recognition.start();
        } catch(e) {
            console.log("Recognition start info:", e);
        }
    }
}
window.toggleMic = toggleMic;

// ----------------------------------------------------
// Text to Speech (TTS) & Audio Playback
// ----------------------------------------------------
var FEMALE_NAMES = ['zira','samantha','karen','moira','tessa','fiona','victoria','aria','jenny','google us english','natural'];
var cachedVoices = [];

function loadVoices() {
    try {
        cachedVoices = window.speechSynthesis ? (window.speechSynthesis.getVoices() || []) : [];
    } catch(e) {}
}

if (typeof window !== 'undefined' && window.speechSynthesis) {
    loadVoices();
    if (window.speechSynthesis.onvoiceschanged !== undefined) {
        window.speechSynthesis.onvoiceschanged = loadVoices;
    }
}

var audioPlayer = new Audio();
var currentAudioQueue = null;

function speakTeacher(rawText) {
    if (!voiceEnabled) return;

    if (typeof window !== 'undefined' && window.speechSynthesis) {
        try { window.speechSynthesis.cancel(); } catch(e) {}
    }
    
    var player = document.getElementById('aria-audio-player') || audioPlayer;
    try { player.pause(); player.currentTime = 0; } catch(e) {}
    setTeacherVideoState(false);

    var clean = (rawText || '').replace(/[*_`#>-]/g, '').replace(/<[^>]*>/g, '').trim();
    if (!clean) return;

    // Split text into natural paragraphs/thoughts first
    var rawParas = clean.split(/\n+/).map(function(p) { return p.trim(); }).filter(function(p) { return p.length > 2; });
    if (rawParas.length === 0) rawParas = [clean];

    var chunks = [];
    for (var p = 0; p < rawParas.length; p++) {
        var para = rawParas[p];
        if (para.length <= 220) {
            chunks.push(para);
        } else {
            // Split long paragraph into natural sentences
            var sentences = para.split(/(?<=[.!?])\s+/).filter(function(s) { return s.trim().length > 2; });
            var cur = '';
            for (var s = 0; s < sentences.length; s++) {
                var sent = sentences[s].trim();
                if (cur && (cur + ' ' + sent).length > 200) {
                    chunks.push(cur.trim());
                    cur = sent;
                } else {
                    cur += (cur ? ' ' : '') + sent;
                }
            }
            if (cur) chunks.push(cur.trim());
        }
    }

    if (chunks.length === 0) return;

    var forceBnVoice = (currentLangPref === 'both' || currentLangPref === 'mother');
    var queueId = Date.now();
    
    currentAudioQueue = {
        id: queueId,
        chunks: chunks,
        index: 0,
        player: player,
        forceBn: forceBnVoice,
        audioPromises: {}
    };

    // Preload first 2 chunks immediately
    getChunkAudioPromise(currentAudioQueue, 0);
    if (chunks.length > 1) {
        getChunkAudioPromise(currentAudioQueue, 1);
    }

    playNextQueueChunk(currentAudioQueue);
}
window.speakTeacher = speakTeacher;

function getChunkAudioPromise(queue, idx) {
    if (!queue || idx >= queue.chunks.length) return Promise.resolve('');
    if (queue.audioPromises[idx]) return queue.audioPromises[idx];

    var chunkText = queue.chunks[idx];
    var isBn = queue.forceBn || /[\u0980-\u09FF]/.test(chunkText);

    queue.audioPromises[idx] = fetch('/api/v1/ai/tts', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
            text: chunkText, 
            lang_pref: queue.forceBn ? 'bn' : (isBn ? 'bn' : 'en') 
        })
    })
    .then(function(res) { return res.json(); })
    .then(function(data) {
        return data.audio_url || '';
    })
    .catch(function(err) {
        console.warn('TTS error on chunk ' + idx + ':', err);
        return '';
    });

    return queue.audioPromises[idx];
}

function playNextQueueChunk(queue) {
    if (!queue || !voiceEnabled || !currentAudioQueue || queue.id !== currentAudioQueue.id || queue.index >= queue.chunks.length) {
        setTeacherVideoState(false);
        return;
    }

    var idx = queue.index;
    var player = queue.player;

    // While waiting for audio, video stays paused and smiling
    setTeacherVideoState(false);

    // Preload next chunk in advance
    if (idx + 1 < queue.chunks.length) {
        getChunkAudioPromise(queue, idx + 1);
    }

    // Await this chunk's audio - guaranteed never skipped!
    getChunkAudioPromise(queue, idx).then(function(audioUrl) {
        if (!queue || !voiceEnabled || !currentAudioQueue || queue.id !== currentAudioQueue.id) {
            setTeacherVideoState(false);
            return;
        }

        if (!audioUrl) {
            console.warn('Audio URL missing for chunk', idx, 'skipping to next');
            queue.index++;
            playNextQueueChunk(queue);
            return;
        }

        player.src = audioUrl;
        player.volume = 1.0;

        player.onended = function() {
            // Audio finished for this paragraph -> IMMEDIATELY PAUSE VIDEO & SHOW SMILING ARIA
            setTeacherVideoState(false);

            if (!currentAudioQueue || queue.id !== currentAudioQueue.id) return;
            queue.index++;

            if (queue.index < queue.chunks.length) {
                // Exact 1-second (1000ms) break between paragraphs with smiling paused video
                setTimeout(function() {
                    if (currentAudioQueue && queue.id === currentAudioQueue.id) {
                        playNextQueueChunk(queue);
                    }
                }, 1000);
            } else {
                setTeacherVideoState(false);
            }
        };

        player.onerror = function(err) {
            console.warn('Audio play error on chunk', idx, err);
            setTeacherVideoState(false);
            if (!currentAudioQueue || queue.id !== currentAudioQueue.id) return;
            queue.index++;
            setTimeout(function() { playNextQueueChunk(queue); }, 200);
        };

        var playPromise = player.play();
        if (playPromise !== undefined) {
            playPromise.then(function() {
                // Video ONLY plays when audio has ACTUALLY started outputting sound
                if (currentAudioQueue && queue.id === currentAudioQueue.id) {
                    setTeacherVideoState(true, queue.chunks[idx]);
                }
            }).catch(function(err) {
                console.warn('Audio play exception:', err);
                setTeacherVideoState(false);
                queue.index++;
                setTimeout(function() { playNextQueueChunk(queue); }, 300);
            });
        }
    });
}

// ----------------------------------------------------
// Quick Skill & Message Helpers
// ----------------------------------------------------
function startQuickSkill(skillName) {
    syncDOM();
    currentSkill = skillName;
    if (currentSkillBadge) currentSkillBadge.textContent = skillName + ': Master Class';
    var topicLabel = document.getElementById('topic-label');
    if (topicLabel) topicLabel.textContent = skillName + ' — 1-on-1 Master Class';
    
    var welcomeHero = document.getElementById('welcome-hero');
    if (welcomeHero) welcomeHero.style.display = 'none';
    
    var prompt = '';
    if (skillName.toLowerCase() === 'speaking') {
        prompt = "Hello ARIA, I want to practice IELTS Speaking Part 3 discussion. Please ask me a thought-provoking question!";
    } else if (skillName.toLowerCase() === 'writing') {
        prompt = "Hello ARIA, I want to practice IELTS Writing. Give me an essay prompt to write and evaluate!";
    } else if (skillName.toLowerCase() === 'listening') {
        prompt = "Hello ARIA, let's practice IELTS Listening strategies and question types!";
    } else {
        prompt = "Hello ARIA, I want to master IELTS Reading! Teach me the core strategies.";
    }
    addStudentMsg(prompt);
    sendTeacherChat(prompt);
}
window.startQuickSkill = startQuickSkill;

function sendQuickMsg(text) {
    syncDOM();
    var welcomeHero = document.getElementById('welcome-hero');
    if (welcomeHero) welcomeHero.style.display = 'none';
    sendQuickMessage(text);
}
window.sendQuickMsg = sendQuickMsg;

// Ensure Teacher Video is initially OFF (showing the idle photo on load)
document.addEventListener('DOMContentLoaded', function() {
    setTeacherVideoState(false);
});
