document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll("[data-feature]").forEach(section => {
      const formset = section.querySelector("[data-formset]");
      const emptyForm = section.querySelector("[data-empty-form]");
      const addBtn = section.querySelector("[data-add-btn]");
      const totalFormsInput = formset.querySelector(
        'input[name$="-TOTAL_FORMS"]'
      );
  
      if (!addBtn || !formset || !emptyForm || !totalFormsInput) return;
  
      addBtn.addEventListener("click", () => {
        const formCount = parseInt(totalFormsInput.value, 10);
        const newFormHtml = emptyForm.innerHTML.replace(
          /__prefix__/g,
          formCount
        );
  
        const wrapper = document.createElement("div");
        wrapper.innerHTML = newFormHtml;
        formset.appendChild(wrapper.firstElementChild);
  
        totalFormsInput.value = formCount + 1;
      });
  
      formset.addEventListener("click", e => {
        if (e.target.closest(".remove-form")) {
          e.target.closest(".journal-input-card").remove();
        }
      });
    });
  });