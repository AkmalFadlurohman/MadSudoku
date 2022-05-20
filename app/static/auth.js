// Handle login button click, validate the input fields and send login request
function login() {
	if (!validateUsername($("#login-username").val())) {
		setLoginMessage("Username must be of two or more characters");
	} else if (!validatePassword($("#login-password").val())) {
		setLoginMessage("Password  must be between 6 to 20 characters and contain at least a number, an uppercase, and a lowercase letter");
	} else {
		sendLoginRequest($("#login-username").val(), $("#login-password").val());
	}
}
// Build login request data and send to server using AJAX
function sendLoginRequest(username, password) {
	let data = {
		user_name: username,
		user_passwd: password
	};
	$.ajax({
		type: "POST",
		url: "http://localhost:5000/user/login",
		data: JSON.stringify(data),
		processData: false,
		contentType: "application/json",
		success: function(response) {
			if (response.result) {
				$("#login-username").val("");
				$("#login-password").val("");
				$(".navbar-collapse").collapse("hide");
				$("#username-view").text(username);
				// Hide the login/register button and show the logout button in place
				$("#auth-btn").hide();
				$("#logout-btn").show();
				// Display success message and close auth modal
				$("#toast-login").text("Success");
				$("#toast-login").css("visibility", "visible");
				setTimeout((function() {
					$("#toast-login").css("visibility", "hidden");
					$("#auth-modal").modal("hide");
				}), 1500);
			} else {
				setLoginMessage("Login failed. Please try again later.");
			}
		},
		error: function(XMLHttpRequest, textStatus, errorThrown) {
			// Handle error from server
			let response = XMLHttpRequest.responseText;
			let msg = response.substring(response.lastIndexOf("<p>") + "<p>".length, response.lastIndexOf("</p>"));
			setLoginMessage(msg);
		}
	});
}
// Display error or success message on login process
function setLoginMessage(msg) {
	$("#toast-login").text(msg);
	$("#toast-login").css("visibility", "visible");
	setTimeout((function() {
		$("#toast-login").css("visibility", "hidden");
	}), 1500);
}
// Handle login button click, validate the input fields, and send sign up request
function register() {
	if (!validateUsername($("#register-username").val())) {
		setRegisterMessage("Username must be of two or more characters");
	} else if (!validatePassword($("#register-password").val())) {
		setRegisterMessage("Password  must be between 6 to 20 characters and contain at least a number, an uppercase, and a lowercase letter");
	} else if ($("#register-password").val() !== $("#register-password-confirm").val()) {
		setRegisterMessage("Passwords do not match");s
	} else {
		sendRegisterRequest($("#register-username").val(), $("#register-password").val());
	}
}
// Build user register/sign up request data and send to server using AJAX
function sendRegisterRequest(username, password) {
	let data = {
		user_name: username,
		user_passwd: password
	};
	$.ajax({
		type: "POST",
		url: "http://localhost:5000/user/signup",
		data: JSON.stringify(data),
		processData: false,
		contentType: "application/json",
		success: function(response) {
			if (response.result) {
				$("#register-username").val("");
				$("#register-password").val("");
				$("#register-password-confirm").val("");
				// Ask user to login after successful registration
				$("#toast-register").text("Success. Please login again.");
				$("#toast-register").css("visibility", "visible");
				setTimeout((function() {
					$("#toast-register").css("visibility", "hidden");
					$("#auth-modal").modal("hide");
				}), 1500);
			} else {
				setRegisterMessage("Register failed. Please try again later.");
			}
		},
		error: function(XMLHttpRequest, textStatus, errorThrown) {
				// Handle error from server
			let response = XMLHttpRequest.responseText;
			let msg = response.substring(response.lastIndexOf("<p>") + "<p>".length, response.lastIndexOf("</p>"));
			setRegisterMessage(htmlDecode(msg));
		}
	});
}
// Display error or success message on user registration process
function setRegisterMessage(msg) {
	$("#toast-register").text(msg);
	$("#toast-register").css("visibility", "visible");
	setTimeout((function() {
		$("#toast-register").css("visibility", "hidden");
	}), 1500);
}
// Handle user logout
function logout(){
	$.ajax({
		type: "POST",
		url: "http://localhost:5000/user/logout",
		processData: false,
		contentType: "application/json",
		success: function(response) {
			// Hide menu bar on mobile view
			$(".navbar-collapse").collapse("hide");
			// Update username view to Guest and show login/register button
			$("#username-view").text("Guest");
			$("#auth-btn").show();
			$("#logout-btn").hide();
		}
	});
}
// Validate username input, ensure it is at least of 2 characters
function validateUsername(username) {
	return (username != "" && username.length >= 2);
}
// Validate user password, ensure it is between 6-20 letters,
// and contain at least a number, an uppercase, and a lowercase letter
function validatePassword(password) {
	let passw = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{6,20}$/;
	return (password != "" && password.match(passw))
}
// Decode HTML encoded server response
function htmlDecode(input) {
	var doc = new DOMParser().parseFromString(input, "text/html");
	return doc.documentElement.textContent;
}
