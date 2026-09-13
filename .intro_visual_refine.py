from pathlib import Path
import re

ROOT = Path('.')


def read(path):
    return (ROOT / path).read_text(encoding='utf-8')


def write(path, text):
    (ROOT / path).write_text(text, encoding='utf-8', newline='\n')


# Homepage icon: use the same image-based course-icon structure as every other topic.
for path, alt in [('index.html', 'Introduction to Algorithms icon'), ('index-ru.html', 'Иконка введения в алгоритмы')]:
    text = read(path)
    text, n = re.subn(
        r'<div class="course-icon intro-course-icon"[^>]*>.*?</div>',
        f'<div class="course-icon"><img alt="{alt}" src="assets/images/topic-introduction.svg"/></div>',
        text,
        count=1,
        flags=re.S,
    )
    if n != 1 and 'topic-introduction.svg' not in text:
        raise RuntimeError(f'Could not replace introduction icon in {path}')
    write(path, text)


def growth_explorer(locale):
    ru = locale == 'ru'
    if ru:
        return '''<div class="growth-explorer" data-growth-explorer data-locale="ru">
        <div class="growth-explorer-head">
          <div><span class="growth-explorer-kicker">Интерактив</span><h3>Как расходятся классы сложности</h3><p>Двигайте ползунок от 1 до 10⁹. Обе оси графика логарифмические, поэтому медленные и быстрые полиномиальные классы остаются одновременно видимыми.</p></div>
          <strong class="growth-current" data-growth-current>n = 1 000</strong>
        </div>
        <div class="growth-slider-block">
          <input class="growth-slider" data-growth-slider type="range" min="0" max="9" step="0.001" value="3" aria-label="Размер входа n от 1 до одного миллиарда">
          <div class="growth-slider-labels"><span>1</span><span>10</span><span>1K</span><span>1M</span><span>1B</span></div>
          <div class="growth-presets"><button type="button" data-growth-preset="1">10</button><button type="button" data-growth-preset="3">1K</button><button type="button" data-growth-preset="6">1M</button><button type="button" data-growth-preset="9">1B</button></div>
        </div>
        <div class="growth-legend" data-growth-legend></div>
        <div class="growth-chart-shell"><svg class="growth-chart" data-growth-chart role="img" aria-label="График роста типичных классов сложности"></svg></div>
        <p class="growth-scale-note">Шкала по вертикали показывает порядок числа операций. Экспонента <code>2ⁿ</code> намеренно обрезается, когда выходит выше диапазона <code>n³</code>: иначе она мгновенно сжала бы все полиномиальные кривые почти в одну линию.</p>
        <div class="growth-values" data-growth-values></div>
      </div>'''
    return '''<div class="growth-explorer" data-growth-explorer data-locale="en">
        <div class="growth-explorer-head">
          <div><span class="growth-explorer-kicker">Interactive</span><h3>Watch the growth classes separate</h3><p>Move the slider from 1 to 10⁹. Both axes are logarithmic, so slow and fast polynomial classes remain visible at the same time.</p></div>
          <strong class="growth-current" data-growth-current>n = 1,000</strong>
        </div>
        <div class="growth-slider-block">
          <input class="growth-slider" data-growth-slider type="range" min="0" max="9" step="0.001" value="3" aria-label="Input size n from 1 to one billion">
          <div class="growth-slider-labels"><span>1</span><span>10</span><span>1K</span><span>1M</span><span>1B</span></div>
          <div class="growth-presets"><button type="button" data-growth-preset="1">10</button><button type="button" data-growth-preset="3">1K</button><button type="button" data-growth-preset="6">1M</button><button type="button" data-growth-preset="9">1B</button></div>
        </div>
        <div class="growth-legend" data-growth-legend></div>
        <div class="growth-chart-shell"><svg class="growth-chart" data-growth-chart role="img" aria-label="Growth chart for common complexity classes"></svg></div>
        <p class="growth-scale-note">The vertical scale represents orders of operation counts. The exponential curve <code>2ⁿ</code> is deliberately clipped once it rises above the <code>n³</code> range; otherwise it would immediately compress every polynomial curve into an unreadable strip.</p>
        <div class="growth-values" data-growth-values></div>
      </div>'''


for path, locale in [('introduction/index.html', 'en'), ('introduction/index-ru.html', 'ru')]:
    text = read(path)

    # The top cards should be just Time / Space / Growth, with no T(n), S(n), or Θ badges.
    text = re.sub(r'<div class="foundation-card-mark">.*?</div>', '', text, flags=re.S)

    # Replace the static schematic bars with the interactive explorer.
    pattern = re.compile(r'<div class="growth-board">.*?(?=<div class="asymptotic-note">)', re.S)
    text, n = pattern.subn(growth_explorer(locale) + '\n      ', text, count=1)
    if n != 1 and 'data-growth-explorer' not in text:
        raise RuntimeError(f'Could not replace growth board in {path}')

    if 'growth.js' not in text:
        text = text.replace('</body>', '  <script src="growth.js"></script>\n</body>', 1)

    write(path, text)


css = read('introduction/styles.css')
marker = '/* Interactive growth explorer */'
if marker not in css:
    css += r'''

/* Interactive growth explorer */
.foundation-card {
  min-height: 145px;
  padding-top: 24px;
}

.foundation-card h3 {
  margin-top: 0;
  font-size: 20px;
}

.growth-explorer {
  margin: 30px 0;
  padding: 24px;
  border: 1px solid #dfe5d2;
  border-radius: 20px;
  background:
    radial-gradient(circle at 92% 8%, rgba(133, 115, 212, .07), transparent 31%),
    #f7f9f2;
}

.growth-explorer-head {
  display: flex;
  justify-content: space-between;
  gap: 24px;
  align-items: flex-start;
}

.growth-explorer-kicker {
  display: block;
  margin-bottom: 5px;
  color: var(--green);
  font-size: 10px;
  font-weight: 850;
  letter-spacing: .09em;
  text-transform: uppercase;
}

.growth-explorer-head h3 {
  margin: 0 0 6px;
  font-size: 21px;
  letter-spacing: -.025em;
}

.growth-explorer-head p {
  max-width: 690px;
  margin: 0;
  color: #626c74;
  font-size: 13.5px;
}

.growth-current {
  flex: 0 0 auto;
  padding: 9px 12px;
  border: 1px solid #d8e2c8;
  border-radius: 11px;
  background: #fff;
  color: #4f6e2b;
  font-family: "SFMono-Regular", Consolas, monospace;
  font-size: 13px;
  font-variant-numeric: tabular-nums;
}

.growth-slider-block {
  margin: 24px 0 16px;
}

.growth-slider {
  width: 100%;
  accent-color: var(--green);
  cursor: pointer;
}

.growth-slider-labels {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  margin-top: 3px;
  color: #8a9196;
  font: 10px/1.2 "SFMono-Regular", Consolas, monospace;
}

.growth-slider-labels span:nth-child(2),
.growth-slider-labels span:nth-child(3),
.growth-slider-labels span:nth-child(4) { text-align: center; }
.growth-slider-labels span:last-child { text-align: right; }

.growth-presets {
  display: flex;
  gap: 7px;
  margin-top: 12px;
}

.growth-presets button {
  padding: 6px 10px;
  border: 1px solid #dde1d8;
  border-radius: 9px;
  background: rgba(255,255,255,.78);
  color: #626c73;
  font: 750 11px/1 inherit;
  cursor: pointer;
}

.growth-presets button:hover {
  border-color: #cbd9b8;
  background: #fff;
  color: #4f6d2c;
}

.growth-legend {
  display: flex;
  flex-wrap: wrap;
  gap: 8px 14px;
  margin: 16px 0 10px;
}

.growth-legend span {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  color: #5e6870;
  font: 750 11px/1.2 "SFMono-Regular", Consolas, monospace;
}

.growth-legend i {
  width: 16px;
  height: 4px;
  border-radius: 999px;
  background: var(--legend);
}

.growth-chart-shell {
  overflow: hidden;
  border: 1px solid #e2e5dd;
  border-radius: 16px;
  background: rgba(255,255,255,.88);
}

.growth-chart {
  display: block;
  width: 100%;
  height: auto;
  min-height: 300px;
}

.growth-chart .grid-line {
  stroke: #e8e8e2;
  stroke-width: 1;
}

.growth-chart .axis-label,
.growth-chart .axis-title,
.growth-chart .exp-exit-label {
  fill: #7b8389;
  font-family: Inter, ui-sans-serif, system-ui, sans-serif;
  font-size: 10px;
}

.growth-chart .axis-title {
  fill: #69737a;
  font-size: 10.5px;
  font-weight: 720;
}

.growth-chart .exp-exit-label {
  fill: #7464aa;
  font-weight: 800;
}

.growth-curve {
  vector-effect: non-scaling-stroke;
}

.growth-scale-note {
  margin: 11px 2px 0;
  color: #778087;
  font-size: 11.5px;
  line-height: 1.55;
}

.growth-values {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 8px;
  margin-top: 18px;
}

.growth-value-card {
  min-width: 0;
  padding: 11px 12px;
  border: 1px solid #e4e4de;
  border-radius: 11px;
  background: rgba(255,255,255,.82);
}

.growth-value-card span {
  display: block;
  color: #7c848a;
  font: 750 10px/1.2 "SFMono-Regular", Consolas, monospace;
}

.growth-value-card strong {
  display: block;
  overflow: hidden;
  margin-top: 5px;
  color: #303a42;
  font: 800 12px/1.3 "SFMono-Regular", Consolas, monospace;
  text-overflow: ellipsis;
  white-space: nowrap;
}

@media (max-width: 760px) {
  .growth-explorer { padding: 18px; }
  .growth-explorer-head { display: block; }
  .growth-current { display: inline-block; margin-top: 12px; }
  .growth-values { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .growth-chart { min-height: 245px; }
}

@media (max-width: 440px) {
  .growth-values { grid-template-columns: 1fr; }
  .growth-presets { flex-wrap: wrap; }
}
'''
write('introduction/styles.css', css)

# Validation.
for path in ('index.html', 'index-ru.html'):
    text = read(path)
    assert 'topic-introduction.svg' in text
    assert 'intro-course-icon' not in text

for path in ('introduction/index.html', 'introduction/index-ru.html'):
    text = read(path)
    assert 'foundation-card-mark' not in text
    assert 'data-growth-explorer' in text
    assert 'growth.js' in text
    assert 'growth-board' not in text

print('Introduction visuals refined successfully.')
