
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




