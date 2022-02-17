$(".text-field").scrollTop($(".text-field")[0].scrollHeight);

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

window.onload = function () {
  var update_loop = this.setInterval(update, 100);
  update();
};

function update() {
  this.fetch("/get_messages")
    .then(function (response) {
      
      return response.json();
    })
    .then(function (dict) {
      var messages = ""
      for (msg of dict["messages"]) {
        messages = messages + "<br>" + msg
        
      }
      document.getElementById("test").innerHTML = messages;
    });
}
