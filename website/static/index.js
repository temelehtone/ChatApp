
// Sends the message to the back-end
$(function () {
  $("#sendBtn").on("click", function (e) {
    var value = document.getElementById("msg").value;
    document.getElementById("msg").value = "";
    
    e.preventDefault();
    $.getJSON("/send_message", { val: value }, function (data) {
      //do nothing
    });
    return false;
  });
});

// Updates the messages 10 times in second
window.onload = function () {
  setInterval(update, 100);
};

function update() {
  this.fetch("/get_messages")
    .then(function (response) {
      return response.json();
    })
    .then(function (dict) {
      $("#list").empty();
      for (msg of dict["messages"]) {
        if (msg.substring(0, 6) == "SERVER") {
          handleServeralerts(msg);
        } else {
          var messageList = msg.split(":");
          $("#list").append(
            `<li><div class='top-row'><h5 class='name'>${messageList[0]}</h5><p class='text'>${messageList[1]}</p></div><div class='time-div'><p class='time'>${messageList[2]}:${messageList[3]}:${messageList[4]}</p></div></li>`
          );
        }
      }
    });
}

function handleServeralerts(msg) {
  if (msg.includes("has joined the chat")) {
    var status = document.getElementById("status");
    status.classList = ""
    status.classList.add("success");
    status.innerHTML = msg;
    
  }
  if (msg.includes("has left the chat")) {
    var status = document.getElementById("status");
    status.classList = ""
    status.classList.add("error");
    status.innerHTML = msg;
    
  }
  
}
function removeStatus() {
  var status = document.getElementById("status");
  status.className = ""
}


function scrollToBottom() {
  

    var element = document.querySelector("#text-field");
    if (element) { 
        // element found
        element.scrollHeight = element.scrollHeight;
    } 
    
  
}


