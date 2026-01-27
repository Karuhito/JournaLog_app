document.addEventListener("DOMContentLoaded", () => {
    const addButton = document.getElementById("add-todo");
    const formsetContainer = document.getElementById("todo-formset");
    const emptyFormTemplate = document.getElementById("todo-empty-form");
    const totalFormsInput = document.querySelector(
        "#id_todo_set-TOTAL_FORMS"
    );

    // フォーム追加
    addButton.addEventListener("click", () => {
        const formCount = parseInt(totalFormsInput.value);

        // empty_form を複製
        const newForm = emptyFormTemplate.cloneNode(true);
        newForm.classList.remove("d-none");
        newForm.removeAttribute("id");

        // __prefix__ を index に置換
        newForm.innerHTML = newForm.innerHTML.replace(
            /__prefix__/g,
            formCount
        );

        // formsetに追加
        formsetContainer.appendChild(newForm);

        // TOTAL_FORMS を更新
        totalFormsInput.value = formCount + 1;
    });

    // フォーム削除（イベントデリゲーション）
    formsetContainer.addEventListener("click", (e) => {
        const removeButton = e.target.closest(".remove-form");
        if (!removeButton) return;

        const formCard = removeButton.closest(".todo-form");
        if (!formCard) return;

        // 既存フォームなら DELETE にチェック
        const deleteInput = formCard.querySelector(
            'input[type="checkbox"][name$="-DELETE"]'
        );

        if (deleteInput) {
            deleteInput.checked = true;
            formCard.style.display = "none";
        } else {
            // 新規フォームならDOMから削除
            formCard.remove();
            totalFormsInput.value =
                parseInt(totalFormsInput.value) - 1;
        }
    });
});