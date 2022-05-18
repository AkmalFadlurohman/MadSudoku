function startChallenge(title, id) {
	closeSidebar();
	resetTimer();
	clearBoard();
	getChallengeData(id, function(data) {
		if (data) {
			let challenge = data;
			let board = challenge.question;
			let solution = challenge.solution;
			for (var i=0;i<board.length;i++) {
				var j = 0;
				while (j<board[i].length) {
					var cellIdx = j+i*9;
					$("#cell-hidden-"+cellIdx).val(solution[i][j]);
					if (board[i][j] != 0) {
						$("#cell-input-"+cellIdx).val(board[i][j]);
						$("#cell-input-"+cellIdx).prop("disabled", true);
					}
					j++;
				}
			}
			setChallengeTitle(title);
			$("#toast-challenge").text("");
			$("#toast-challenge").hide();
			$("#challenge-id").val(id);
			$("#stats-msg").hide();
			$("#stats-ranks").show();
			startTimer();
			$("#check-btn").prop("disabled", false);
		} else {
			window.alert("An error occurred. Please try again later.");
		}
	});
}
function getChallengeData(challengeID, callback) {
	let url = "http://localhost:5000/challenge?id=" + challengeID;
	$.ajax({url: url, success: function(response) {
		callback(response);
	}});
}
function setChallengeTitle(challengeTitle) {
	challengeHeading = challengeTitle + " Challenge";
	$("#challenge-title").text(challengeHeading);
	$("#stats-challenge").text(challengeHeading);
}
function clearBoard() {
	for (i = 0; i < 81; i++) {
		$("#cell-input-"+i).val("");
		$("#cell-input-"+i).prop("disabled", false);
	}
}
function checkSolution() {
	// Array to build game input data
	let answer = new Array();
	// Check for empty cells
	for (var i=0;i<9;i++) {
		answer[i] = new Array();
		var j = 0;
		while (j<9) {
			var cellIdx = j+i*9;
			if ($("#cell-input-"+cellIdx).val() === "") {
				$("#toast-challenge").text("There are still empty cells in the board!");
				$("#toast-challenge").show();
				setTimeout((function() {
					$("#toast-challenge").hide();
					$("#toast-challenge").text("");
				}), 2500);
				return;
			}
			// if ($("#cell-input-"+cellIdx).val() != $("#cell-hidden-"+cellIdx).val()) {
			// 	$("#cell-input-"+cellIdx).focus();
			// 	$("#toast-challenge").text("There are still cells with incorrect values!");
			// 	$("#toast-challenge").show();
			// 	setTimeout((function() {
			// 		$("#toast-challenge").hide();
			// 		$("#toast-challenge").text("");
			// 	}), 2500);
			// 	return;
			// }
			answer[i].push($("#cell-input-"+cellIdx).val());
			j++;
		}
	}
	stopTimer();
	clearTime = $("#hours").html() + ":" + $("#mins").html() + ":" + $("#seconds").html();
	data = {
		challenge_id: $("#challenge-id").val(),
		user_name: $("#username-view").html(),
		clear_time: clearTime,
		answer: answer
	}
	$.ajax({
		type: "POST",
		url: "http://localhost:5000/result/check",
		data: JSON.stringify(data),
		processData: false,
		contentType: "application/json",
		success: function(response){
			if (response.clear) {
				stopChallenge();
			} else {
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
function stopChallenge() {
	$("#toast-challenge").text("Challenge Cleared");
	$("#toast-challenge").show();
	$("#check-btn").prop("disabled", true);

	$("#stats-time").html("Your time: " + clearTime);
	$("#share-btn").show();
	getTopFive($("#challenge-id").val());
}
