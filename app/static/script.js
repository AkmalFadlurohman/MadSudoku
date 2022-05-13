/* Set the width of the sidebar to 20% of screen width */
function openSidebar() {
	document.getElementById("left-sidebar").style.width = "20%";
}
/* Set sidebar width to 0 (Hide sidebar) */
function closeSidebar() {
	document.getElementById("left-sidebar").style.width = "0";
}
function startChallenge(challenge) {
	resetTimer();
	setChallengeTitle(challenge.innerHTML);
	startTimer();
	$("#check-btn").prop("disabled", false);
}
function setChallengeTitle(challengeTitle) {
	$("#challenge-title").text(challengeTitle);
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
