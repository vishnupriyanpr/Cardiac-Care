// ... (keep previous code until loginUser function)

function loginUser() {
  const email = document.getElementById('loginEmail').value.trim();
  const password = document.getElementById('loginPassword').value;
  
  // Clear previous errors
  clearError();
  
  if (!email || !password) {
    showError("Please enter both email and password.");
    return;
  }
  
  // Check credentials
  const user = users.find(u => u.email === email && u.password === password);
  
  if (user) {
    // Successful login
    loginForm.classList.add('hidden');
    chatContainer.classList.remove('hidden');
    
    // Clear chat box
    chatBox.innerHTML = '';
    
    // Welcome message
    setTimeout(() => {
      const welcomeMsg = document.createElement('div');
      welcomeMsg.className = 'message bot';
      welcomeMsg.innerHTML = `
        <strong>Welcome back, ${user.name}!</strong><br><br>
        I'm your Heart Disease Risk Classifier. Please describe any symptoms...
      `;
      chatBox.appendChild(welcomeMsg);
      chatBox.scrollTop = chatBox.scrollHeight;
    }, 500);
  } else {
    // Either email or password is wrong
    showError("Invalid credentials. Please try again.");
    
    // Highlight both fields
    document.getElementById('loginEmail').classList.add('error');
    document.getElementById('loginPassword').classList.add('error');
  }
}

function showError(message) {
  clearError(); // Clear any existing errors
  
  const errorElement = document.createElement('div');
  errorElement.className = 'error-message';
  errorElement.textContent = message;
  
  const loginButton = document.querySelector('#login button');
  loginButton.parentNode.insertBefore(errorElement, loginButton.nextSibling);
}

function clearError() {
  // Remove error message
  const existingError = document.querySelector('.error-message');
  if (existingError) {
    existingError.remove();
  }
  
  // Remove error styling from fields
  document.getElementById('loginEmail').classList.remove('error');
  document.getElementById('loginPassword').classList.remove('error');
}

// ... (rest of the code remains the same)