from pathlib import Path
import re

ROOT = Path('.')


def read(path):
    return (ROOT / path).read_text(encoding='utf-8')


def write(path, text):
    (ROOT / path).write_text(text, encoding='utf-8', newline='\n')


# Home page cards.
index = read('index.html')
intro_card = '''<a class="course-card live" href="introduction/">
<div class="course-icon intro-course-icon" aria-hidden="true"><span>Θ</span><small>n → ∞</small></div>
<div>
<h3>Introduction to Algorithms</h3>
<p>Computation models, time and space complexity, asymptotic notation, and common growth rates.</p>
</div>
</a>
'''
if 'href="introduction/"' not in index:
    index = index.replace('<div class="course-grid">\n', '<div class="course-grid">\n' + intro_card, 1)
write('index.html', index)

index_ru = read('index-ru.html')
intro_card_ru = '''<a class="course-card live" href="introduction/index-ru.html">
<div class="course-icon intro-course-icon" aria-hidden="true"><span>Θ</span><small>n → ∞</small></div>
<div>
<h3>Введение в алгоритмы</h3>
<p>Модели вычислений, временная и пространственная сложность, асимптотическая нотация и типичные скорости роста.</p>
</div>
</a>
'''
if 'href="introduction/index-ru.html"' not in index_ru:
    index_ru = index_ru.replace('<div class="course-grid">\n', '<div class="course-grid">\n' + intro_card_ru, 1)
write('index-ru.html', index_ru)

# Sorting becomes Chapter 2 and explicitly points back to the foundations chapter.
sorting = read('sorting/index.html')
sorting = sorting.replace('<div class="chapter-label">Chapter 1</div>', '<div class="chapter-label">Chapter 2</div>', 1)
if 'chapter-prereq-note' not in sorting:
    sorting = sorting.replace(
        '<h1>Sorting</h1>\n',
        '<h1>Sorting</h1>\n<div class="chapter-prereq-note">Need a refresher on <strong>Θ, O, worst-case time, or auxiliary space</strong>? <a href="../introduction/">Review Introduction to Algorithms →</a></div>\n',
        1,
    )
write('sorting/index.html', sorting)

sorting_ru = read('sorting/index-ru.html')
sorting_ru = sorting_ru.replace('<div class="chapter-label">Глава 1</div>', '<div class="chapter-label">Глава 2</div>', 1)
if 'chapter-prereq-note' not in sorting_ru:
    sorting_ru = sorting_ru.replace(
        '<h1>Сортировки</h1>\n',
        '<h1>Сортировки</h1>\n<div class="chapter-prereq-note">Нужно освежить <strong>Θ, O, худший случай или дополнительную память</strong>? <a href="../introduction/index-ru.html">Вернуться к введению в алгоритмы →</a></div>\n',
        1,
    )
write('sorting/index-ru.html', sorting_ru)

# Shared visual styling for the new home card and prerequisite note.
styles = read('assets/css/styles.css')
marker = '/* ---------- Introduction chapter integration ---------- */'
if marker not in styles:
    styles += r'''

/* ---------- Introduction chapter integration ---------- */
.intro-course-icon {
  flex-direction: column;
  gap: 1px;
  background: linear-gradient(180deg, #f3f5ec 0%, #e9eee0 100%);
  color: #556d37;
}

.intro-course-icon span {
  display: block;
  font: 700 35px/1 Georgia, serif;
}

.intro-course-icon small {
  display: block;
  color: #7a876a;
  font: 700 9px/1.1 "SFMono-Regular", Consolas, monospace;
  letter-spacing: .03em;
}

.chapter-prereq-note {
  margin: 7px 0 34px;
  padding: 13px 16px;
  border: 1px solid #dfe5d4;
  border-radius: 12px;
  background: #f7f9f2;
  color: #657069;
  font-size: 13px;
  line-height: 1.55;
}

.chapter-prereq-note strong { color: #4f5d45; }
.chapter-prereq-note a {
  color: #55752d;
  font-weight: 800;
  text-decoration: none;
}
.chapter-prereq-note a:hover { text-decoration: underline; }
'''
write('assets/css/styles.css', styles)

# README structure.
readme = read('README.md')
if 'introduction/' not in readme:
    readme += '''\n\n## Published chapters\n\n- `introduction/` — algorithm analysis foundations: computation model, time, memory, and asymptotic notation.\n- `sorting/` — sorting theory and practice problems.\n'''
    write('README.md', readme)

# Basic consistency checks.
assert 'href="introduction/"' in read('index.html')
assert 'href="introduction/index-ru.html"' in read('index-ru.html')
assert 'Chapter 2' in read('sorting/index.html')
assert 'Глава 2' in read('sorting/index-ru.html')
assert '../introduction/' in read('sorting/index.html')
assert '../introduction/index-ru.html' in read('sorting/index-ru.html')
assert (ROOT / 'introduction/index.html').exists()
assert (ROOT / 'introduction/index-ru.html').exists()
assert (ROOT / 'introduction/styles.css').exists()
print('Introduction chapter integrated successfully.')
