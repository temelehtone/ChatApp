$(function() {
    $('#test').on('click', function(e) {
      e.preventDefault()
      $.getJSON('/run',
          function(data) {
        //do nothing
      });
      return false;
    });
  });