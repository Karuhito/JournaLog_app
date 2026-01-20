document.addEventListener("DOMContentLoaded", () => {

    // ==========================
    // DOM取得
    // ==========================
    const formsetContainer = document.getElementById("goal-formset");
    const addButton = document.getElementById("add-goal");
    const emptyFormTemplateEl = document.getElementById("goal-empty-form");

    const totalFormsInput = document.querySelector(
        'input[name="goal-TOTAL_FORMS"]'
    );

    // ==========================
    // 必須要素チェック
    // ==========================
    if (!formsetContainer) {
        console.error("goal-formset が見つかりません");
        return;
    }
    if (!addButton) {
        console.error("add-goal ボタンが見つかりません");
        return;
    }
    if (!emptyFormTemplateEl) {
        console.error("goal-empty-form が見つかりません");
        return;
    }
    if (!totalFormsInput) {
        console.error("goal-TOTAL_FORMS が見つかりません");
        return;
    }

    // ==========================
    // 初期設定
    // ==========================
    const emptyFormTemplate = emptyFormTemplateEl.innerHTML;

    // empty_form 内の input は最初は無効化（POSTに含めない）
    emptyFormTemplateEl
        .querySelectorAll("input")
        .forEach(el => el.disabled = true);

    // ==========================
    // 追加処理
    // ==========================
    addButton.addEventListener("click", () => {

        const formCount = parseInt(totalFormsInput.value, 10);

        // __prefix__ → index
        const newFormHtml = emptyFormTemplate.replace(
            /__prefix__/g,
            formCount
        );

        const tempDiv = document.createElement("div");
        tempDiv.innerHTML = newFormHtml;

        const newForm = tempDiv.firstElementChild;

        // disabled解除（これが超重要）
        newForm.querySelectorAll("input").forEach(el => {
            el.disabled = false;
        });

        formsetContainer.appendChild(newForm);

        // 🔥 Djangoが参照する唯一の数値
        totalFormsInput.value = formCount + 1;
    });

    // ==========================
    // 削除処理（UI用）
    // ※ TOTAL_FORMS は減らさない
    // ==========================
    formsetContainer.addEventListener("click", (e) => {
        if (e.target.classList.contains("remove-form")) {
            const form = e.target.closest(".goal-form");
            if (form) {
                // 入力を無効化してPOSTから除外
                form.querySelectorAll("input").forEach(el => {
                    el.disabled = true;
                });
                form.remove();
            }
        }
    });

});