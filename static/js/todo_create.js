document.addEventListener("DOMContentLoaded", function() {
    const formset = document.getElementById("todo-formset");
    const addButton = document.getElementById("add-todo");
    const totalForms = document.querySelector('#id_form-TOTAL_FORMS');

    const emptyForm = formset.firstElementChild.cloneNode(true);
    emptyForm.querySelectorAll('input, select').forEach(input => {
        if (input.type === 'checkbox') input.checked = false;
        else input.value = '';
    });

    // 削除ボタン
    formset.addEventListener("click", function(e) {
        if (e.target && e.target.classList.contains("remove-form")) {
            e.target.closest(".todo-form").remove();
            updateFormIndices();
        }
    });

    // 追加ボタン
    addButton.addEventListener("click", function() {
        const newForm = emptyForm.cloneNode(true);
        formset.appendChild(newForm);
        updateFormIndices();
    });

    function updateFormIndices() {
        const forms = formset.querySelectorAll(".todo-form");
        forms.forEach((form, index) => {
            form.querySelectorAll("input, select").forEach(input => {
                const name = input.name.replace(/\d+/, index);
                const id = input.id.replace(/\d+/, index);
                input.name = name;
                input.id = id;
            });
        });
        totalForms.value = forms.length;
    }
});