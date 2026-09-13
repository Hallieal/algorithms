from pathlib import Path

ROOT = Path('.')


def rw(path, fn):
    p = ROOT / path
    text = p.read_text(encoding='utf-8')
    new = fn(text)
    p.write_text(new, encoding='utf-8', newline='\n')


def patch_home(text):
    text = text.replace('assets/images/topic-introduction.svg"', 'assets/images/topic-introduction.svg?v=3"')
    text = text.replace('assets/images/topic-introduction.svg?v=2"', 'assets/images/topic-introduction.svg?v=3"')
    return text


def patch_intro(text, ru=False):
    if 'interactive.css' not in text:
        text = text.replace('<link rel="stylesheet" href="styles.css">', '<link rel="stylesheet" href="styles.css">\n  <link rel="stylesheet" href="interactive.css?v=1">', 1)
    text = text.replace('src="growth.js"', 'src="growth.js?v=3"')
    text = text.replace('src="growth.js?v=2"', 'src="growth.js?v=3"')
    if 'growth-slider-instruction' not in text:
        label = 'Двигайте ползунок, чтобы менять n' if ru else 'Drag the slider to change n'
        text = text.replace('<div class="growth-slider-block">\n          <input', f'<div class="growth-slider-block">\n          <div class="growth-slider-instruction">{label}</div>\n          <input', 1)
    assert 'foundation-card-mark' not in text
    return text


rw('index.html', patch_home)
rw('index-ru.html', patch_home)
rw('introduction/index.html', lambda t: patch_intro(t, False))
rw('introduction/index-ru.html', lambda t: patch_intro(t, True))

for path in ['introduction/index.html', 'introduction/index-ru.html']:
    text = (ROOT / path).read_text(encoding='utf-8')
    assert 'interactive.css?v=1' in text
    assert 'growth.js?v=3' in text
    assert 'growth-slider-instruction' in text
    assert 'foundation-card-mark' not in text

print('Introduction icon cache-bust and slider visibility patch validated.')
