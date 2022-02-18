
$(".text-field").scrollTop($(".text-field")[0].scrollHeight);
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
window.onload = function() {
  setInterval(update, 100)
}


function update() {
  this.fetch("/get_messages")
    .then(function (response) {
      return response.json();
    })
    .then(function (dict) {
      $("#list").empty()
      var ul = document.getElementById("list");

      for (msg of dict["messages"]) {
        if (msg.substring(0, 6) == "SERVER") {
          handleServeralerts(msg)
        } else {
          var messageList = msg.split(":")
          var li = document.createElement("li");
        li.appendChild(document.createTextNode(messageList[0]));
        li.appendChild(document.createTextNode(messageList[1]));
        ul.appendChild(li);
        }
        
      }
    });
}


function handleServeralerts(msg) {
  var status = document.getElementById("status");
  status.classList.add('success')
  status.innerHTML = msg;
}