
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

