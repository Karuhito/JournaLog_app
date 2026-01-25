document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".todo-checkbox").forEach((checkbox) => {
      checkbox.addEventListener("change", async () => {
        const todoId = checkbox.dataset.todoId;
        const row = checkbox.closest(".todo-item");
  
        try {
          const response = await fetch(
            `/journal/todo/toggle/${todoId}/`,
            {
              method: "POST",
              headers: {
                "X-CSRFToken": getCsrfToken(),
              },
            }
          );
  
          const data = await response.json();
  
          if (!data.success) {
            checkbox.checked = !checkbox.checked;
            return;
          }
  
          // ★ ここが核心
          row.classList.toggle("is-done", data.is_done);
  
        } catch (error) {
          console.error(error);
          checkbox.checked = !checkbox.checked;
        }
      });
    });
  });
  
  function getCsrfToken() {
    return document.querySelector("[name=csrfmiddlewaretoken]").value;
  }