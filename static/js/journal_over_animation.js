function runJournalOverAnimation() {
    const cards = document.querySelectorAll(".journal-card");

    cards.forEach((card, index) => {
        setTimeout(() => {
            card.classList.add("is-visible");
        }, index * 150); // 0.15秒ずつ遅らせる
    });
}

// 初回ロード
document.addEventListener("DOMContentLoaded", runJournalOverAnimation);

// 戻るボタン・キャッシュ復帰時も再実行
window.addEventListener("pageshow", function(event) {
    if (event.persisted || window.performance.navigation.type === 2) {
        runJournalOverAnimation();
    }
});