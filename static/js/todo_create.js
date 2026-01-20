document.addEventListener("DOMContentLoaded", () => {

    const formsetContainer = document.getElementById("todo-formset");
    const addButton = document.getElementById("add-todo");
    const emptyFormTemplateEl = document.getElementById("todo-empty-form");

    const totalFormsInput = document.querySelector(
        'input[name="todo-TOTAL_FORMS"]'
    );

    if (!formsetContainer || !addButton || !emptyFormTemplateEl || !totalFormsInput) {
        console.error("todo_create.js: 必要な要素が見つかりません");
        return;
    }

    const emptyFormTemplate = emptyFormTemplateEl.innerHTML;

    // ------------------
    // 追加
    // ------------------
    addButton.addEventListener("click", () => {
        const formCount = parseInt(totalFormsInput.value, 10);

        const newFormHtml = emptyFormTemplate.replace(
            /__prefix__/g,
            formCount
        );

        const tempDiv = document.createElement("div");
        tempDiv.innerHTML = newFormHtml;

        const newForm = tempDiv.firstElementChild;

        // disabled解除（empty_form対策）
        newForm.querySelectorAll("input").forEach(el => {
            el.disabled = false;
        });

        formsetContainer.appendChild(newForm);

        totalFormsInput.value = formCount + 1;
    });

    // ------------------
    // 削除
    // ------------------
    formsetContainer.addEventListener("click", (e) => {
        if (e.target.classList.contains("remove-form")) {
            const form = e.target.closest(".todo-form");
            if (form) {
                form.remove();
                updateTotalForms();
            }
        }
    });

    function updateTotalForms() {
        const forms = formsetContainer.querySelectorAll(".todo-form");
        totalFormsInput.value = forms.length;

        forms.forEach((form, index) => {
            form.querySelectorAll("input, label").forEach(el => {
                if (el.name) {
                    el.name = el.name.replace(/todo-\d+-/, `todo-${index}-`);
                }
                if (el.id) {
                    el.id = el.id.replace(/todo-\d+-/, `todo-${index}-`);
                }
                if (el.htmlFor) {
                    el.htmlFor = el.htmlFor.replace(/todo-\d+-/, `todo-${index}-`);
                }
            });
        });
    }
});