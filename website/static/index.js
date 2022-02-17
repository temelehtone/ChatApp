

$('.text-field').scrollTop($('.text-field')[0].scrollHeight);



$(function() {
    $('#sendBtn').on('click', function(e) {
      var value = document.getElementById("msg").value
      e.preventDefault()
      $.getJSON('/send_message',
          {val: value},
          function(data) {
        //do nothing
      });
      return false;
    });
  });


function validate(name) {
    if (name.length >= 2) {
        return true
    }
    return false
}