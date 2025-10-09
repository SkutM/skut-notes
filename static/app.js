const output = document.getElementById("output");

// displays messages

function log(message, data = null) {
    output.textContent = message + (data ? "\n" + JSON.stringify(data, null, 2) : "");
}

// register
document.getElementById("register-btn").addEventListener("click", async () => {
    const username = document.getElementById("reg-username").value;
    const password = document.getElementById("reg-password").value;

    // for clicks
    const registerBtn = document.getElementById("register-btn");
    registerBtn.disabled = true;

    try {
        const res = await fetch("/api/register", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username, password})
        });

        const data = await res.json();
        log(`Register response (${res.status}):`, data);
    } catch (err) {
        log("Error during register:", err)
    } finally {
        registerBtn.disabled = false;
    }
});

// login
document.getElementById("login-btn").addEventListener("click", async () => {
    const username = document.getElementById("login-username").value;
    const password = document.getElementById("login-password").value;

    // avoid multiple rapid submissions login
    const loginBtn = document.getElementById("login-btn");
    loginBtn.disabled = true;

    try {
        const res = await fetch("/api/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username, password })
        });

        const data = await res.json();

        if (res.ok) {
            // store tokens
            localStorage.setItem("access_token", data.access_token);
            localStorage.setItem("refresh_token", data.refresh_token);
            localStorage.setItem("user_id", data.user_id); // handled in auth.py, as well
            log(`Login successful! Tokens stored.`, data);
            document.getElementById("notes-section").style.display = "block";
            document.getElementById("logout-btn").style.display = "inline-block"; // show logout
            getNotes();
        } else {
            log(`Login failed (${res.status}):`, data);
        }
    } catch (err) {
        log ("Error during login:", err);
    } finally {
        // for login button
        loginBtn.disabled = false;
    }
    
});

// logout
document.getElementById("logout-btn").addEventListener("click", () => {
    localStorage.clear();
    document.getElementById("notes-section").style.display = "none";
    document.getElementById("logout-btn").style.display = "none";
    log("Logged out succesfully");
});

// notes helper for auth headers
function getAuthHeaders() {
    const token = localStorage.getItem("access_token");
    return {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`
    };
}

// create note
document.getElementById("create-note-btn").addEventListener("click", async () => {
    const userId = localStorage.getItem("user_id");
    if (!userId) {
        log("Error: You must log in before creating a note.")
        return;
    }
    const text = document.getElementById("note-input").value;

    // create btn
    const createBtn = document.getElementById("create-note-btn");
    createBtn.disabled = true;

    try {
        const res = await fetch(`/api/${userId}/notes`, {
            method: "POST",
            headers: getAuthHeaders(),
            body: JSON.stringify({ text })
        });
        const data = await res.json();
        log(`Create Note (${res.status})`, data);
        if (res.ok) {
            document.getElementById("note-input").value = ""; //clear field after creating note
            getNotes();
        }
    } catch (err) {
        log("Error creating note:", err)
    } finally {
        createBtn.disabled = false;
    }
});

// get notes
async function getNotes() {
    const userId = localStorage.getItem("user_id");

    try {
        const res = await fetch(`/api/${userId}/notes`, {
            headers: getAuthHeaders()
        });
        const data = await res.json();

        if (res.ok) {
            const container = document.getElementById("notes-container");
            container.innerHTML = "";
            data.notes.forEach(note => {
                const div = document.createElement("div");
                div.textContent = note.text;

                // for reflecting note change next to btns
                div.dataset.noteId = note.id;

                // Edit button
                const editBtn = document.createElement("button");
                editBtn.textContent = "Edit";
                editBtn.addEventListener("click", () => {
                    const newText = prompt("Edit note:", note.text);
                    if (newText && newText.trim() !== "") {
                        updateNote(note.id, newText);
                    }
                });

                // Delete button
                const delBtn = document.createElement("button");
                delBtn.textContent = "Delete";
                delBtn.addEventListener("click", () => {
                    deleteNote(note.id);
                });

                // Add to DOM
                div.appendChild(editBtn);
                div.appendChild(delBtn);
                // was here before (below)
                container.appendChild(div);
            });
            log("Fetched notes successfully:", data);
        } else {
            log(`Failed to fetch notes (${res.status}):`, data);
        }
    } catch (err) {
        log("Error fetching notes:", err);
    }
}

async function deleteNote(noteId) {
    const userId = localStorage.getItem("user_id");
    try {
        const res = await fetch(`/api/${userId}/notes/${noteId}`, {
            method: "DELETE",
            headers: getAuthHeaders()
        });
        
        if (res.ok) {
            log(`Deleted note ${noteId}`);
            getNotes();
        } else {
            const data = await res.json();
            log(`Failed to delete (${res.status}):`, data);
        } 
    } catch (err) {
        log("Error deleting note:", err)
    }
}

async function updateNote(noteId, newText) {
    const userId = localStorage.getItem("user_id");
    try {
        const res = await fetch(`/api/${userId}/notes/${noteId}`, {
            method: "PUT",
            headers: getAuthHeaders(),
            body: JSON.stringify({ text: newText })
        });
        const data = await res.json();
        if (res.ok) {
            log(`Updated note ${noteId}`, data)
            // reflecting note change immediately
            // *next to edit and del buttons, not output (that's fine)*
            const noteElements = document.querySelectorAll("#notes-container div");
            noteElements.forEach(div => {
                if (div.dataset.noteId == noteId) {
                    div.firstChild.textContent = newText;
                }
            })
        } else {
            log(`Failed to update (${res.status}):`, data)
        }
    } catch (err) {
        log("Error updating note:", err)
    }
}