document.addEventListener('DOMContentLoaded', function () {
    var mainAccordions = document.querySelectorAll('#accordionMain .collapse');
    mainAccordions.forEach(function (accordion) {
        accordion.addEventListener('show.bs.collapse', function () {
            mainAccordions.forEach(function (otherAccordion) {
                if (otherAccordion !== accordion) {
                    $(otherAccordion).collapse('hide');
                }
            });
        });
    });

    var nestedAccordions = document.querySelectorAll('.card-body .collapse');
    nestedAccordions.forEach(function (accordion) {
        accordion.addEventListener('show.bs.collapse', function () {
            var parentAccordion = accordion.closest('.collapse');
            var siblingAccordions = parentAccordion.querySelectorAll('.collapse');
            siblingAccordions.forEach(function (siblingAccordion) {
                if (siblingAccordion !== accordion) {
                    $(siblingAccordion).collapse('hide');
                }
            });
        });
    });
});