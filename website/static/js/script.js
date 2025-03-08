document.getElementById("checkBtn").addEventListener("click", function() {
    let password = document.getElementById("password").value;

    fetch("/check_password", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ password: password })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("result").innerHTML = 
            `Strength: <strong>${data.strength}</strong><br>
             Length: ${data.criteria.length ? "✅" : "❌"} |
             Uppercase: ${data.criteria.uppercase ? "✅" : "❌"} |
             Lowercase: ${data.criteria.lowercase ? "✅" : "❌"} |
             Digits: ${data.criteria.digits ? "✅" : "❌"} |
             Special Chars: ${data.criteria.special_chars ? "✅" : "❌"}`;
    })
    .catch(error => console.error("Error:", error));
});
