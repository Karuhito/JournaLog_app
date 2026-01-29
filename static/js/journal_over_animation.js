document.addEventListener("DOMContentLoaded", () => {
    const cards = document.querySelectorAll(".journal-card");

    cards.forEach((card, index) => {
        setTimeout(() => {
            card.classList.add("is-visible");
        }, index * 150); // 0.15秒ずつ遅らせる
    });
});