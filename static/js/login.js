  function login() {
    // Get the username and password from the form
    var username = document.getElementById("username").value;
    var password = document.getElementById("password").value;

    // Create the URL with username and password parameters
    var url = "http://localhost:8000/api/get_token?user_name=" + encodeURIComponent(username) + "&user_pass=" + encodeURIComponent(password);

    // Send a POST request to the API endpoint
    fetch(url, {
      method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
      // Check if login was successful
      if (data.flag === true) {
        // Set the token to a cookie
        document.cookie = "token=" + data.content;
        // Show success message
        showAlert("Login successful", "alert-success");
        // Replace login button with username
        var loginField = document.getElementById("login-btn");
        loginField.innerText = username
        window.location.href = "/";

      } else {
        // Show error message
        showAlert("Login failed. Error message: " + data.msg, "alert-danger");
      }
    })
    .catch(error => {
      // Show error message
      showAlert("Error: " + error, "alert-danger");
    });
  }

  function showAlert(message, alertType) {
    var alertDiv = document.createElement("div");
    alertDiv.className = "alert " + alertType;
    alertDiv.appendChild(document.createTextNode(message));
    var container = document.querySelector(".container");
    container.insertBefore(alertDiv, container.firstChild);
    setTimeout(function(){
      alertDiv.remove();
    }, 3000);
  }
