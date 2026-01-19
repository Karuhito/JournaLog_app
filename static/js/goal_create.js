document.addEventListener("DOMContentLoaded", () => {

    const formsetContainer = document.getElementById("goal-formset");
    const addButton = document.getElementById("add-goal");
    const emptyFormTemplateEl = document.getElementById("goal-empty-form");

    const totalFormsInput = document.querySelector(
        'input[name="goal-TOTAL_FORMS"]'
    );

    if (!formsetContainer || !addButton || !emptyFormTemplateEl || !totalFormsInput) {
        console.error("goal_create.js: 必要な要素が見つかりません");
        return;
    }

    const emptyFormTemplate = emptyFormTemplateEl.innerHTML;

    // ==========================
    // 追加
    // ==========================
    addButton.addEventListener("click", () => {
        const formCount = parseInt(totalFormsInput.value, 10);

        const newFormHtml = emptyFormTemplate.replace(
            /__prefix__/g,
            formCount
        );

        const tempDiv = document.createElement("div");
        tempDiv.innerHTML = newFormHtml;

        const newForm = tempDiv.firstElementChild;

        // disabled を解除
        newForm.querySelectorAll("input").forEach(el => {
            el.disabled = false;
        });

        formsetContainer.appendChild(newForm);

        // ⭐ これが最重要
        totalFormsInput.value = formCount + 1;
    });

    // ==========================
    // 削除
    // ==========================
    formsetContainer.addEventListener("click", (e) => {
        if (e.target.classList.contains("remove-form")) {
            const form = e.target.closest(".goal-form");
            if (form) {
                form.remove();
                renumberForms();
            }
        }
    });

    function renumberForms() {
        const forms = formsetContainer.querySelectorAll(".goal-form");
        totalFormsInput.value = forms.length;

        forms.forEach((form, index) => {
            form.querySelectorAll("input, label").forEach(el => {
                if (el.name) {
                    el.name = el.name.replace(/goal-\d+-/, `goal-${index}-`);
                }
                if (el.id) {
                    el.id = el.id.replace(/goal-\d+-/, `goal-${index}-`);
                }
                if (el.htmlFor) {
                    el.htmlFor = el.htmlFor.replace(/goal-\d+-/, `goal-${index}-`);
                }
            });
        });
    }
});