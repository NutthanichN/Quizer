function convertToTimeFormat(rawSeconds) {
  rawSeconds = Math.floor(rawSeconds / 1000);
  var hours = Math.floor(rawSeconds / (60 * 60));
  var minutes = Math.floor((rawSeconds % (60 * 60)) / 60);
  var seconds = Math.floor((rawSeconds % (60 * 60)) % 60);
  var strH = hours.toString();
  var strM = minutes.toString();
  var strS = seconds.toString();
  if(minutes < 10) {
    strM = "0" + strM;
  }
  if(seconds < 10) {
    strS = "0" + strS;
  }
  return strH + ":" + strM + ":" + strS;
}

if(typeof(Storage) !== "undefined") {
  // console.log("here");
  if(sessionStorage.getItem("initTime") === null) {
    document.getElementById("time").innerHTML = "0:00:00";
    var initTime = new Date().getTime();
    sessionStorage.setItem("initTime", initTime.toString());
    // console.log(sessionStorage.getItem("initTime"));
  }
  else {
    document.getElementById("time").innerHTML = sessionStorage.getItem("previousTimeDuration");
  }
}

function timer() {
  var currentTime = new Date().getTime();
  var timeDuration = currentTime - parseInt(sessionStorage.getItem("initTime"));
  var timeDurationStr = convertToTimeFormat(timeDuration);
  sessionStorage.setItem("previousTimeDuration", timeDurationStr);
  document.getElementById("time").innerHTML = timeDurationStr;
}

setInterval(timer, 1000);
