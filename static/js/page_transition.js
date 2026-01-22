document.addEventListener("DOMContentLoaded", () => {

    const links = document.querySelectorAll(
        ".calendar-cell a"
    );

    links.forEach(link => {
        link.addEventListener("click", (e) => {
            e.preventDefault();

            const url = link.getAttribute("href");
            const cell = link.closest(".calendar-cell");

            // セルをフォーカス状態に
            cell.classList.add("is-selected");

            // 画面遷移アニメーション
            document.body.classList.add("is-transitioning");

            // 少し待ってから遷移
            setTimeout(() => {
                window.location.href = url;
            }, 220);
        });
    });

});