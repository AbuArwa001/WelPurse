$(document).ready(function() {
    $('.join-btn').click(function(e) {
        e.preventDefault();
        var groupId = $(this).data('groupid');
        var memberId = $(this).data('memberid');
        $.ajax({
            url: 'http://127.0.0.1:5001/api/v1/join_group',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ welfare_id: groupId, member_id: memberId }),
            success: function(response) {
                // Update the modal body with the success message and show the modal
                $('#customAlertModal .modal-body').text('You have successfully become a contributor!');
                $('#customAlertModal').modal('show');
                $(e.target).remove(); // Optionally remove the join button after successful join
            },
            error: function(xhr, status, error) {
                // Update the modal body with the error message and show the modal
                $('#customAlertModal .modal-body').text('An error occurred: ' + error);
                $('#customAlertModal').modal('show');
            }
        });
    });
});
