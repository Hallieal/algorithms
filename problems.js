(() => {
  "use strict";

  const progress = document.getElementById("reading-progress");
  if (progress) {
    const updateProgress = () => {
      const doc = document.documentElement;
      const max = doc.scrollHeight - window.innerHeight;
      const value = max > 0 ? Math.min(1, Math.max(0, window.scrollY / max)) : 0;
      progress.style.width = `${value * 100}%`;
    };
    updateProgress();
    window.addEventListener("scroll", updateProgress, { passive: true });
    window.addEventListener("resize", updateProgress);
  }

  const links = [...document.querySelectorAll(".sidebar a[href^='#']")];
  if (links.length) {
    const sections = links
      .map(link => document.querySelector(link.getAttribute("href")))
      .filter(Boolean);

    const updateActive = () => {
      let current = sections[0];
      for (const section of sections) {
        if (section.getBoundingClientRect().top <= 135) current = section;
      }
      links.forEach(link => {
        link.classList.toggle("active", current && link.getAttribute("href") === `#${current.id}`);
      });
    };
    updateActive();
    window.addEventListener("scroll", updateActive, { passive: true });
  }

  document.querySelectorAll(".copy-code").forEach(button => {
    button.addEventListener("click", async () => {
      const block = button.closest(".problem-code")?.querySelector("code");
      if (!block) return;
      const original = button.textContent;
      try {
        await navigator.clipboard.writeText(block.textContent);
        button.textContent = "Copied";
      } catch (_) {
        button.textContent = "Select code";
      }
      window.setTimeout(() => { button.textContent = original; }, 1300);
    });
  });
})();
