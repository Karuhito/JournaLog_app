console.log("journal.js loaded");
document.addEventListener('DOMContentLoaded', () => {

    function setupFormset({
        addBtnId,
        formsetId,
        emptyFormId,
        totalFormsId,
        formClass
    }) {
        const addBtn = document.getElementById(addBtnId);
        const formset = document.getElementById(formsetId);
        const emptyFormTemplate = document.getElementById(emptyFormId).innerHTML;
        const totalForms = document.getElementById(totalFormsId);

        // 追加
        addBtn.addEventListener('click', () => {
            let formCount = parseInt(totalForms.value);

            let newFormHtml = emptyFormTemplate.replace(/__prefix__/g, formCount);
            formset.insertAdjacentHTML('beforeend', newFormHtml);

            totalForms.value = formCount + 1;
        });

        // 削除
        formset.addEventListener('click', (e) => {
            if (e.target.classList.contains('remove-form')) {
                e.target.closest(formClass).remove();
                totalForms.value = parseInt(totalForms.value) - 1;
            }
        });
    }

    // Todo
    setupFormset({
        addBtnId: 'add-todo',
        formsetId: 'todo-formset',
        emptyFormId: 'todo-empty-form',
        totalFormsId: 'id_todo-TOTAL_FORMS',
        formClass: '.todo-form'
    });

    // Goal
    setupFormset({
        addBtnId: 'add-goal',
        formsetId: 'goal-formset',
        emptyFormId: 'goal-empty-form',
        totalFormsId: 'id_goal-TOTAL_FORMS',
        formClass: '.goal-form'
    });
});