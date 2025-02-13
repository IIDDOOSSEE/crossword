async function checkUser() {
    try {
        const response = await fetch("/user/info/");
        const result = await response.json();

        if (response.ok) {
            document.getElementById("user-label").textContent = "Logged in as: " + result.username;
            document.getElementById("logout-btn").style.display = "block";
        } else {
            document.getElementById("user-label").textContent = "Not logged in";
            document.getElementById("logout-btn").style.display = "none";
        }
    } catch (error) {
        console.error("Error checking user:", error);
    }
}

async function hashPassword(password) {
    const encoder = new TextEncoder();
    const data = encoder.encode(password);
    const hashBuffer = await crypto.subtle.digest('SHA-256', data);
    const hashArray = Array.from(new Uint8Array(hashBuffer));
    return hashArray.map(byte => byte.toString(16).padStart(2, '0')).join('');
}

async function registerUser(event) {
    event.preventDefault();
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    const confirmPassword = document.getElementById("confirmPassword").value;
    const csrfToken = document.getElementById("csrf_token").value;

    if (password !== confirmPassword) {
        alert("Passwords do not match");
        return;
    }

    try {
        const hashedPassword = await hashPassword(password);

        const response = await fetch("/user/register/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken
            },
            body: JSON.stringify({ username, password: hashedPassword }) // Sending hashed password
        });

        const result = await response.json();
        if (response.ok) {
            alert("User registered successfully!");
            window.location.href = "/user/login";
        } else {
            alert(result.error);
        }
    } catch (error) {
        console.error("Error registering user:", error);
    }
}

async function logoutUser() {
    try {
        await fetch("/user/logout/");
        window.location.href = "/user/login";
    } catch (error) {
        console.error("Error logging out:", error);
    }
}

window.onload = checkUser;
