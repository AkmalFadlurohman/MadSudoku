/* Set the width of the sidebar to 20% of screen width */
function openSidebar() {
	getChallengesList(function(data) {
		if (data) {
			const challenges = JSON.parse(data);
			if (challenges.length > 0) {
					$("#challenges-msg").hide();
					for (var i=0;i<challenges.length;i++) {
						$("#challenges-list").append("<a href='#' onclick='startChallenge(this.innerHTML, " + challenges[i].id + ")'>" + challenges[i].name + "</a>");
					}
					$("#left-sidebar").width("20%");
			}
		}
	});
}
/* Set sidebar width to 0 (Hide sidebar) */
function closeSidebar() {
	$("#challenges-msg").show();
	$("#challenges-list").empty();
	$("#left-sidebar").width(0);
}
function getChallengesList(callback) {
	$.ajax({url: "http://localhost:5000/challenge/list", success: function(result) {
		callback(result);
	}});
}
function startChallenge(title, id) {
	closeSidebar();
	resetTimer();
	clearBoard();
	getChallengeData(id, function(data) {
		if (data) {
			let challenge = JSON.parse(data);
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
				setChallengeTitle(title);
				$("#stats-msg").hide();
				$("#stats-ranks").show();
				startTimer();
				$("#check-btn").prop("disabled", false);
			}
		} else {
			window.alert("An error occurred. Please try again later.");
		}
	});
}
function getChallengeData(id, callback) {
	let url = "http://localhost:5000/challenge?id=" + id;
	$.ajax({url: url, success: function(result) {
		callback(result);
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
function updateUsername() {
	username = $("#username-input").val();
	if (username == "") {
		return false;
	}
	$("#username-view").text(username);
	$("#username-modal").modal("hide");
}
function checkSolution() {
	for (var i=0;i<81;i++) {
		if ($("#cell-input-"+i).val() === "") {
			$("#toast-empty-cells").show();
			setTimeout((function() {
				$("#toast-empty-cells").hide();
			}), 2500);
			return;
		}
		if ($("#cell-input-"+i).val() != $("#cell-hidden-"+i).val()) {
			$("#cell-input-"+i).focus();
			$("#toast-incorrect-cells").show();
			setTimeout((function() {
				$("#toast-incorrect-cells").hide();
			}), 2500);
			return;
		}
	}
	stopChallenge();
}
function stopChallenge() {
	stopTimer();
	copyTime();
	$("#check-btn").prop("disabled", true);
	$("#share-btn").show();
	$("#stats-modal").modal("show");
}
function copyTime() {
	$("#stats-hours").html($("#hours").html());
	$("#stats-mins").html($("#mins").html());
	$("#stats-seconds").html($("#seconds").html());
}

function shareStats() {
	var time = $("#stats-hours").html() + $("#stats-mins").html() + $("#stats-seconds").html();
	var text = "I did MadSudoku " + $("#challenge-title").html() + " in " + time + ". What's your time?";
	let temp = document.createElement("textarea");
	temp.value = text;
	temp.setAttribute("readonly", "");
	temp.style.position = "absolute";
	temp.style.left = "-9999px";
	document.body.appendChild(temp);
	temp.select();
	document.execCommand("copy");
	document.body.removeChild(temp);
	$("#toast-share").css("visibility", "visible");
	setTimeout((function() {
		$("#toast-share").css("visibility", "hidden");
	}), 1000);
}
