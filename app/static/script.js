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
	startTimer();
	$("#check-btn").prop("disabled", false);
}
function setChallengeTitle(challengeTitle) {
	$("#challenge-title").text(challengeTitle);
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
}
