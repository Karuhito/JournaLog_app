// timeset_rule.js
document.addEventListener("DOMContentLoaded", () => {
    console.log("timeset_rule.js 実行");
  
    // start/endの同期・制約を設定する関数
    function setTimeRules(scheduleRow) {
      const startSelect = scheduleRow.querySelector('select[name$="start_time"]');
      const endSelect = scheduleRow.querySelector('select[name$="end_time"]');
  
      if (!startSelect || !endSelect) return;
  
      function updateEndOptions() {
        const startValue = startSelect.value;
  
        // end_time の option を制御
        Array.from(endSelect.options).forEach(option => {
          if (option.value < startValue) {
            option.disabled = true;
          } else {
            option.disabled = false;
          }
        });
  
        // 現在の end_time が start_time より前なら同期
        if (endSelect.value < startValue) {
          endSelect.value = startValue;
        }
      }
  
      // 初期状態の制御
      updateEndOptions();
  
      // start_time が変更されたら end_time を制御
      startSelect.addEventListener("change", () => {
        updateEndOptions();
      });
    }
  
    // 既存の schedule-fields に適用
    document.querySelectorAll(".schedule-fields").forEach(setTimeRules);
  
    // 追加フォームが出てきたら自動で制御
    const formsetContainer = document.querySelector('[data-formset]');
    if (formsetContainer) {
      const observer = new MutationObserver(mutations => {
        mutations.forEach(mutation => {
          mutation.addedNodes.forEach(node => {
            if (node.nodeType === 1 && node.querySelector(".schedule-fields")) {
              setTimeRules(node.querySelector(".schedule-fields"));
            }
          });
        });
      });
  
      observer.observe(formsetContainer, { childList: true, subtree: true });
    }
  });