$(document).ready(function () {
  var steps = $('.form-step');
  var nextBtn = $('.btn-next');
  var prevBtn = $('.btn-prev');
  var progress = $('#progress');
  var progressSteps = $('.progress-step');

  var currentStep = 0;

  nextBtn.click(function () {
      currentStep++;
      updateFormSteps();
      updateProgressBar();
  });

  prevBtn.click(function () {
      currentStep--;
      updateFormSteps();
      updateProgressBar();
  });

  function updateFormSteps() {
      steps.removeClass('form-step-active');
      steps.eq(currentStep).addClass('form-step-active');
  }

  function updateProgressBar() {
      progressSteps.each(function (idx, step) {
        console.log("INDEX",idx)
        console.log("CURRENT STEP",currentStep)
        if (idx <= currentStep) {
            $(step).addClass('progress-step-active');
        } else {
            $(step).removeClass('progress-step-active');
        }
    });
    console.log("PROGRESS STEPS",progressSteps.length)
    var newWidth = (currentStep / (progressSteps.length - 1)) * 100;
    console.log("NEW WIDTH", newWidth)
    progress.css('width', newWidth + '%');
  }
});

$(document).ready(function() {
    $('form').on('submit', function(e) {
      // Custom validation logic here
      if (!this.checkValidity()) {
        e.preventDefault(); // Prevent form submission
        // Focus on the first invalid input
        $(this).find(':input:invalid').first().focus();
      }
    });
  });