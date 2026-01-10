document.addEventListener("DOMContentLoaded", function() {
    const formset = document.getElementById("goal-formset");
    const addButton = document.getElementById("add-goal");
    const totalForms = document.querySelector('#id_form-TOTAL_FORMS');

    // 空フォームのテンプレートを作成
    const emptyForm = formset.firstElementChild.cloneNode(true);
    // 中身をクリア
    emptyForm.querySelectorAll('input').forEach(input => {
        if (input.type === 'checkbox') input.checked = false;
        else input.value = '';
    });

    // 削除ボタンのクリックイベント
    formset.addEventListener("click", function(e) {
        if (e.target && e.target.classList.contains("remove-form")) {
            e.target.closest(".goal-form").remove();
            updateFormIndices();
        }
    });

    // 追加ボタンのクリックイベント
    addButton.addEventListener("click", function() {
        const newForm = emptyForm.cloneNode(true);
        formset.appendChild(newForm);
        updateFormIndices();
    });

    // フォーム番号を更新する関数
    function updateFormIndices() {
        const forms = formset.querySelectorAll(".goal-form");
        forms.forEach((form, index) => {
            form.querySelectorAll("input").forEach(input => {
                const name = input.name.replace(/\d+/, index);
                const id = input.id.replace(/\d+/, index);
                input.name = name;
                input.id = id;
            });
        });
        totalForms.value = forms.length;
    }
});