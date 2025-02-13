async function hashPassword(password) {
    const encoder = new TextEncoder();
    const data = encoder.encode(password);
    const hashBuffer = await crypto.subtle.digest('SHA-256', data);
    const hashArray = Array.from(new Uint8Array(hashBuffer));
    return hashArray.map(byte => byte.toString(16).padStart(2, '0')).join('');
}

async function loginUser(event) {
    event.preventDefault();
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    const csrfToken = document.getElementById("csrf_token").value;

    try {
        const hashedPassword = await hashPassword(password);

        const response = await fetch("/user/login/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken
            },
            body: JSON.stringify({ username, password: hashedPassword }),
            credentials: "include" // Ensures cookies (session) are sent
        });

        const result = await response.json();
        if (response.ok) {
            alert("Login successful!");
            window.location.href = menuRedirectUrl; // Redirect to menu
        } else {
            alert(result.error);
        }
    } catch (error) {
        console.error("Error logging in:", error);
    }
}

// Store the Django-generated redirect URL

