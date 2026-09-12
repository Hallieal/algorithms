const DEFAULTS = {
  selection: [7, 3, 8, 2, 6, 4, 9, 1],
  insertion: [7, 3, 8, 2, 6, 4, 9, 1]
};

function randomArray() {
  const pool = [1,2,3,4,5,6,7,8,9];
  for (let i = pool.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [pool[i], pool[j]] = [pool[j], pool[i]];
  }
  return pool.slice(0, 8);
}

function range(n, start = 0) {
  return Array.from({length:n}, (_, i) => i + start);
}

function selectionSteps(input) {
  const a = [...input];
  const steps = [{
    array:[...a],
    active:[],
    candidate:[],
    fixed:[],
    text:"Отсортированный префикс пока пуст."
  }];

  for (let i = 0; i < a.length - 1; i++) {
    let minPos = i;

    steps.push({
      array:[...a],
      active:[],
      candidate:[minPos],
      fixed:range(i),
      text:`Начинаем итерацию i = ${i}. Пока считаем минимумом элемент ${a[minPos]}.`
    });

    for (let j = i + 1; j < a.length; j++) {
      steps.push({
        array:[...a],
        active:[j],
        candidate:[minPos],
        fixed:range(i),
        text:`Сравниваем ${a[j]} с текущим минимумом ${a[minPos]}.`
      });

      if (a[j] < a[minPos]) {
        minPos = j;
        steps.push({
          array:[...a],
          active:[],
          candidate:[minPos],
          fixed:range(i),
          text:`Новый минимум неотсортированной части: ${a[minPos]}.`
        });
      }
    }

    if (minPos !== i) {
      const left = a[i], right = a[minPos];
      [a[i], a[minPos]] = [a[minPos], a[i]];
      steps.push({
        array:[...a],
        active:[i, minPos],
        candidate:[],
        fixed:range(i + 1),
        text:`Меняем местами ${left} и ${right}. Позиция ${i} теперь окончательна.`
      });
    } else {
      steps.push({
        array:[...a],
        active:[i],
        candidate:[],
        fixed:range(i + 1),
        text:`Минимум уже стоит на позиции ${i}. Префикс увеличивается без обмена.`
      });
    }
  }

  steps.push({
    array:[...a],
    active:[],
    candidate:[],
    fixed:range(a.length),
    text:"Готово: весь массив отсортирован."
  });
  return steps;
}

function insertionSteps(input) {
  const a = [...input];
  const steps = [{
    array:[...a],
    active:[],
    candidate:[],
    fixed:[0],
    text:"Первый элемент образует отсортированный префикс длины 1."
  }];

  for (let i = 1; i < a.length; i++) {
    const key = a[i];
    let j = i - 1;

    steps.push({
      array:[...a],
      active:[i],
      candidate:[],
      fixed:range(i),
      text:`Берём элемент ${key} и вставляем его в отсортированный префикс.`
    });

    while (j >= 0 && a[j] > key) {
      const shifted = a[j];
      a[j + 1] = a[j];
      steps.push({
        array:[...a],
        active:[j, j + 1],
        candidate:[],
        fixed:range(Math.max(j, 0)),
        text:`${shifted} > ${key}, поэтому ${shifted} сдвигается на одну позицию вправо.`
      });
      j--;
    }

    a[j + 1] = key;
    steps.push({
      array:[...a],
      active:[j + 1],
      candidate:[],
      fixed:range(i + 1),
      text:`Вставляем ${key} на позицию ${j + 1}. Префикс длины ${i + 1} отсортирован.`
    });
  }

  steps.push({
    array:[...a],
    active:[],
    candidate:[],
    fixed:range(a.length),
    text:"Готово: весь массив отсортирован."
  });
  return steps;
}

function buildSteps(type, array) {
  if (type === "selection") return selectionSteps(array);
  if (type === "insertion") return insertionSteps(array);
  return [];
}

function render(viz) {
  const bars = viz.querySelector(".bars");
  const caption = viz.querySelector(".step-caption");
  const step = viz._steps[viz._index];

  bars.innerHTML = "";

  step.array.forEach((value, idx) => {
    const el = document.createElement("div");
    el.className = "bar";
    el.style.setProperty("--value", value);
    el.textContent = value;
    el.setAttribute("aria-label", `Позиция ${idx}: ${value}`);

    if ((step.fixed || []).includes(idx)) el.classList.add("fixed");
    if ((step.candidate || []).includes(idx)) el.classList.add("candidate");
    if ((step.active || []).includes(idx)) el.classList.add("active");

    bars.appendChild(el);
  });

  caption.textContent = step.text;
}

function initVisualizer(viz) {
  const type = viz.dataset.algorithm;
  viz._array = [...DEFAULTS[type]];
  viz._steps = buildSteps(type, viz._array);
  viz._index = 0;
  render(viz);

  viz.querySelector('[data-action="next"]').addEventListener("click", () => {
    viz._index = Math.min(viz._index + 1, viz._steps.length - 1);
    render(viz);
  });

  viz.querySelector('[data-action="reset"]').addEventListener("click", () => {
    viz._array = [...DEFAULTS[type]];
    viz._steps = buildSteps(type, viz._array);
    viz._index = 0;
    render(viz);
  });

  viz.querySelector('[data-action="randomize"]').addEventListener("click", () => {
    viz._array = randomArray();
    viz._steps = buildSteps(type, viz._array);
    viz._index = 0;
    render(viz);
  });
}

function initRevealButtons() {
  document.querySelectorAll(".reveal").forEach(btn => {
    btn.addEventListener("click", () => {
      const box = document.getElementById(btn.dataset.target);
      if (!box) return;
      box.classList.toggle("show");
      btn.textContent = box.classList.contains("show") ? "Скрыть ответ" : "Показать ответ";
      btn.setAttribute("aria-expanded", box.classList.contains("show") ? "true" : "false");
    });
  });
}

function initSidebar() {
  const links = [...document.querySelectorAll(".sidebar a")];
  if (!links.length) return;

  const sections = links
    .map(a => document.querySelector(a.getAttribute("href")))
    .filter(Boolean);

  const observer = new IntersectionObserver(entries => {
    const visible = entries
      .filter(entry => entry.isIntersecting)
      .sort((a,b) => b.intersectionRatio - a.intersectionRatio)[0];

    if (!visible) return;

    links.forEach(a => a.classList.remove("active"));
    const active = links.find(a => a.getAttribute("href") === `#${visible.target.id}`);
    if (active) active.classList.add("active");
  }, {
    rootMargin:"-20% 0px -65% 0px",
    threshold:[0, .1, .3, .6]
  });

  sections.forEach(section => observer.observe(section));
}

function updateProgress() {
  const bar = document.getElementById("reading-progress");
  if (!bar) return;

  const doc = document.documentElement;
  const scrollable = doc.scrollHeight - window.innerHeight;
  const ratio = scrollable > 0 ? window.scrollY / scrollable : 0;
  bar.style.width = `${Math.max(0, Math.min(1, ratio)) * 100}%`;
}

document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".visualizer").forEach(initVisualizer);
  initRevealButtons();
  initSidebar();
  updateProgress();
});

window.addEventListener("scroll", updateProgress, {passive:true});
window.addEventListener("resize", updateProgress);
