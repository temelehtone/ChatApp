

$('.text-field').scrollTop($('.text-field')[0].scrollHeight);



$(function() {
    $('#test').on('click', function(e) {
      e.preventDefault()
      $.getJSON('/add_msg',
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