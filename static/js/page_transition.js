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

document.addEventListener('DOMContentLoaded', () => {
    // すべてのドロップダウンに適用
    document.querySelectorAll('.dropdown').forEach(dropdown => {
      const menu = dropdown.querySelector('.dropdown-menu');
  
      // 初期状態でスライドクラスを付与
      menu.classList.add('slide');
  
      // showイベント → メニュー展開
      dropdown.addEventListener('show.bs.dropdown', () => {
        menu.classList.add('show');
      });
  
      // hideイベント → メニューを閉じる
      dropdown.addEventListener('hide.bs.dropdown', e => {
        e.preventDefault(); // 即時閉鎖を止める
        menu.classList.remove('show');
  
        // トランジション完了後にBootstrapで正式に閉じる
        const handler = () => {
          bootstrap.Dropdown.getOrCreateInstance(dropdown).hide();
          menu.removeEventListener('transitionend', handler);
        };
        menu.addEventListener('transitionend', handler);
      });
    });
  });