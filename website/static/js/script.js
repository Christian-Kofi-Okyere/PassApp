document.addEventListener("DOMContentLoaded", function() {
    const checkBtn = document.getElementById("checkBtn");
    const generateBtn = document.getElementById("generateBtn");
    const passwordInput = document.getElementById("password");
    const resultDiv = document.getElementById("result");
    const aiAdviceDiv = document.getElementById("ai-advice");
    const generatedPasswordDiv = document.getElementById("generated-password");
    const toggleVisibilityBtn = document.getElementById("toggleVisibility");
  
    checkBtn.addEventListener("click", function() {
      let password = passwordInput.value;
  
      fetch("/check_password", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ password: password })
      })
      .then(response => response.json())
      .then(data => {
        resultDiv.innerHTML = `
          <p><strong>Strength:</strong> ${data.strength}</p>
          <p>
            Length: ${data.criteria.length ? "✅" : "❌"} |
            Uppercase: ${data.criteria.uppercase ? "✅" : "❌"} |
            Lowercase: ${data.criteria.lowercase ? "✅" : "❌"} |
            Digits: ${data.criteria.digits ? "✅" : "❌"} |
            Special Chars: ${data.criteria.special_chars ? "✅" : "❌"}
          </p>
          ${data.is_common ? "<p class='text-danger'>Warning: This is a common password!</p>" : ""}
        `;
        aiAdviceDiv.innerHTML = `<strong>AI Advice:</strong> ${data.advice}`;
      })
      .catch(error => console.error("Error:", error));
    });
  
    generateBtn.addEventListener("click", function() {
      let length = document.getElementById("passwordLength").value || 12;
      fetch(`/generate_password?length=${length}`)
        .then(response => response.json())
        .then(data => {
          generatedPasswordDiv.innerHTML = `<strong>Generated Password:</strong> ${data.generated_password}`;
          passwordInput.value = data.generated_password;
        })
        .catch(error => console.error("Error:", error));
    });
  
    toggleVisibilityBtn.addEventListener("click", function() {
      if (passwordInput.type === "password") {
        passwordInput.type = "text";
        toggleVisibilityBtn.textContent = "Hide";
      } else {
        passwordInput.type = "password";
        toggleVisibilityBtn.textContent = "Show";
      }
    });
  });
  