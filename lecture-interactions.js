(() => {
  document.addEventListener("click", (event) => {
    const button = event.target.closest("button[data-reveal]");
    if (!button) return;

    const target = document.getElementById(button.dataset.reveal);
    if (!target) return;

    target.hidden = !target.hidden;
    button.setAttribute("aria-expanded", String(!target.hidden));

    const isRussian = document.documentElement.lang.toLowerCase().startsWith("ru");
    button.textContent = target.hidden
      ? (isRussian ? "Показать ответ" : "Show answer")
      : (isRussian ? "Скрыть ответ" : "Hide answer");
  });

  const sidebarLinks = [...document.querySelectorAll(".sidebar a")];
  const sections = sidebarLinks
    .map((link) => document.querySelector(link.getAttribute("href")))
    .filter(Boolean);

  if ("IntersectionObserver" in window && sections.length) {
    const observer = new IntersectionObserver((entries) => {
      const visible = entries
        .filter((entry) => entry.isIntersecting)
        .sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0];

      if (!visible) return;

      sidebarLinks.forEach((link) => link.classList.remove("active"));
      const current = sidebarLinks.find(
        (link) => link.getAttribute("href") === `#${visible.target.id}`
      );
      if (current) current.classList.add("active");
    }, {
      rootMargin: "-20% 0px -65% 0px",
      threshold: [0, 0.1, 0.3, 0.6]
    });

    sections.forEach((section) => observer.observe(section));
  }

  const progress = document.getElementById("reading-progress");
  if (progress) {
    const updateProgress = () => {
      const height = document.documentElement.scrollHeight - window.innerHeight;
      const ratio = height > 0 ? window.scrollY / height : 0;
      progress.style.width = `${Math.max(0, Math.min(1, ratio)) * 100}%`;
    };

    updateProgress();
    window.addEventListener("scroll", updateProgress, { passive: true });
    window.addEventListener("resize", updateProgress);
  }
})();
