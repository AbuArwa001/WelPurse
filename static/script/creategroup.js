var currentTab = 0; // Current tab is set to be the first tab (0)
showTab(currentTab); // Display the current tab

function showTab(n) {
  // This function will display the specified tab of the form...
  var x = $(".tab");
  $(x[n]).show();
  // ... and fix the Previous/Next buttons:
  if (n == 0) {
    $("#prevBtn").hide();
  } else {
    $("#prevBtn").show();
  }
  if (n == (x.length - 1)) {
    $("#nextBtn").text("Submit");
  } else {
    $("#nextBtn").text("Next");
  }
  // ... and run a function that displays the correct step indicator:
  fixStepIndicator(n);
}

function nextPrev(n) {
  // This function will figure out which tab to display
  var x = $(".tab");
  // Exit the function if any field in the current tab is invalid:
  if (n == 1 && !validateForm()) return false;
  // Hide the current tab:
  $(x[currentTab]).hide();
  // Increase or decrease the current tab by 1:
  currentTab = currentTab + n;
  // if you have reached the end of the form... :
  if (currentTab >= x.length) {
    //...the form gets submitted:
    $("#regForm").submit();
    return false;
  }
  // Otherwise, display the correct tab:
  showTab(currentTab);
}

function validateForm() {
  // This function deals with validation of the form fields
  var x, y, i, valid = true;
  x = $(".tab");
  y = $(x[currentTab]).find("input");
  // A loop that checks every input field in the current tab:
  for (i = 0; i < y.length; i++) {
    // If a field is empty...
    if ($(y[i]).val() == "") {
      // add an "invalid" class to the field:
      $(y[i]).addClass("invalid");
      // and set the current valid status to false:
      valid = false;
    }
  }
  // If the valid status is true, mark the step as finished and valid:
  if (valid) {
    $(".step").eq(currentTab).addClass("finish");
  }
  return valid; // return the valid status
}

function fixStepIndicator(n) {
  // This function removes the "active" class of all steps...
  var x = $(".step");
  x.removeClass("active");
  //... and adds the "active" class to the current step:
  x.eq(n).addClass("active");
}
