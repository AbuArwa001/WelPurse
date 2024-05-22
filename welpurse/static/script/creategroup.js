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
          if (idx <= currentStep) {
              $(step).addClass('progress-step-active');
          } else {
              $(step).removeClass('progress-step-active');
          }
      });
      progress.css('width', ((currentStep + 1) / progressSteps.length) * 100 + '%');
  }
});
