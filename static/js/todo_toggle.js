function attachTodoToggle() {
  document.querySelectorAll(".todo-checkbox").forEach((checkbox) => {
      // 一度イベントリスナーを解除してから再アタッチ（重複防止）
      checkbox.replaceWith(checkbox.cloneNode(true));
      const newCheckbox = document.querySelector(`.todo-checkbox[data-todo-id='${checkbox.dataset.todoId}']`);

      newCheckbox.addEventListener("change", async () => {
          const todoId = newCheckbox.dataset.todoId;
          const row = newCheckbox.closest(".todo-item");

          try {
              const response = await fetch(`/journal/todo/toggle/${todoId}/`, {
                  method: "POST",
                  headers: {
                      "X-CSRFToken": getCsrfToken(),
                  },
              });

              const data = await response.json();

              if (!data.success) {
                  newCheckbox.checked = !newCheckbox.checked;
                  return;
              }

              // 完了状態の切替
              row.classList.toggle("is-done", data.is_done);

          } catch (error) {
              console.error(error);
              newCheckbox.checked = !newCheckbox.checked;
          }
      });
  });
}

function getCsrfToken() {
  return document.querySelector("[name=csrfmiddlewaretoken]").value;
}

// 初回ロード
document.addEventListener("DOMContentLoaded", attachTodoToggle);

// 戻るボタン・キャッシュ復帰時も再アタッチ
window.addEventListener("pageshow", function(event) {
  if (event.persisted || window.performance.navigation.type === 2) {
      attachTodoToggle();
  }
});