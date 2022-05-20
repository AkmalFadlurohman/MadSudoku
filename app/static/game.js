// Handle challenge initiation and set challenge data to game board
function startChallenge(title, id) {
	closeSidebar();
	resetTimer();
	clearBoard();
	getChallengeData(id, function(data) {
		if (data) {
			let challenge = data;
			let board = challenge.question;
			// Set game data to board
			for (var i=0;i<board.length;i++) {
				var j = 0;
				while (j<board[i].length) {
					var cellIdx = j+i*9; //Simulate two dimesional array index on one dimesional array
					if (board[i][j] != 0) {
						$("#cell-input-"+cellIdx).val(board[i][j]);
						$("#cell-input-"+cellIdx).prop("disabled", true);
					}
					j++;
				}
			}
			setChallengeTitle(title);
			// Hide messages from previous game
			$("#toast-challenge").text("");
			$("#toast-challenge").hide();
			// Set hidden form input to selected CHallenge ID
			$("#challenge-id").val(id);
			// Update stats modal
			$("#stats-msg").hide();
			$("#stats-ranks").show();
			$("#stats-time").html("");
			$("#share-btn").hide();

			$("#check-btn").prop("disabled", false);
			startTimer();
		} else {
			window.alert("An error occurred. Please try again later.");
		}
	});
}
// Get challengedata selected by user from server
function getChallengeData(challengeID, callback) {
	let url = "http://localhost:5000/challenge?id=" + challengeID;
	$.ajax({url: url, success: function(response) {
		callback(response);
	}});
}
// Set display title for selected challenge
function setChallengeTitle(challengeTitle) {
	challengeHeading = challengeTitle + " Challenge";
	$("#challenge-title").text(challengeHeading);
	$("#stats-challenge").text(challengeHeading);
}
// Clear game board from data, handle challenge switching
function clearBoard() {
	for (i = 0; i < 81; i++) {
		$("#cell-input-"+i).val("");
		$("#cell-input-"+i).prop("disabled", false);
	}
}
// Handle checking user answer, send game data to server, and set response accordingly
function checkSolution() {
	// Array to build game data
	let answer = new Array();
	// Check for empty cells
	for (var i=0;i<9;i++) {
		answer[i] = new Array();
		var j = 0;
		while (j<9) {
			var cellIdx = j+i*9; //Simulate two dimesional array index on one dimesional array
			// If empty cell is found, display message
			if ($("#cell-input-"+cellIdx).val() === "") {
				$("#toast-challenge").text("There are still empty cells in the board!");
				$("#toast-challenge").show();
				setTimeout((function() {
					$("#toast-challenge").hide();
					$("#toast-challenge").text("");
				}), 2500);
				return;
			}
			answer[i].push($("#cell-input-"+cellIdx).val());
			j++;
		}
	}
	stopTimer(); // Pause timer before sending data to server
	clearTime = $("#hours").html() + ":" + $("#mins").html() + ":" + $("#seconds").html();
	data = {
		challenge_id: $("#challenge-id").val(),
		user_name: $("#username-view").text(),
		clear_time: clearTime,
		answer: answer
	};
	// Send game data to server
	$.ajax({
		type: "POST",
		url: "http://localhost:5000/result/check",
		data: JSON.stringify(data),
		processData: false,
		contentType: "application/json",
		success: function(response) {
			// If user answer is correct, stop ongoing challenge
			if (response.clear) {
				stopChallenge();
			} else {
				// Start timer again if current answer is incorrect and display message
				startTimer();
				$("#toast-challenge").text("There are still cells with incorrect values!");
				$("#toast-challenge").show();
				setTimeout((function() {
					$("#toast-challenge").hide();
					$("#toast-challenge").text("");
				}), 2500);
			}
		}
	});
}
// Set related view components for stopped challenge/game mode
function stopChallenge() {
	$("#toast-challenge").text("Challenge Cleared");
	$("#toast-challenge").show();
	$("#check-btn").prop("disabled", true);
	// Show clear time and share button in stats modal
	$("#stats-time").html("Your time: " + clearTime);
	$("#share-btn").show();
	getTopFive($("#challenge-id").val());
}
