document.addEventListener('DOMContentLoaded', function () {
    // Function to dynamically add a new inline form
    function addForm(button, prefix) {
        var totalFormsInput = document.getElementById(`id_${prefix}-TOTAL_FORMS`);
        var totalForms = parseInt(totalFormsInput.value, 10);
        var emptyForm = document.getElementById(`${prefix}-empty-form`).cloneNode(true);
        emptyForm.id = `${prefix}-${totalForms}`;
        emptyForm.innerHTML = emptyForm.innerHTML.replace(/__prefix__/g, totalForms);
        emptyForm.style.display = 'block';

        // Insert the new form before the add button
        var addButtonRow = button.closest('.add-row');
        addButtonRow.before(emptyForm);

        // Increment the total forms count
        totalFormsInput.value = totalForms + 1;
    }

    // Function to dynamically remove an inline form
    function removeForm(button) {
        var form = button.closest('.inline-related');
        form.style.display = 'none';
        var deleteInput = form.querySelector('input[name$="-DELETE"]');
        deleteInput.checked = true;
    }

    // Add event listeners for the add buttons
    document.querySelectorAll('.add-row a').forEach(function (addButton) {
        addButton.addEventListener('click', function (event) {
            event.preventDefault();
            var prefix = this.dataset.prefix;
            addForm(this, prefix);
        });
    });

    // Add event listeners for the delete buttons
    document.querySelectorAll('.inline-deletelink').forEach(function (deleteButton) {
        deleteButton.addEventListener('click', function (event) {
            event.preventDefault();
            removeForm(this);
        });
    });
});