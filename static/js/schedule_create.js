document.addEventListener("DOMContentLoaded", () => {

    const formsetContainer = document.getElementById("schedule-formset");
    const addButton = document.getElementById("add-schedule");
    const emptyFormTemplate = document.getElementById("schedule-empty-form").innerHTML;

    // management form
    const totalFormsInput = document.querySelector(
        'input[name="form-TOTAL_FORMS"]'
    );

    // ==========================
    // 追加処理
    // ==========================
    addButton.addEventListener("click", () => {
        const formCount = parseInt(totalFormsInput.value);

        let newFormHtml = emptyFormTemplate.replace(/__prefix__/g, formCount);

        const tempDiv = document.createElement("div");
        tempDiv.innerHTML = newFormHtml;

        formsetContainer.appendChild(tempDiv.firstElementChild);

        totalFormsInput.value = formCount + 1;
    });

    // ==========================
    // 削除処理（イベント委譲）
    // ==========================
    formsetContainer.addEventListener("click", (e) => {
        if (e.target.classList.contains("remove-form")) {
            const scheduleForm = e.target.closest(".schedule-form");
            scheduleForm.remove();
            updateTotalForms();
        }
    });

    // ==========================
    // TOTAL_FORMS 再計算
    // ==========================
    function updateTotalForms() {
        const forms = formsetContainer.querySelectorAll(".schedule-form");
        totalFormsInput.value = forms.length;

        forms.forEach((form, index) => {
            const inputs = form.querySelectorAll("input, select, textarea, label");

            inputs.forEach(el => {
                if (el.name) {
                    el.name = el.name.replace(/form-\d+-/, `form-${index}-`);
                }
                if (el.id) {
                    el.id = el.id.replace(/form-\d+-/, `form-${index}-`);
                }
                if (el.htmlFor) {
                    el.htmlFor = el.htmlFor.replace(/form-\d+-/, `form-${index}-`);
                }
            });
        });
    }

});