(() => {
  document.addEventListener("click", (event) => {
    const link = event.target.closest(".language-switch a");
    if (!link) return;
    const lang = link.textContent.trim().toLowerCase();
    if (lang === "en" || lang === "ru") localStorage.setItem("aha-language", lang);
  });
})();
