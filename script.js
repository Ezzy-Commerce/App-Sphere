// Store user data locally
let users = JSON.parse(localStorage.getItem("users")) || [];
let currentUser = JSON.parse(localStorage.getItem("currentUser")) || null;

// Check username availability in real-time
function checkUsernameAvailability() {
  const usernameInput = document.getElementById("username");
  const availabilityMessage = document.getElementById("username-availability");

  usernameInput.addEventListener("input", () => {
    const username = usernameInput.value.trim().toLowerCase();
    const userExists = users.some(user => user.username.toLowerCase() === username);

    if (username) {
      if (userExists) {
        availabilityMessage.textContent = "Username is already taken.";
        availabilityMessage.style.color = "red";
        // Hide the message after 3 seconds
        setTimeout(() => {
          availabilityMessage.textContent = "";
        }, 3000); // 3 seconds delay
      } else {
        availabilityMessage.textContent = "Username is available.";
        availabilityMessage.style.color = "green";
      }
    } else {
      availabilityMessage.textContent = "";
    }
  });
}

// Handle Registration
function register(event) {
  event.preventDefault(); // Prevent form submission

  const username = document.getElementById("username").value.trim();
  const email = document.getElementById("email").value.trim(); // Email field added
  const password = document.getElementById("password").value.trim();
  const confirmPassword = document.getElementById("confirm-password").value.trim();
  const termsAccepted = document.getElementById("terms").checked; // Check if terms are accepted

  // Validate input
  if (!username || !email || !password || !confirmPassword) {
    showMessage("Please fill in all fields.", "error");
    return;
  }

  if (!termsAccepted) {
    showMessage("You must accept the Terms and Conditions to register.", "error");
    return;
  }

  if (password !== confirmPassword) {
    showMessage("Passwords do not match.", "error");
    return;
  }

  // Check if the username or email already exists
  const userExists = users.some(
    user => user.username.toLowerCase() === username.toLowerCase() || user.email.toLowerCase() === email.toLowerCase()
  );

  if (userExists) {
    showMessage("A user with this username or email already exists. Please choose different credentials.", "error");
    return;
  }

  // Hash the password before storing (use secure methods in production)
  const hashedPassword = hashPassword(password);
  const newUser = { username, email, password: hashedPassword, uploadedApps: [] };

  users.push(newUser);
  localStorage.setItem("users", JSON.stringify(users));
  showMessage("Registration successful! Redirecting to payment page...", "success");

  // Show loading indicator
  const loadingMessage = document.createElement("div");
  loadingMessage.classList.add("loading");
  loadingMessage.textContent = "Loading... Please wait.";
  document.body.appendChild(loadingMessage);

  // Redirect to payment page after a short delay to show the loading message
  setTimeout(() => {
    window.location.href = "payment.html";
  }, 2000); // Redirect after 2 seconds
}

// Show messages to the user
function showMessage(message, type) {
  const messageBox = document.getElementById("message-box");
  if (messageBox) {
    messageBox.textContent = message;
    messageBox.className = `message ${type}`; // Add CSS class based on message type
  } else {
    alert(message); // Fallback if no message box is available
  }
}

// Toggle password visibility
function togglePasswordVisibility(inputId, iconElement) {
  const input = document.getElementById(inputId);
  const icon = iconElement.querySelector("i");

  if (input.type === "password") {
    input.type = "text";
    icon.classList.remove("fa-eye");
    icon.classList.add("fa-eye-slash");
  } else {
    input.type = "password";
    icon.classList.remove("fa-eye-slash");
    icon.classList.add("fa-eye");
  }
}

// Focus on the username field on page load
window.onload = () => {
  const usernameField = document.getElementById("login-username");
  if (usernameField) usernameField.focus();
  
  checkUsernameAvailability();
};
