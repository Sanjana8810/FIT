const sendButton = document.getElementById("send-btn");
const userInput = document.getElementById("user-input");
const chatBox = document.getElementById("chat-box");

function addMessage(message, className) {
    const div = document.createElement("div");
    div.className = className;
    div.textContent = message;
    chatBox.appendChild(div);
    chatBox.scrollTop = chatBox.scrollHeight;
}

async function sendMessage() {
    const message = userInput.value.trim();

    if (message === "") {
        return;
    }

    addMessage(message, "user-message");
    userInput.value = "";
    sendButton.disabled = true;

    try {
        const response = await fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                message: message
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Unable to get a response.");
        }

        addMessage(data.reply, "bot-message");

    } catch (error) {
        addMessage(
            "Sorry, something went wrong. Please try again.",
            "bot-message"
        );
        console.error(error);
    } finally {
        sendButton.disabled = false;
        userInput.focus();
    }
}

sendButton.addEventListener("click", sendMessage);

userInput.addEventListener("keydown", function(event) {
    if (event.key === "Enter") {
        sendMessage();
    }
});

document.getElementById("workout-btn").addEventListener("click", async function() {
    const result = document.getElementById("workout-result");

    result.textContent = "Loading workout ideas...";

    try {
        const response = await fetch("/workout");
        const data = await response.json();

        if (!response.ok) {
            throw new Error("Could not load workout ideas.");
        }

        result.textContent = data.workout;

    } catch (error) {
        result.textContent = "Unable to load workout ideas.";
        console.error(error);
    }
});
