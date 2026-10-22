
const chatForm = document.getElementById("chatForm");
const questionInput = document.getElementById("questionInput");
const messages = document.getElementById("messages");
const welcomeScreen = document.getElementById("welcomeScreen");
const sendBtn = document.getElementById("sendBtn");
const newChatBtn = document.getElementById("newChatBtn");

// Automatically resize the question input as the user types.
questionInput.addEventListener("input", () => {
    questionInput.style.height = "auto";
    questionInput.style.height =
        Math.min(questionInput.scrollHeight, 150) + "px";
});

// Create a chat message safely using textContent.
function addMessage(role, text) {
    const message = document.createElement("div");
    message.className = `message ${role}`;

    const avatar = document.createElement("div");
    avatar.className = "message-avatar";
    avatar.textContent = role === "user" ? "YOU" : "AI";

    const content = document.createElement("div");
    content.className = "message-content";

    const label = document.createElement("div");
    label.className = "message-label";
    label.textContent = role === "user" ? "YOU" : "PDF ASSISTANT";

    const bubble = document.createElement("div");
    bubble.className = "message-bubble";
    bubble.textContent = text;

    content.append(label, bubble);
    message.append(avatar, content);
    messages.appendChild(message);

    return { message, content, bubble };
}

// Display the source passages returned by Flask.
function addSources(content, sources) {
    if (!Array.isArray(sources) || sources.length === 0) {
        return;
    }

    const sourceContainer = document.createElement("div");
    sourceContainer.className = "sources";

    sources.forEach((source, index) => {
        const chip = document.createElement("div");
        chip.className = "source-chip";

        const details = document.createElement("details");
        const summary = document.createElement("summary");

        summary.textContent = `Source ${index + 1} · Page ${source.page}`;

        const excerpt = document.createElement("p");
        excerpt.textContent = source.text;

        details.append(summary, excerpt);
        chip.appendChild(details);
        sourceContainer.appendChild(chip);
    });

    content.appendChild(sourceContainer);
}

// Send a question to the Flask backend.
async function sendQuestion(question) {
    const cleanedQuestion = question.trim();

    if (!cleanedQuestion) {
        return;
    }

    welcomeScreen.style.display = "none";
    addMessage("user", cleanedQuestion);

    questionInput.value = "";
    questionInput.style.height = "auto";
    sendBtn.disabled = true;

    const loading = addMessage("assistant", "Thinking...");
    loading.bubble.classList.add("typing");

    try {
        const response = await fetch("/api/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                question: cleanedQuestion
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "The request failed.");
        }

        loading.bubble.classList.remove("typing");
        loading.bubble.textContent = data.answer || "No answer was returned.";

        addSources(loading.content, data.sources);

    } catch (error) {
        loading.bubble.classList.remove("typing");
        loading.bubble.textContent =
            `Sorry, something went wrong: ${error.message}`;

        console.error("Chat request failed:", error);

    } finally {
        sendBtn.disabled = false;
        questionInput.focus();
        messages.scrollIntoView({
            behavior: "smooth",
            block: "end"
        });
    }
}

// Handle the form submission.
chatForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    if (sendBtn.disabled) {
        return;
    }

    await sendQuestion(questionInput.value);
});

// Make suggested questions clickable.
document.querySelectorAll(".suggestion-card").forEach((button) => {
    button.addEventListener("click", () => {
        sendQuestion(button.dataset.question);
    });
});

// Reset the visible conversation.
newChatBtn.addEventListener("click", () => {
    messages.replaceChildren();
    welcomeScreen.style.display = "";
    questionInput.value = "";
    questionInput.style.height = "auto";
    questionInput.focus();
});


const uploadForm = document.getElementById("uploadForm");
const pdfFileInput = document.getElementById("pdfFile");
const uploadBtn = document.getElementById("uploadBtn");
const uploadStatus = document.getElementById("uploadStatus");
const documentCard = document.getElementById("documentCard");

pdfFileInput.addEventListener("change", () => {
    const file = pdfFileInput.files[0];

    if (file) {
        uploadStatus.className = "upload-status";
        uploadStatus.textContent = `Selected: ${file.name}`;
    }
});

uploadForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const file = pdfFileInput.files[0];

    if (!file) {
        uploadStatus.className = "upload-status error";
        uploadStatus.textContent = "Please select a PDF first.";
        return;
    }

    if (
        !file.name.toLowerCase().endsWith(".pdf") ||
        file.size > 15 * 1024 * 1024
    ) {
        uploadStatus.className = "upload-status error";
        uploadStatus.textContent =
            "Choose a PDF file no larger than 15 MB.";
        return;
    }

    const formData = new FormData();
    formData.append("file", file);

    uploadBtn.disabled = true;
    uploadBtn.textContent = "Indexing PDF...";
    uploadStatus.className = "upload-status";
    uploadStatus.textContent =
        "Extracting text and creating embeddings. This may take a moment.";

    try {
        const response = await fetch("/api/upload", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Upload failed.");
        }

        uploadStatus.className = "upload-status success";
        uploadStatus.textContent =
            `Indexed ${data.filename}: ${data.pages} pages, ` +
            `${data.chunks} chunks.`;

        documentCard.querySelector(".document-info strong").textContent =
            data.filename;

        documentCard.querySelector(".document-info span").textContent =
            `${data.pages} pages · ${data.chunks} chunks`;

        pdfFileInput.value = "";

    } catch (error) {
        uploadStatus.className = "upload-status error";
        uploadStatus.textContent = error.message;
        console.error("PDF upload failed:", error);

    } finally {
        uploadBtn.disabled = false;
        uploadBtn.textContent = "Add to knowledge base";
    }
});
