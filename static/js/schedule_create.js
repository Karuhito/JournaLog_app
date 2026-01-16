document.addEventListener("DOMContentLoaded", () => {

    // ==========================
    // DOM取得
    // ==========================
    const formsetContainer = document.getElementById("schedule-formset");
    const addButton = document.getElementById("add-schedule");
    const emptyFormTemplateEl = document.getElementById("schedule-empty-form");

    if (!formsetContainer || !addButton || !emptyFormTemplateEl) {
        console.error("schedule_create.js: 必要な要素が見つかりません");
        return;
    }

    const emptyFormTemplate = emptyFormTemplateEl.innerHTML;

    // ==========================
    // management form（prefix = schedule）
    // ==========================
    const totalFormsInput = document.querySelector(
        'input[name="schedule-TOTAL_FORMS"]'
    );

    if (!totalFormsInput) {
        console.error("schedule-TOTAL_FORMS が見つかりません");
        return;
    }

    // ==========================
    // 追加処理
    // ==========================
    addButton.addEventListener("click", () => {
        const formCount = parseInt(totalFormsInput.value, 10);

        // __prefix__ を index に置換
        const newFormHtml = emptyFormTemplate.replace(
            /__prefix__/g,
            formCount
        );

        const tempDiv = document.createElement("div");
        tempDiv.innerHTML = newFormHtml;

        formsetContainer.appendChild(tempDiv.firstElementChild);

        // TOTAL_FORMS 更新
        totalFormsInput.value = formCount + 1;
    });

    // ==========================
    // 削除処理（イベント委譲）
    // ==========================
    formsetContainer.addEventListener("click", (e) => {
        if (e.target.classList.contains("remove-form")) {
            const scheduleForm = e.target.closest(".schedule-form");
            if (scheduleForm) {
                scheduleForm.remove();
                updateTotalForms();
            }
        }
    });

    // ==========================
    // TOTAL_FORMS 再計算 & index振り直し
    // ==========================
    function updateTotalForms() {
        const forms = formsetContainer.querySelectorAll(".schedule-form");
        totalFormsInput.value = forms.length;

        forms.forEach((form, index) => {
            const elements = form.querySelectorAll(
                "input, select, textarea, label"
            );

            elements.forEach(el => {
                if (el.name) {
                    el.name = el.name.replace(
                        /schedule-\d+-/,
                        `schedule-${index}-`
                    );
                }
                if (el.id) {
                    el.id = el.id.replace(
                        /schedule-\d+-/,
                        `schedule-${index}-`
                    );
                }
                if (el.htmlFor) {
                    el.htmlFor = el.htmlFor.replace(
                        /schedule-\d+-/,
                        `schedule-${index}-`
                    );
                }
            });
        });
    }

});