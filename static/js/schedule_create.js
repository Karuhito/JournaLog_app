document.addEventListener("DOMContentLoaded", () => {
    console.log("schedule_create.js loaded");

    const formsetContainer = document.getElementById("schedule-formset");
    const addButton = document.getElementById("add-schedule");
    const emptyFormTemplateEl = document.getElementById("schedule-empty-form");

    if (!formsetContainer || !addButton || !emptyFormTemplateEl) {
        console.error("schedule_create.js: 必要な要素が見つかりません");
        return;
    }

    const emptyFormTemplate = emptyFormTemplateEl.innerHTML;
    const totalFormsInput = document.querySelector('input[name="schedule-TOTAL_FORMS"]');
    if (!totalFormsInput) {
        console.error("schedule-TOTAL_FORMS が見つかりません");
        return;
    }

    // ==========================
    // 追加ボタン処理
    // ==========================
    addButton.addEventListener("click", () => {
        const formCount = parseInt(totalFormsInput.value, 10);

        const tempDiv = document.createElement("div");
        tempDiv.innerHTML = emptyFormTemplate.replace(/__prefix__/g, formCount);

        const newForm = tempDiv.firstElementChild;
        // disabled解除（もし空フォームに disabled がある場合）
        newForm.querySelectorAll("select, input").forEach(el => el.disabled = false);

        formsetContainer.appendChild(newForm);

        totalFormsInput.value = formCount + 1;
    });

    // ==========================
    // 削除ボタン処理
    // ==========================
    formsetContainer.addEventListener("click", e => {
        if (e.target.classList.contains("remove-form")) {
            const form = e.target.closest(".schedule-form");
            if (form) {
                form.remove();
                updateTotalForms();
            }
        }
    });

    // ==========================
    // start_time 自動補完 + 制限
    // ==========================
    formsetContainer.addEventListener("change", e => {
        if (e.target.classList.contains("time-select") && e.target.name.includes("start_time")) {
            const startSelect = e.target;
            const form = startSelect.closest(".schedule-form");
            const endSelect = form.querySelector("select[name*='end_time']");

            if (endSelect) {
                // 開始時刻を自動で終了時刻にセット
                endSelect.value = startSelect.value;

                // 終了時刻の選択肢制限（開始時刻より前は無効化）
                Array.from(endSelect.options).forEach(option => {
                    if (option.value < startSelect.value) {
                        option.disabled = true;
                    } else {
                        option.disabled = false;
                    }
                });
            }
        }
    });

    // ==========================
    // TOTAL_FORMS & index振り直し
    // ==========================
    function updateTotalForms() {
        const forms = formsetContainer.querySelectorAll(".schedule-form");
        totalFormsInput.value = forms.length;

        forms.forEach((form, index) => {
            const elements = form.querySelectorAll("input, select, textarea, label");
            elements.forEach(el => {
                if (el.name) el.name = el.name.replace(/schedule-\d+-/, `schedule-${index}-`);
                if (el.id) el.id = el.id.replace(/schedule-\d+-/, `schedule-${index}-`);
                if (el.htmlFor) el.htmlFor = el.htmlFor.replace(/schedule-\d+-/, `schedule-${index}-`);
            });
        });
    }
});