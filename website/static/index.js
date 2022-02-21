
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

// Updates the messages 5 times in second
window.onload = function () {

  setInterval(update, 200);
};

function update() {
  this.fetch("/get_messages")
    .then(function (response) {
      return response.json();
    })
    .then(function (data) {
      $("#list").empty();

      // Updates the messages to the screen based on who sent them
      for (msg of data["messages"]) {
        var messageList = msg.split(":");
        if (msg.substring(0, 6) == "SERVER") {
          if (msg.includes("has joined the chat")) {
            $("#list").append(
              `<li class="list-item server-join"><div class='top-row'><h5 class='name'>${messageList[0]}</h5><p class='text'>${messageList[1]}</p></div><div class='time-div'><p class='time'>${messageList[2]}:${messageList[3]}:${messageList[4]}</p></div></li>`
            );
          }
          if (msg.includes("has left the chat")) {
            $("#list").append(
              `<li class="list-item server-left"><div class='top-row'><h5 class='name'>${messageList[0]}</h5><p class='text'>${messageList[1]}</p></div><div class='time-div'><p class='time'>${messageList[2]}:${messageList[3]}:${messageList[4]}</p></div></li>`
            );
          }
        } else {
          if (messageList[0] == data["name"]) {
            $("#list").append(
              `<li class="list-item"><div class='top-row'><h5 class='name'>${messageList[0]}</h5><p class='text'>${messageList[1]}</p></div><div class='time-div'><p class='time'>${messageList[2]}:${messageList[3]}:${messageList[4]}</p></div></li>`
            );
          } else {
            $("#list").append(
              `<li class="list-item another-client"><div class='top-row'><h5 class='name'>${messageList[0]}</h5><p class='text'>${messageList[1]}</p></div><div class='time-div'><p class='time'>${messageList[2]}:${messageList[3]}:${messageList[4]}</p></div></li>`
            );
          }
        }
      }
    });
}


// Scrolls to bottom of the chat when button pressed
function scrollToBottom() {
  var textField = document.querySelector("#text-field");
  textField.scrollTop = textField.scrollHeight - textField.clientHeight;
}

// Sends message if eneter is pressed
addEventListener('keydown', (e) => {
  if(e.key == "Enter" && document.getElementById("msg").value != "") {
    var value = document.getElementById("msg").value;
    document.getElementById("msg").value = "";
    
    e.preventDefault();
    $.getJSON("/send_message", { val: value }, function (data) {
      //do nothing
    });
    return false;
  }
})



