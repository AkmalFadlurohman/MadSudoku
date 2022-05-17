/* Set the width of the sidebar to 20% of screen width */
function openSidebar() {
	getChallengesList(function(data) {
		if (data) {
			const challenges = data
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
	// stopTimer();
	resetTimer();
	clearBoard();
	getChallengeData(id, function(data) {
		if (data) {
			var board = data.question;
			for (var i=0;i<board.length;i++) {
				var j = 0;
				while (j<board[i].length) {
					if (board[i][j] == 0) {
						j++;
					} else {
						var cellIdx = j+i*9;
						$("#cell-input-"+cellIdx).val(board[i][j]);
						$("#cell-input-"+cellIdx).prop("disabled", true);
						j++;
					}
				}
				setChallengeTitle(title);
				$("#stats-msg").hide();
				$("#stats-ranks").show();
				startTimer();
				$("#check-btn").prop("disabled", false);
			}
		} else {
			window.aler("An error occurred. Please try again later.")
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
	for (i = 0; i < 82; i++) {
		$('.cell-txt-input[name="cell-input[' + (i) + ']"]').val("");
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
function stopChallenge() {
	stopTimer();
	copyTime();
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
	$("#toast").css("visibility", "visible")
	setTimeout((function() {
		$("#toast").css("visibility", "hidden");
	}), 1000);
}
