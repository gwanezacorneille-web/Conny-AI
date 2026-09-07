const API_BASE = window.CONNY_V14_API || "";

let token = localStorage.getItem("conny_v14_token") || "";

const auth = document.getElementById("auth");
const chatApp = document.getElementById("chatApp");
const authStatus = document.getElementById("authStatus");
const identity = document.getElementById("identity");
const chat = document.getElementById("chat");

function setStatus(text) {
    authStatus.textContent = text;
}

async function api(path, options = {}) {
    const headers = {
        "Content-Type": "application/json",
        ...(options.headers || {})
    };

    if (token) {
        headers.Authorization = `Bearer ${token}`;
    }

    const response = await fetch(API_BASE + path, {
        ...options,
        headers
    });

    let data = {};

    try {
        data = await response.json();
    } catch (_) {}

    if (!response.ok) {
        throw new Error(data.detail || data.message || "Request failed");
    }

    return data;
}

function enterApp(data) {
    token = data.token;
    localStorage.setItem("conny_v14_token", token);

    auth.style.display = "none";
    chatApp.style.display = "block";

    identity.textContent =
        `${data.username} — ${data.account_type}`;
}

async function registerAccount() {
    try {
        const data = await api("/auth/register", {
            method: "POST",
            body: JSON.stringify({
                username: document.getElementById("username").value,
                password: document.getElementById("password").value
            })
        });

        enterApp(data);
    } catch (error) {
        setStatus(error.message);
    }
}

async function login() {
    try {
        const data = await api("/auth/login", {
            method: "POST",
            body: JSON.stringify({
                username: document.getElementById("username").value,
                password: document.getElementById("password").value,
                account_type: "private"
            })
        });

        enterApp(data);
    } catch (error) {
        setStatus(error.message);
    }
}

async function guestLogin() {
    try {
        const data = await api("/auth/guest", {
            method: "POST"
        });

        enterApp(data);
    } catch (error) {
        setStatus(error.message);
    }
}

async function logout() {
    try {
        await api("/auth/logout", {
            method: "POST"
        });
    } catch (_) {}

    token = "";
    localStorage.removeItem("conny_v14_token");

    chatApp.style.display = "none";
    auth.style.display = "block";
}

async function restoreSession() {
    if (!token) {
        return;
    }

    try {
        const data = await api("/auth/session");
        enterApp(data);
    } catch (_) {
        token = "";
        localStorage.removeItem("conny_v14_token");
    }
}

async function sendMessage() {
    const input = document.getElementById("message");
    const message = input.value.trim();

    if (!message) {
        return;
    }

    chat.innerHTML += `<p><b>You:</b> ${escapeHtml(message)}</p>`;
    input.value = "";

    /*
     * Authentication is now attached to the V14 request.
     * The V14 chat gateway can be connected to the existing
     * V13 intelligence adapter without modifying the V13 freeze.
     */
    try {
        const response = await api("/api/chat", {
            method: "POST",
            body: JSON.stringify({
                message
            })
        });

        chat.innerHTML +=
            `<p><b>CONNY:</b> ${escapeHtml(response.response || "")}</p>`;
    } catch (error) {
        chat.innerHTML +=
            `<p><b>CONNY:</b> ${escapeHtml(error.message)}</p>`;
    }
}

function escapeHtml(value) {
    return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}

restoreSession();
