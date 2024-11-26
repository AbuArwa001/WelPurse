$(document).ready(function() {
    window.openFormRequest = function openFormRequest(userId, welfareId) {
      $('input[name="welfare_id"]').val(welfareId);
      $('input[name="member_id"]').val(userId);
    }
  });

  $(document).ready(function() {
    // Get the modal
    var modal = document.getElementById("createEventModal");
  
    // Get the button that opens the modal
    var btns = document.getElementsByClassName("create-event-btn");
  
    // Get the <span> element that closes the modal
    var span = document.getElementsByClassName("close")[0];
  
    // When the user clicks on a button, open the modal and fill the form
    Array.prototype.forEach.call(btns, function(btn) {
      btn.onclick = function() {
        var welfareGroupName = $(this).data("welfare-group-name");
        var amountRequested = $(this).data("amount-requested");
        var donationPurpose = $(this).data("donation-purpose");
        var welfareId = $(this).data("welfare-id");
        var requestId = $(this).data("request-id");
  
        $("#createEventForm input[name='welfare_group_name']").val(welfareGroupName);
        $("#createEventForm input[name='target_amount']").val(amountRequested);
        $("#createEventForm textarea[name='donation_purpose']").val(donationPurpose);
        $("#createEventForm input[name='requestId']").val(requestId);
        $("#createEventForm input[name='welfare_id']").val(welfareId);
  
        // Set default values for event dates
        var currentDate = new Date().toISOString().slice(0, 10);
        var endDate = new Date();
        endDate.setDate(endDate.getDate() + 7);
        endDate = endDate.toISOString().slice(0, 10);
  
        $("#createEventForm input[name='event_date']").val(currentDate);
        $("#createEventForm input[name='start_date']").val(currentDate);
        $("#createEventForm input[name='end_date']").val(endDate);
  
        console.log("welfareGroupName:", welfareGroupName);
        console.log("amountRequested:", amountRequested);
        console.log("donationPurpose:", donationPurpose);
        console.log("requestId:", requestId);
        console.log("welfareId:", welfareId);
        
        modal.style.display = "block";
      };
    });
  
    // When the user clicks on <span> (x), close the modal
    span.onclick = function() {
      modal.style.display = "none";
    };
  
    // When the user clicks anywhere outside of the modal, close it
    window.onclick = function(event) {
      if (event.target == modal) {
        modal.style.display = "none";
      }
    };
  });