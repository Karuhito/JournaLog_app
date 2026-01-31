document.addEventListener('DOMContentLoaded', () => {

    function setupFormset({ addBtnId, formsetId, emptyFormId }) {
        const addBtn = document.getElementById(addBtnId);
        const formset = document.getElementById(formsetId);
        const emptyTemplate = document.getElementById(emptyFormId)?.innerHTML;

        if (!addBtn || !formset || !emptyTemplate) {
            console.error("Formset elements not found!", addBtn, formset, emptyTemplate);
            return;
        }

        // 追加ボタン
        addBtn.addEventListener('click', () => {
            const totalFormsInput = formset.querySelector('input[name$="-TOTAL_FORMS"]');
            if (!totalFormsInput) {
                console.error("TOTAL_FORMS input not found!");
                return;
            }

            const index = parseInt(totalFormsInput.value);
            const newFormHtml = emptyTemplate.replace(/__prefix__/g, index);

            formset.insertAdjacentHTML('beforeend', newFormHtml);
            totalFormsInput.value = index + 1;
        });

        // 削除ボタン
        formset.addEventListener('click', (e) => {
            if (!e.target.classList.contains('remove-form') && !e.target.closest('.remove-form')) return;

            const form = e.target.closest('.goal-form, .todo-form');
            if (!form) return;

            const deleteInput = form.querySelector('input[type="hidden"][name$="-DELETE"]');
            if (deleteInput) deleteInput.value = "on"; // Django に削除フラグ

            form.remove();
        });
    }

    setupFormset({ addBtnId: 'add-goal', formsetId: 'goal-formset', emptyFormId: 'goal-empty-form' });
    setupFormset({ addBtnId: 'add-todo', formsetId: 'todo-formset', emptyFormId: 'todo-empty-form' });

});