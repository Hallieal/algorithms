(() => {
  "use strict";

  function answerLabels() {
    const isRussian = document.documentElement.lang.toLowerCase().startsWith("ru");
    return isRussian
      ? { show: "Показать ответ", hide: "Скрыть ответ" }
      : { show: "Show answer", hide: "Hide answer" };
  }

  function setupReveals() {
    const labels = answerLabels();
    document.addEventListener("click", event => {
      const button = event.target.closest("button[data-reveal]");
      if (!button) return;

      const target = document.getElementById(button.dataset.reveal);
      if (!target) return;

      target.hidden = !target.hidden;
      button.setAttribute("aria-expanded", String(!target.hidden));
      button.textContent = target.hidden ? labels.show : labels.hide;
    });
  }

  function setupSidebar() {
    const sidebarLinks = [...document.querySelectorAll(".sidebar a")];
    const sections = sidebarLinks
      .map(link => document.querySelector(link.getAttribute("href")))
      .filter(Boolean);

    if (!("IntersectionObserver" in window) || !sections.length) return;

    const observer = new IntersectionObserver(entries => {
      const visible = entries
        .filter(entry => entry.isIntersecting)
        .sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0];

      if (!visible) return;
      sidebarLinks.forEach(link => link.classList.remove("active"));
      const current = sidebarLinks.find(
        link => link.getAttribute("href") === `#${visible.target.id}`
      );
      if (current) current.classList.add("active");
    }, {
      rootMargin: "-20% 0px -65% 0px",
      threshold: [0, 0.1, 0.3, 0.6]
    });

    sections.forEach(section => observer.observe(section));
  }

  function setupProgress() {
    const progress = document.getElementById("reading-progress");
    if (!progress) return;

    const update = () => {
      const height = document.documentElement.scrollHeight - window.innerHeight;
      const ratio = height > 0 ? window.scrollY / height : 0;
      progress.style.width = `${Math.max(0, Math.min(1, ratio)) * 100}%`;
    };

    update();
    window.addEventListener("scroll", update, { passive: true });
    window.addEventListener("resize", update);
  }

  function mountStepper(root, options) {
    if (!root) return;

    const {
      initial,
      build,
      render,
      randomize = null,
      store = "_states",
      nextAction = "next",
      resetAction = "reset",
      randomizeAction = "randomize"
    } = options;

    const reset = data => {
      root[store] = build(data);
      root._index = 0;
      render(root);
    };

    reset(initial);

    root.addEventListener("click", event => {
      const button = event.target.closest("button[data-action]");
      if (!button) return;
      const action = button.dataset.action;

      if (action === nextAction) {
        root._index = Math.min(root._index + 1, root[store].length - 1);
        render(root);
      } else if (action === resetAction) {
        reset(initial);
      } else if (randomize && action === randomizeAction) {
        reset(randomize());
      }
    });
  }

  window.LectureCore = { mountStepper };

  setupReveals();
  setupSidebar();
  setupProgress();
})();
