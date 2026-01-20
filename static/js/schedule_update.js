document.addEventListener("DOMContentLoaded", () => {
    const formContainer = document.querySelector(".card-body form");

    if (!formContainer) {
        console.error("schedule_update.js: フォームが見つかりません");
        return;
    }

    const startTime = formContainer.querySelector("select[name$='start_time']");
    const endTime = formContainer.querySelector("select[name$='end_time']");

    if (!startTime || !endTime) {
        console.error("schedule_update.js: start_time または end_time が見つかりません");
        return;
    }

    // 開始時刻が変更されたら終了時刻の選択肢を制限
    startTime.addEventListener("change", () => {
        Array.from(endTime.options).forEach(opt => {
            opt.disabled = opt.value < startTime.value;
        });

        // 終了時刻が開始時刻より前なら開始時刻に合わせる
        if (endTime.value < startTime.value) {
            endTime.value = startTime.value;
        }
    });

    // ページロード時にも制約を適用
    Array.from(endTime.options).forEach(opt => {
        opt.disabled = opt.value < startTime.value;
    });
});