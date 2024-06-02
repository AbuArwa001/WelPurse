$(document).ready(function() {
    window.openForm = function openForm(eventId, eventName, amount, description, welfareId) {
      $("#popupForm").css("display", "flex");
      $('input[name="welfare_group"]').val(eventName);
      $('input[name="amount"]').val(amount);
      $('textarea[name="event_description"]').val(description);
      $('input[name="welfare_id"]').val(welfareId);
      $('input[name="event_id"]').val(eventId);
    }
    

    window.closeForm = function closeForm() {
      $("#popupForm").css("display", "none");
    }

    // You can also bind events inside the ready function
    // For example, if you have a button to open the form:
    $('#openFormButton').click(function() {
      openForm('Event Name', '100', 'This is a description.');
    });

    // And a button to close the form:
    $('#closeFormButton').click(function() {
      closeForm();
    });
  });
  $(document).ready(function() {
    var $contributeButton = $('#contribute-button');
    var $mpesaNumber = $('#mpesa-number');

    $('#payment-method').change(function() {
        var selectedMethod = $(this).val();

        // Toggle MPesa number input
        if (selectedMethod === 'mpesa') {
            $mpesaNumber.show();
        } else {
            $mpesaNumber.hide();
        }

        // Toggle contribute button functionality
        if (selectedMethod === 'credit_card') {
            $contributeButton.addClass('intaSendPayButton').show();
        } else {
            $contributeButton.removeClass('intaSendPayButton').hide();
        }
    });
});
