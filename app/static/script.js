/* Set the width of the sidebar to 20% of screen width */
function openSidebar() {
	$("#left-sidebar").width("20%");
}
/* Set sidebar width to 0 (Hide sidebar) */
function closeSidebar() {
	$("#left-sidebar").width(0);
}
function startChallenge(challenge) {
	resetTimer();
	clearBoard();
	setChallengeTitle(challenge.innerHTML);
	$("#stats-msg").hide();
	$("#stats-ranks").show();
	startTimer();
	$("#check-btn").prop("disabled", false);
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
