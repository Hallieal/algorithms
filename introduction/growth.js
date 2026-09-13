(() => {
  "use strict";

  const explorers = document.querySelectorAll("[data-growth-explorer]");
  if (!explorers.length) return;

  const SVG_NS = "http://www.w3.org/2000/svg";
  const COLORS = {
    constant: "#8e9498",
    log: "#4fa99d",
    linear: "#739b2e",
    nlogn: "#d0a34b",
    square: "#d58e43",
    cube: "#b76b73",
    exp: "#8573b7"
  };

  function svg(tag, attrs = {}) {
    const el = document.createElementNS(SVG_NS, tag);
    for (const [key, value] of Object.entries(attrs)) el.setAttribute(key, value);
    return el;
  }

  function formatInteger(n, locale) {
    return new Intl.NumberFormat(locale).format(n);
  }

  function formatFromLog10(logValue, locale) {
    if (!Number.isFinite(logValue)) return "0";
    if (logValue < 6) {
      const value = Math.pow(10, logValue);
      if (value < 1000) return new Intl.NumberFormat(locale, { maximumFractionDigits: 2 }).format(value);
      return new Intl.NumberFormat(locale, { maximumFractionDigits: 0 }).format(value);
    }
    const exponent = Math.floor(logValue);
    const coefficient = Math.pow(10, logValue - exponent);
    return `${coefficient.toFixed(coefficient >= 9.95 ? 0 : 2)} × 10^${formatInteger(exponent, locale)}`;
  }

  function formatCount(kind, n, locale) {
    if (kind === "constant") return "1";
    if (kind === "log") {
      if (n <= 1) return "0";
      return new Intl.NumberFormat(locale, { maximumFractionDigits: 2 }).format(Math.log2(n));
    }
    if (kind === "linear") return formatFromLog10(Math.log10(Math.max(1, n)), locale);
    if (kind === "nlogn") {
      if (n <= 1) return "0";
      return formatFromLog10(Math.log10(n) + Math.log10(Math.log2(n)), locale);
    }
    if (kind === "square") return formatFromLog10(2 * Math.log10(Math.max(1, n)), locale);
    if (kind === "cube") return formatFromLog10(3 * Math.log10(Math.max(1, n)), locale);
    if (kind === "exp") return formatFromLog10(n * Math.log10(2), locale);
    return "";
  }

  function logOps(kind, n) {
    if (kind === "constant") return 0;
    if (kind === "log") return Math.log10(Math.max(1, Math.log2(Math.max(2, n))));
    if (kind === "linear") return Math.log10(Math.max(1, n));
    if (kind === "nlogn") return Math.log10(Math.max(1, n)) + Math.log10(Math.max(1, Math.log2(Math.max(2, n))));
    if (kind === "square") return 2 * Math.log10(Math.max(1, n));
    if (kind === "cube") return 3 * Math.log10(Math.max(1, n));
    if (kind === "exp") return n * Math.log10(2);
    return 0;
  }

  function niceTick(value) {
    if (value === 0) return "1";
    if (value === 1) return "10";
    if (value === 2) return "100";
    if (value === 3) return "1K";
    if (value === 6) return "1M";
    if (value === 9) return "1B";
    return `10^${Math.round(value)}`;
  }

  explorers.forEach(root => {
    const locale = root.dataset.locale === "ru" ? "ru-RU" : "en-US";
    const isRu = locale === "ru-RU";
    const slider = root.querySelector("[data-growth-slider]");
    const current = root.querySelector("[data-growth-current]");
    const chart = root.querySelector("[data-growth-chart]");
    const values = root.querySelector("[data-growth-values]");
    const legend = root.querySelector("[data-growth-legend]");
    if (!slider || !current || !chart || !values || !legend) return;

    const series = [
      ["constant", "O(1)"],
      ["log", "O(log n)"],
      ["linear", "O(n)"],
      ["nlogn", "O(n log n)"],
      ["square", "O(n²)"],
      ["cube", "O(n³)"],
      ["exp", "O(2ⁿ)"]
    ];

    legend.innerHTML = series.map(([kind, label]) =>
      `<span><i style="--legend:${COLORS[kind]}"></i>${label}</span>`
    ).join("");

    values.innerHTML = series.map(([kind, label]) =>
      `<div class="growth-value-card" data-growth-value="${kind}"><span>${label}</span><strong>—</strong></div>`
    ).join("");

    function draw() {
      const exponent = Number(slider.value);
      const n = Math.max(1, Math.round(Math.pow(10, exponent)));
      slider.setAttribute("aria-valuetext", `n = ${formatInteger(n, locale)}`);
      current.textContent = `n = ${formatInteger(n, locale)}`;

      root.querySelectorAll("[data-growth-value]").forEach(card => {
        const kind = card.dataset.growthValue;
        card.querySelector("strong").textContent = formatCount(kind, n, locale);
      });

      const W = 760, H = 360;
      const M = { l: 58, r: 20, t: 22, b: 46 };
      const plotW = W - M.l - M.r;
      const plotH = H - M.t - M.b;
      const xMax = Math.max(1, Math.log10(Math.max(10, n)));
      const yMax = Math.max(3, 3 * Math.log10(Math.max(10, n)) + 0.25);
      const x = logN => M.l + (logN / xMax) * plotW;
      const y = logY => M.t + plotH - (Math.max(0, Math.min(yMax, logY)) / yMax) * plotH;

      chart.innerHTML = "";
      chart.setAttribute("viewBox", `0 0 ${W} ${H}`);

      const grid = svg("g", { class: "growth-grid" });
      chart.appendChild(grid);

      const xTicks = [];
      const maxDecade = Math.floor(xMax);
      const stepX = maxDecade > 6 ? 3 : maxDecade > 3 ? 2 : 1;
      for (let k = 0; k <= maxDecade; k += stepX) xTicks.push(k);
      if (!xTicks.includes(maxDecade)) xTicks.push(maxDecade);
      xTicks.forEach(k => {
        const xx = x(k);
        grid.appendChild(svg("line", { x1: xx, y1: M.t, x2: xx, y2: M.t + plotH, class: "grid-line" }));
        const label = svg("text", { x: xx, y: H - 14, class: "axis-label", "text-anchor": "middle" });
        label.textContent = niceTick(k);
        grid.appendChild(label);
      });

      const yStep = yMax <= 6 ? 1 : yMax <= 15 ? 3 : 5;
      for (let k = 0; k <= yMax + 1e-9; k += yStep) {
        const yy = y(k);
        grid.appendChild(svg("line", { x1: M.l, y1: yy, x2: M.l + plotW, y2: yy, class: "grid-line" }));
        const label = svg("text", { x: M.l - 10, y: yy + 4, class: "axis-label", "text-anchor": "end" });
        label.textContent = k === 0 ? "1" : `10^${k}`;
        grid.appendChild(label);
      }

      const axisX = svg("text", { x: M.l + plotW / 2, y: H - 1, class: "axis-title", "text-anchor": "middle" });
      axisX.textContent = isRu ? "размер входа n (логарифмическая шкала)" : "input size n (logarithmic scale)";
      chart.appendChild(axisX);

      const axisY = svg("text", { x: 15, y: M.t + plotH / 2, class: "axis-title", transform: `rotate(-90 15 ${M.t + plotH / 2})`, "text-anchor": "middle" });
      axisY.textContent = isRu ? "число операций (логарифмическая шкала)" : "operation count (logarithmic scale)";
      chart.appendChild(axisY);

      const curves = svg("g", { class: "growth-curves" });
      chart.appendChild(curves);

      let expExit = null;
      for (const [kind] of series) {
        const pts = [];
        const samples = 180;
        for (let i = 0; i <= samples; i++) {
          const logN = (i / samples) * xMax;
          const sampleN = Math.max(1, Math.pow(10, logN));
          const logY = logOps(kind, sampleN);
          if (kind === "exp" && logY > yMax) {
            if (!expExit && pts.length) expExit = pts[pts.length - 1];
            break;
          }
          pts.push([x(logN), y(logY)]);
        }
        if (pts.length < 2) continue;
        const d = pts.map((p, i) => `${i ? "L" : "M"}${p[0].toFixed(2)},${p[1].toFixed(2)}`).join(" ");
        curves.appendChild(svg("path", { d, fill: "none", stroke: COLORS[kind], "stroke-width": kind === "exp" ? 3.2 : 2.7, "stroke-linecap": "round", "stroke-linejoin": "round", class: `growth-curve curve-${kind}` }));
      }

      if (expExit) {
        const [xx] = expExit;
        const arrow = svg("path", { d: `M${xx},${M.t + 13} L${xx},${M.t + 1} M${xx - 5},${M.t + 7} L${xx},${M.t + 1} L${xx + 5},${M.t + 7}`, stroke: COLORS.exp, "stroke-width": 2.4, fill: "none", "stroke-linecap": "round", "stroke-linejoin": "round" });
        chart.appendChild(arrow);
        const label = svg("text", { x: Math.min(xx + 7, W - 125), y: M.t + 13, class: "exp-exit-label" });
        label.textContent = isRu ? "2ⁿ вышло за масштаб" : "2ⁿ leaves the scale";
        chart.appendChild(label);
      }
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
