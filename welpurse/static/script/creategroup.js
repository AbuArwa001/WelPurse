$(document).ready(function() {
  let formStepsNum = 0;

  $(".btn-next").on("click", function() {
    formStepsNum++;
    updateFormSteps();
    updateProgressbar();
  });

  $(".btn-prev").on("click", function() {
    formStepsNum--;
    updateFormSteps();
    updateProgressbar();
  });

  function updateFormSteps() {
    $(".form-step").each(function() {
      $(this).removeClass("form-step-active");
    });
    $(".form-step").eq(formStepsNum).addClass("form-step-active");
  }

  function updateProgressbar() {
    $(".progress-step").each(function(idx) {
      if (idx < formStepsNum + 1) {
        $(this).addClass("progress-step-active");
      } else {
        $(this).removeClass("progress-step-active");
      }
    });

    const progressActive = $(".progress-step-active").length;
    const progressTotal = $(".progress-step").length;
    const progressWidth = ((progressActive - 1) / (progressTotal - 1)) * 100;

    $("#progress").css("width", progressWidth + "%");
  }
});
