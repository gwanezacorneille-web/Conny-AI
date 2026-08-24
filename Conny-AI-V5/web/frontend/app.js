
// ============================================================
// CONNY V12 SESSION ID
// Each browser gets its own persistent session identifier.
// ============================================================

function getConnySessionId() {
    let id = localStorage.getItem("conny_session_id");

    if (!id) {
        if (window.crypto && crypto.randomUUID) {
            id = crypto.randomUUID();
        } else {
            id = "conny-" + Date.now() + "-" + Math.random().toString(36).slice(2);
        }

        localStorage.setItem("conny_session_id", id);
    }

    return id;
}

const CONNY_SESSION_ID = getConnySessionId();

// ============================================================
// CONNY V12 CHAT SESSION HEADER
// Automatically attaches the session ID to chat requests.
// ============================================================

const CONNY_ORIGINAL_FETCH = window.fetch;

window.fetch = function(input, init = {}) {
    const url = typeof input === "string"
        ? input
        : (input && input.url ? input.url : "");

    if (url.includes("/api/chat")) {
        const headers = new Headers(init.headers || {});

        headers.set("X-Session-ID", CONNY_SESSION_ID);

        init = {
            ...init,
            headers
        };
    }

    return CONNY_ORIGINAL_FETCH.call(window, input, init);
};

const chat = document.getElementById("chat");
const input = document.getElementById("messageInput");
const sendButton = document.getElementById("sendButton");

const API_URL = "/api/chat";

/* =========================================================
   CONNY VOICE V1
   Browser Speech Synthesis layer
   ========================================================= */

const voice = {
    enabled: true,
    speaking: false,
    rate: 1.0,
    pitch: 1.0,
    volume: 1.0,
    preferredVoice: null
};


function loadConnyVoice() {

    if (!("speechSynthesis" in window)) {

        console.warn("CONNY VOICE: Speech synthesis is not supported.");

        voice.enabled = false;

        return;
    }

    const voices = window.speechSynthesis.getVoices();

    if (!voices.length) {
        return;
    }

    /*
     * Prefer an English voice.
     * We deliberately do not hard-code a platform-specific
     * voice name so CONNY remains cross-platform.
     */

    voice.preferredVoice =
        voices.find(v => /^en/i.test(v.lang)) ||
        voices[0];
}


function speakConny(text) {

    if (!voice.enabled) {
        return;
    }

    if (!("speechSynthesis" in window)) {
        return;
    }

    if (!text || !text.trim()) {
        return;
    }

    window.speechSynthesis.cancel();

    const utterance = new SpeechSynthesisUtterance(text);

    utterance.rate = voice.rate;
    utterance.pitch = voice.pitch;
    utterance.volume = voice.volume;

    if (voice.preferredVoice) {
        utterance.voice = voice.preferredVoice;
    }

    utterance.onstart = function() {

        voice.speaking = true;

        document.body.classList.add("conny-speaking");

        if (typeof setRepresenterState === "function") {
            setRepresenterState("speaking");
        }

        console.log("CONNY VOICE: speaking");
    };


    utterance.onend = function() {

        voice.speaking = false;

        document.body.classList.remove("conny-speaking");

        if (typeof setRepresenterState === "function") {
            setRepresenterState("idle");
        }

        console.log("CONNY VOICE: finished");
    };


    utterance.onerror = function(event) {

        voice.speaking = false;

        document.body.classList.remove("conny-speaking");

        if (typeof setRepresenterState === "function") {
            setRepresenterState("idle");
        }

        console.warn(
            "CONNY VOICE ERROR:",
            event.error
        );
    };


    window.speechSynthesis.speak(utterance);
}


if ("speechSynthesis" in window) {

    loadConnyVoice();

    window.speechSynthesis.onvoiceschanged =
        loadConnyVoice;

}



function addMessage(sender, text, intent = null, decision = null) {

    const message = document.createElement("div");

    message.className = `message ${sender}`;

    const bubble = document.createElement("div");

    bubble.className = "message-bubble";

    bubble.textContent = text;

    message.appendChild(bubble);

    if (sender === "conny" && (intent || decision)) {

        const meta = document.createElement("div");

        meta.className = "message-meta";

        const parts = [];

        if (intent) {
            parts.push(`intent: ${intent}`);
        }

        if (decision) {
            parts.push(`decision: ${decision}`);
        }

        meta.textContent = parts.join(" • ");

        bubble.appendChild(meta);
    }

    chat.appendChild(message);

    chat.scrollTop = chat.scrollHeight;
}


function setLoading(loading) {

    sendButton.disabled = loading;
    input.disabled = loading;

    if (loading) {
        sendButton.textContent = "…";
    } else {
        sendButton.textContent = "➤";
    }
}


async function sendMessage() {

    const message = input.value.trim();

    if (!message) {
        return;
    }

    addMessage("user", message);

    input.value = "";

    setLoading(true);

    if (typeof setRepresenterState === "function") {
        setRepresenterState("thinking");
    }

    try {

        const response = await fetch(API_URL, {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                message: message
            })

        });


        if (!response.ok) {

            throw new Error(
                `Server returned HTTP ${response.status}`
            );

        }


        const data = await response.json();


        const connyResponse =
            data.response || "I didn't receive a response.";

        if (typeof setRepresenterState === "function") {
            setRepresenterState("responding");
        }

        addMessage(
            "conny",
            connyResponse
        );

        speakConny(connyResponse);


    } catch (error) {

        console.error("CONNY API ERROR:", error);

        addMessage(
            "conny",
            "I couldn't connect to my brain. Please try again."
        );

    } finally {

        setLoading(false);

        input.focus();

    }
}


sendButton.addEventListener(
    "click",
    sendMessage
);


input.addEventListener(
    "keydown",
    function(event) {

        if (
            event.key === "Enter" &&
            !event.shiftKey
        ) {

            event.preventDefault();

            sendMessage();

        }

    }
);


input.focus();



/* =========================================================
   CONNY AI CHAT CONTROLS
   ========================================================= */

const newChatButton = document.getElementById("newChatButton");
const chatContainer = document.getElementById("chat");

function startNewChat() {

    if (!chatContainer) {
        return;
    }

    chatContainer.innerHTML = `
        <div class="welcome">

            <img
                class="welcome-representer"
                src="/frontend/representer/conny-representer.png"
                alt="CONNY AI representer"
            >

            <p>
                All primary systems are online.
            </p>

            <p>
                Hello. I'm CONNY.
            </p>

            <div class="watermark">
                <strong>CONNY AI</strong>
                <span>powered by Gwaneza Corneille Karenzi</span>
            </div>

        </div>
    `;

    if (input) {
        input.value = "";
        input.focus();
    }

}

if (newChatButton) {

    newChatButton.addEventListener(
        "click",
        startNewChat
    );

}


/* =========================================================
   CONNY AI INFORMATION PANEL
   ========================================================= */



const infoButton = document.getElementById("infoButton");
const infoOverlay = document.getElementById("infoOverlay");
const closeInfoButton = document.getElementById("closeInfoButton");


function openConnyInfo() {

    if (!infoOverlay) {
        return;
    }

    infoOverlay.classList.add("active");

    infoOverlay.setAttribute(
        "aria-hidden",
        "false"
    );

    document.body.classList.add("info-open");
}


function closeConnyInfo() {

    if (!infoOverlay) {
        return;
    }

    infoOverlay.classList.remove("active");

    infoOverlay.setAttribute(
        "aria-hidden",
        "true"
    );

    document.body.classList.remove("info-open");
}


if (infoButton) {

    infoButton.addEventListener(
        "click",
        openConnyInfo
    );

}


if (closeInfoButton) {

    closeInfoButton.addEventListener(
        "click",
        closeConnyInfo
    );

}


if (infoOverlay) {

    infoOverlay.addEventListener(
        "click",
        function(event) {

            if (event.target === infoOverlay) {

                closeConnyInfo();

            }

        }
    );

}


document.addEventListener(
    "keydown",
    function(event) {

        if (
            event.key === "Escape" &&
            infoOverlay &&
            infoOverlay.classList.contains("active")
        ) {

            closeConnyInfo();

        }

    }
);


/* =========================================================
   CONNY VOICE INPUT V1
   Browser Speech Recognition
   ========================================================= */

const micButton = document.getElementById("micButton");

let recognition = null;
let isListening = false;


/*
 * Browser compatibility
 *
 * Chrome / Edge commonly expose:
 *   SpeechRecognition
 *
 * Some browsers expose:
 *   webkitSpeechRecognition
 */

const SpeechRecognition =
    window.SpeechRecognition ||
    window.webkitSpeechRecognition;


if (micButton && SpeechRecognition) {

    recognition = new SpeechRecognition();

    recognition.continuous = false;
    recognition.interimResults = true;
    recognition.lang = "en-US";


    recognition.onstart = function() {

        isListening = true;

        micButton.classList.add("listening");

        if (typeof setRepresenterState === "function") {
            setRepresenterState("listening");
        }

        micButton.textContent = "🔴";

        micButton.setAttribute(
            "aria-label",
            "Stop voice input"
        );

        micButton.setAttribute(
            "title",
            "Listening..."
        );

    };


    recognition.onresult = function(event) {

        let transcript = "";

        for (
            let i = event.resultIndex;
            i < event.results.length;
            i++
        ) {

            transcript +=
                event.results[i][0].transcript;

        }

        transcript = transcript.trim();

        if (transcript) {

            input.value = transcript;

        }

    };


    recognition.onerror = function(event) {

        console.error(
            "CONNY VOICE INPUT ERROR:",
            event.error
        );

    };


    recognition.onend = function() {

        isListening = false;

        micButton.classList.remove("listening");

        if (typeof setRepresenterState === "function") {
            setRepresenterState("idle");
        }

        micButton.textContent = "🎙";

        micButton.setAttribute(
            "aria-label",
            "Voice input"
        );

        micButton.setAttribute(
            "title",
            "Voice input"
        );

        input.focus();

    };


    micButton.addEventListener(
        "click",
        function() {

            if (isListening) {

                recognition.stop();

                return;

            }

            try {

                recognition.start();

            } catch (error) {

                console.error(
                    "CONNY VOICE START ERROR:",
                    error
                );

            }

        }
    );

}
else if (micButton) {

    micButton.disabled = true;

    micButton.title =
        "Voice input is not supported by this browser";

    console.warn(
        "CONNY: Speech Recognition is not supported."
    );

}


/* =========================================================
   CONNY REPRESENTer V2
   State Engine
   ========================================================= */

const connyRepresenter =
    document.querySelector(".welcome-representer");


const connyRepresenterState = {
    current: "idle"
};


function setRepresenterState(state) {

    if (!connyRepresenter) {
        return;
    }

    const allowedStates = [
        "idle",
        "listening",
        "thinking",
        "responding",
        "speaking"
    ];

    if (!allowedStates.includes(state)) {
        console.warn(
            "CONNY REPRESENTer: Unknown state:",
            state
        );

        return;
    }


    connyRepresenterState.current = state;


    connyRepresenter.dataset.state = state;


    connyRepresenter.classList.remove(
        "state-idle",
        "state-listening",
        "state-thinking",
        "state-responding",
        "state-speaking"
    );


    connyRepresenter.classList.add(
        `state-${state}`
    );


    console.log(
        `CONNY REPRESENTer STATE: ${state.toUpperCase()}`
    );
}


/*
 * Initial state
 */

setRepresenterState("idle");
