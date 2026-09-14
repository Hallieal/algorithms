(() => {
  "use strict";

  const simulators = document.querySelectorAll("[data-growth-simulator]");
  if (!simulators.length) return;

  function formatNumber(value, locale) {
    if (!Number.isFinite(value)) return "∞";
    if (value < 1_000_000_000_000) {
      return new Intl.NumberFormat(locale, { maximumFractionDigits: value < 100 ? 2 : 0 }).format(value);
    }
    const exponent = Math.floor(Math.log10(value));
    const coefficient = value / Math.pow(10, exponent);
    return `${coefficient.toFixed(2)} × 10^${exponent}`;
  }

  function powerOfTwoText(n, locale) {
    if (n <= 39) return new Intl.NumberFormat(locale).format(Math.pow(2, n));
    const exponent = n * Math.log10(2);
    const e = Math.floor(exponent);
    const coefficient = Math.pow(10, exponent - e);
    return `≈ ${coefficient.toFixed(2)} × 10^${e}`;
  }

  function valuesFor(n) {
    const log = n <= 1 ? 0 : Math.log2(n);
    return {
      constant: 1,
      log,
      linear: n,
      nlogn: n * log,
      square: n * n,
      cube: n * n * n
    };
  }

  simulators.forEach(root => {
    const locale = root.dataset.locale === "ru" ? "ru-RU" : "en-US";
    const slider = root.querySelector("[data-growth-slider]");
    const current = root.querySelector("[data-growth-current]");
    const expN = root.querySelector("[data-exp-n]");
    const expCount = root.querySelector("[data-exp-count]");
    if (!slider || !current || !expN || !expCount) return;

    function draw() {
      const n = Number(slider.value);
      const values = valuesFor(n);
      const scale = Math.max(1, values.cube);

      current.textContent = `n = ${n}`;
      slider.setAttribute("aria-valuetext", `n = ${n}`);

      root.querySelectorAll(".sim-row[data-kind]").forEach(row => {
        const kind = row.dataset.kind;
        const value = values[kind];
        const bar = row.querySelector(".sim-track span");
        const count = row.querySelector("[data-count]");
        const percent = Math.max(0.4, Math.min(100, (value / scale) * 100));
        if (bar) bar.style.setProperty("--bar", `${percent}%`);
        if (count) count.textContent = formatNumber(value, locale);
      });

      expN.textContent = `n = ${n}`;
      expCount.textContent = powerOfTwoText(n, locale);
    }

    slider.addEventListener("input", draw);
    root.querySelectorAll("[data-growth-preset]").forEach(button => {
      button.addEventListener("click", () => {
        slider.value = button.dataset.growthPreset;
        draw();
      });
    });

    draw();
  });
})();
