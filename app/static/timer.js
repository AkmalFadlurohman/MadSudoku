"use strict";

let hour = 0;
let minute = 0;
let second = 0;
let millisecond = 0;

let cron;

function startTimer() {
	stopTimer();
	cron = setInterval(() => { timer(); }, 10);
}

function stopTimer() {
	clearInterval(cron);
}

function resetTimer() {
	hour = 0;
	minute = 0;
	second = 0;
	$("#hours").html("00");
	$("#mins").html("00");
	$("#seconds").html("00");
}

function timer() {
	if ((millisecond += 10) == 1000) {
		millisecond = 0;
		second++;
	}
	if (second == 60) {
		second = 0;
		minute++;
	}
	if (minute == 60) {
		minute = 0;
		hour++;
	}
	$("#hours").html(returnData(hour));
	$("#mins").html(returnData(minute));
	$("#seconds").html(returnData(second));
}

function returnData(input) {
	return input > 10 ? input : `0${input}`
}
