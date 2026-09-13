from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import unquote
import re

ROOT = Path('.')


def read(path):
    return (ROOT / path).read_text(encoding='utf-8')


def write(path, text):
    (ROOT / path).write_text(text, encoding='utf-8', newline='\n')


# -----------------------------------------------------------------------------
# 1. Shared stepper: add previous-step support and button state synchronization.
# -----------------------------------------------------------------------------
core_path = Path('assets/js/lecture-core.js')
core = core_path.read_text(encoding='utf-8')
if 'previousAction' not in core:
    core = core.replace(
        '      nextAction = "next",\n      resetAction = "reset",\n      randomizeAction = "randomize"',
        '      nextAction = "next",\n      previousAction = nextAction.replace(/^next/, "previous"),\n      resetAction = "reset",\n      randomizeAction = "randomize"'
    )
    core = core.replace(
        '    const reset = data => {\n      root[store] = build(data);\n      root._index = 0;\n      render(root);\n    };',
        '''    const syncButtons = () => {
      const previous = root.querySelector(`[data-action="${previousAction}"]`);
      const next = root.querySelector(`[data-action="${nextAction}"]`);
      const last = Math.max(0, root[store].length - 1);
      if (previous) previous.disabled = root._index <= 0;
      if (next) next.disabled = root._index >= last;
    };

    const draw = () => {
      render(root);
      syncButtons();
    };

    const reset = data => {
      root[store] = build(data);
      root._index = 0;
      draw();
    };'''
    )
    core = core.replace(
        '''      if (action === nextAction) {
        root._index = Math.min(root._index + 1, root[store].length - 1);
        render(root);
      } else if (action === resetAction) {''',
        '''      if (action === nextAction) {
        root._index = Math.min(root._index + 1, root[store].length - 1);
        draw();
      } else if (action === previousAction) {
        root._index = Math.max(root._index - 1, 0);
        draw();
      } else if (action === resetAction) {'''
    )
core_path.write_text(core, encoding='utf-8', newline='\n')


# -----------------------------------------------------------------------------
# 2. Insert Previous buttons into every step-by-step visualizer in Sorting.
# -----------------------------------------------------------------------------
button_re = re.compile(r'(<button\b[^>]*data-action="(next[^"]*)"[^>]*>.*?</button>)', re.S)
stepper_pages = []
stepper_count = 0
for path in sorted(Path('sorting').glob('*.html')):
    text = path.read_text(encoding='utf-8')
    lang_ru = '<html lang="ru"' in text or '<html lang="ru-RU"' in text
    changed = False

    def repl(match):
        nonlocal_marker[0] += 1
        button_html, action = match.group(1), match.group(2)
        previous_action = re.sub(r'^next', 'previous', action)
        if f'data-action="{previous_action}"' in text:
            return button_html
        label = '← Предыдущий шаг сортировки' if lang_ru else '← Previous sorting step'
        previous = f'<button class="previous-step" data-action="{previous_action}" type="button" disabled>{label}</button>'
        return f'<div class="step-nav-controls">{previous}{button_html}</div>'

    nonlocal_marker = [0]
    new_text = button_re.sub(repl, text)
    if new_text != text:
        changed = True
        stepper_count += nonlocal_marker[0]
        path.write_text(new_text, encoding='utf-8', newline='\n')
        stepper_pages.append(str(path))


# -----------------------------------------------------------------------------
# 3. Problem-to-problem navigation.
# -----------------------------------------------------------------------------
problem_dir = Path('sorting/problems')
english = [
    ('wave-form.html', 'Sort in Wave Form'),
    ('two-sum-sorted.html', 'Two Sum in a Sorted Array'),
    ('meeting-rooms.html', 'Meeting Rooms'),
    ('three-way-partitioning.html', 'Three-Way Partitioning'),
    ('k-smallest.html', 'K Smallest Elements'),
    ('inversion-count.html', 'Inversion Count'),
    ('top-k-frequent.html', 'Top K Frequent Elements'),
    ('merge-without-space.html', 'Merge Without Extra Space'),
    ('closest-pair.html', 'Closest Pair of Points'),
]
russian = [
    ('three-way-partitioning-ru.html', 'Трёхчастное разбиение'),
    ('k-smallest-ru.html', 'K наименьших элементов'),
    ('inversion-count-ru.html', 'Число инверсий'),
    ('top-k-frequent-ru.html', 'K самых частых элементов'),
    ('merge-without-space-ru.html', 'Слияние без дополнительной памяти'),
    ('closest-pair-ru.html', 'Ближайшая пара точек'),
]

for filename, _ in english + russian:
    if not (problem_dir / filename).exists():
        raise RuntimeError(f'Missing problem page: {filename}')

back_card_re = re.compile(r'\s*<div class="next-part back-problems">.*?</div>\s*', re.S)
old_pager_re = re.compile(r'\s*<nav class="problem-sequence-nav".*?</nav>\s*', re.S)


def nav_card(direction, href, title, ru=False):
    if not href:
        return '<div class="problem-sequence-empty" aria-hidden="true"></div>'
    if ru:
        eyebrow = '← Предыдущая задача' if direction == 'prev' else 'Следующая задача →'
    else:
        eyebrow = '← Previous problem' if direction == 'prev' else 'Next problem →'
    cls = 'previous' if direction == 'prev' else 'next'
    return f'<a class="problem-sequence-link {cls}" href="{href}"><span>{eyebrow}</span><strong>{title}</strong></a>'


def add_problem_navigation(sequence, ru=False):
    for i, (filename, title) in enumerate(sequence):
        path = problem_dir / filename
        text = path.read_text(encoding='utf-8')
        text = back_card_re.sub('\n', text)
        text = old_pager_re.sub('\n', text)

        prev_item = sequence[i - 1] if i > 0 else None
        next_item = sequence[i + 1] if i + 1 < len(sequence) else None
        prev_html = nav_card('prev', prev_item[0], prev_item[1], ru) if prev_item else nav_card('prev', None, '', ru)
        next_html = nav_card('next', next_item[0], next_item[1], ru) if next_item else nav_card('next', None, '', ru)
        center_text = 'Все задачи' if ru else 'All practice problems'
        aria = 'Навигация по задачам' if ru else 'Problem navigation'
        pager = f'''\n<nav class="problem-sequence-nav" aria-label="{aria}">
  {prev_html}
  <a class="problem-sequence-index" href="./">{center_text}</a>
  {next_html}
</nav>\n'''

        marker = text.rfind('</section>\n  </main>')
        if marker == -1:
            marker = text.rfind('</section>\n</main>')
        if marker == -1:
            raise RuntimeError(f'Could not find final section in {filename}')
        text = text[:marker] + pager + text[marker:]
        path.write_text(text, encoding='utf-8', newline='\n')


add_problem_navigation(english, ru=False)
add_problem_navigation(russian, ru=True)


# -----------------------------------------------------------------------------
# 4. CSS: mobile header, previous-step controls, and problem pager.
# -----------------------------------------------------------------------------
styles_path = Path('assets/css/styles.css')
styles = styles_path.read_text(encoding='utf-8')
marker = '/* ---------- Navigation and mobile-header refinements ---------- */'
if marker not in styles:
    styles += r'''

/* ---------- Navigation and mobile-header refinements ---------- */
.step-nav-controls {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 9px;
  flex-wrap: wrap;
}

.previous-step {
  min-height: 39px;
  padding: 9px 13px;
  border: 1px solid #d8d5ce;
  border-radius: 10px;
  background: #fff;
  color: #56616a;
  font: inherit;
  font-size: 12px;
  font-weight: 760;
  cursor: pointer;
}

.previous-step:hover:not(:disabled) {
  border-color: #c7d5ae;
  background: #f6f9f0;
  color: var(--ink);
}

.previous-step:disabled,
.primary-step:disabled {
  opacity: .38;
  cursor: default;
  transform: none !important;
}

@media (max-width: 720px) {
  .topbar {
    height: auto;
    min-height: 62px;
    padding: 10px 14px;
    gap: 10px;
  }

  .brand {
    flex: 0 0 auto;
    min-width: 0;
  }

  .brand-name {
    display: none;
  }

  .brand-mark {
    width: 34px;
    height: 34px;
    flex: 0 0 34px;
  }

  .topnav {
    margin-left: auto;
    min-width: 0;
    gap: 10px;
    flex-wrap: nowrap;
  }

  .topnav > a,
  .language-switch {
    white-space: nowrap;
    font-size: 12px;
  }

  .visualizer-head {
    gap: 14px;
  }

  .step-nav-controls {
    justify-content: flex-start;
  }
}

@media (max-width: 420px) {
  .topbar { padding-left: 11px; padding-right: 11px; }
  .topnav { gap: 8px; }
  .topnav > a,
  .language-switch { font-size: 11px; }
  .step-nav-controls { gap: 7px; }
  .previous-step,
  .primary-step { padding-left: 10px; padding-right: 10px; }
}
'''
styles_path.write_text(styles, encoding='utf-8', newline='\n')

problems_css_path = problem_dir / 'assets/problems.css'
problems_css = problems_css_path.read_text(encoding='utf-8')
problem_marker = '/* ---------- Sequential problem navigation ---------- */'
if problem_marker not in problems_css:
    problems_css += r'''

/* ---------- Sequential problem navigation ---------- */
.problem-sequence-nav {
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto minmax(0, 1fr);
  gap: 12px;
  align-items: stretch;
  margin-top: 42px;
  padding-top: 28px;
  border-top: 1px solid var(--line);
}

.problem-sequence-link {
  min-width: 0;
  padding: 16px 18px;
  border: 1px solid var(--line);
  border-radius: 14px;
  background: #fff;
  text-decoration: none;
  transition: transform .16s ease, border-color .16s ease, box-shadow .16s ease;
}

.problem-sequence-link:hover {
  transform: translateY(-1px);
  border-color: #cfd9bf;
  box-shadow: 0 8px 22px rgba(35, 42, 48, .055);
}

.problem-sequence-link.next { text-align: right; }
.problem-sequence-link span {
  display: block;
  margin-bottom: 4px;
  color: #7c858c;
  font-size: 10px;
  font-weight: 820;
  letter-spacing: .06em;
  text-transform: uppercase;
}
.problem-sequence-link strong {
  display: block;
  color: var(--ink);
  font-size: 14px;
  line-height: 1.35;
}

.problem-sequence-index {
  align-self: center;
  padding: 9px 12px;
  color: #61704e;
  font-size: 12px;
  font-weight: 780;
  text-decoration: none;
  white-space: nowrap;
}
.problem-sequence-index:hover { text-decoration: underline; }
.problem-sequence-empty { min-width: 0; }

@media (max-width: 700px) {
  .problem-sequence-nav {
    grid-template-columns: 1fr 1fr;
  }
  .problem-sequence-index {
    grid-column: 1 / -1;
    grid-row: 2;
    justify-self: center;
  }
  .problem-sequence-empty { display: none; }
  .problem-sequence-link.next { text-align: left; }
}

@media (max-width: 480px) {
  .problem-sequence-nav { grid-template-columns: 1fr; }
  .problem-sequence-index { grid-column: 1; grid-row: auto; justify-self: start; }
  .problem-sequence-link.next { text-align: left; }
}
'''
problems_css_path.write_text(problems_css, encoding='utf-8', newline='\n')


# -----------------------------------------------------------------------------
# 5. Audit the intended theory sequence (EN/RU).
# -----------------------------------------------------------------------------
theory = {
    'sorting/introduction.html': ['applications.html'],
    'sorting/applications.html': ['introduction.html', 'selection-insertion.html'],
    'sorting/selection-insertion.html': ['applications.html', 'bubble.html'],
    'sorting/bubble.html': ['selection-insertion.html', 'merge.html'],
    'sorting/merge.html': ['bubble.html', 'quick.html'],
    'sorting/quick.html': ['merge.html', 'problems/'],
    'sorting/introduction-ru.html': ['applications-ru.html'],
    'sorting/applications-ru.html': ['introduction-ru.html', 'selection-insertion-ru.html'],
    'sorting/selection-insertion-ru.html': ['applications-ru.html', 'bubble-ru.html'],
    'sorting/bubble-ru.html': ['selection-insertion-ru.html', 'merge-ru.html'],
    'sorting/merge-ru.html': ['bubble-ru.html', 'quick-ru.html'],
    'sorting/quick-ru.html': ['merge-ru.html', 'problems/index-ru.html'],
}
for filename, targets in theory.items():
    text = read(filename)
    for target in targets:
        if f'href="{target}"' not in text and f"href='{target}'" not in text:
            raise RuntimeError(f'Missing theory navigation: {filename} -> {target}')


# -----------------------------------------------------------------------------
# 6. Full local href/src audit across every HTML file.
# -----------------------------------------------------------------------------
class RefParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.refs = []
    def handle_starttag(self, tag, attrs):
        for key, value in attrs:
            if key in ('href', 'src') and value:
                self.refs.append((key, value))


def resolve_local(html_path, value):
    value = value.strip()
    if not value or value.startswith(('#', 'http://', 'https://', 'mailto:', 'tel:', 'javascript:', 'data:')):
        return None
    clean = unquote(value.split('#', 1)[0].split('?', 1)[0])
    if not clean:
        return None
    if clean.startswith('/'):
        if clean.startswith('/algorithms/'):
            clean = clean[len('/algorithms/'):]
            target = ROOT / clean
        elif clean == '/algorithms/' or clean == '/':
            target = ROOT
        else:
            return None
    else:
        target = (html_path.parent / clean)
    return target

broken = []
refs_checked = 0
for html in sorted(ROOT.rglob('*.html')):
    parser = RefParser()
    parser.feed(html.read_text(encoding='utf-8'))
    for kind, value in parser.refs:
        target = resolve_local(html, value)
        if target is None:
            continue
        refs_checked += 1
        if target.is_dir():
            exists = (target / 'index.html').exists()
        else:
            exists = target.exists()
        if not exists:
            broken.append((str(html), kind, value, str(target)))

if broken:
    details = '\n'.join(f'{a}: {k}={v} -> {t}' for a, k, v, t in broken[:40])
    raise RuntimeError(f'Broken local references ({len(broken)}):\n{details}')

# Verify pagers and Previous buttons specifically.
for filename, _ in english:
    text = (problem_dir / filename).read_text(encoding='utf-8')
    assert 'problem-sequence-nav' in text, filename
for filename, _ in russian:
    text = (problem_dir / filename).read_text(encoding='utf-8')
    assert 'problem-sequence-nav' in text, filename

for path in stepper_pages:
    text = Path(path).read_text(encoding='utf-8')
    assert 'data-action="previous' in text, path

print(f'Navigation audit complete: {refs_checked} local href/src references checked; 0 broken.')
print(f'Problem pagers: {len(english)} EN + {len(russian)} RU pages.')
print(f'Previous-step controls inserted: {stepper_count} across {len(stepper_pages)} theory pages.')
