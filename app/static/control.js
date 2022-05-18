/* Set the width of the sidebar to 20% of screen width */
function openSidebar() {
	$(".navbar-collapse").collapse("hide");
	getChallengesList(function(data) {
		if (data) {
			const challenges = JSON.parse(data)
			if (challenges.length > 0) {
					$("#challenges-msg").hide();
					for (var i=0;i<challenges.length;i++) {
						$("#challenges-list").append("<a href='#' onclick='startChallenge(this.innerHTML, " + challenges[i].id + ")'>" + challenges[i].name + "</a>");
					}
					$("#left-sidebar").toggleClass("open");
			}
		}
	});
}
/* Set sidebar width to 0 (Hide sidebar) */
function closeSidebar() {
	$("#challenges-msg").show();
	$("#challenges-list").empty();
	$("#left-sidebar").toggleClass("open");
}
function openStatsModal() {
	let challengeID = $("#challenge-id").val();
	if (challengeID !== "") {
		getTopFive(challengeID);
	} else {
		$("#stats-modal").modal("show");
	}
}
function getChallengesList(callback) {
	$.ajax({url: "http://localhost:5000/challenge/list", success: function(response) {
		callback(response);
	}});
}
function updateUsername() {
	username = $("#username-input").val();
	if (username == "") {
		return false;
	}
	userpasswd = $("#userpasswd-input").val();
	data = { "user_name" : username, "user_passwd" : userpasswd }
	$.ajax({
		type: "POST",
		url: "http://localhost:5000/user/login",
		data: JSON.stringify(data),
		processData: false,
		contentType: "application/json",
		success: function(response){
			$("#username-view").text(username)
		}
	});
	//$("#username-view").text(username);
	$("#username-modal").modal("hide");
}
function getTopFive(challengeID) {
	$("#ranks-table > tbody").empty();
	let url = "http://localhost:5000/result?challenge_id=" + challengeID;
	$.ajax({
		url: url,
		success: function(response) {
			var ranks = JSON.parse(response);
			if (ranks.length == 0) {
				$("#ranks-msg").show();
			} else {
				$("#ranks-msg").hide();
				for (var i=0;i<ranks.length;i++) {
					row = "<tr><td>" + (i+1) + "</td><td>" + ranks[i].user_name + "</td><td>" + ranks[i].clear_time + "</td></tr>";
					$("#ranks-table > tbody:last-child").append(row);
				}
			}
			$("#stats-modal").modal("show");
		},
		error: function(XMLHttpRequest, textStatus, errorThrown) {
			$("#ranks-msg").show();
			$("#stats-modal").modal("show");
		}
	});
}
function shareStats() {
	var time = $("#stats-time").html();
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
