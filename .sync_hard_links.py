from pathlib import Path


def replace(path, old, new):
    p = Path(path)
    text = p.read_text(encoding='utf-8')
    if old not in text:
        raise RuntimeError(f'Expected text not found in {path}: {old}')
    p.write_text(text.replace(old, new), encoding='utf-8')

# Russian practice index: Hard pages are now bilingual.
replace('sorting-problems-ru.html', 'href="problem-top-k-frequent.html"', 'href="problem-top-k-frequent-ru.html"')
replace('sorting-problems-ru.html', 'href="problem-merge-without-space.html"', 'href="problem-merge-without-space-ru.html"')
replace('sorting-problems-ru.html', 'href="problem-closest-pair.html"', 'href="problem-closest-pair-ru.html"')
replace('sorting-problems-ru.html', '<span class="problem-open">Открыть решение · EN →</span>', '<span class="problem-open">Открыть решение →</span>')
replace('sorting-problems-ru.html', 'Слить два отсортированных массива на месте, рассматривая их как одну виртуальную последовательность.', 'Разделить значения между двумя массивами и восстановить порядок с O(1) дополнительной памятью.')
replace('sorting-problems-ru.html', 'Страницы Medium доступны на русском и английском; остальные решения пока остаются на английском.', 'Страницы Medium и Hard доступны на русском и английском; решения Easy пока остаются на английском.')

# English card should describe the new algorithm rather than the old gap-method presentation.
replace('sorting-problems.html', 'Merge two sorted arrays in place by treating them as one virtual sequence.', 'Separate the values between two sorted arrays, then restore order with O(1) auxiliary space.')

# Russian Applications should enter the Russian Hard pages.
replace('sorting-applications-ru.html', 'href="problem-top-k-frequent.html"', 'href="problem-top-k-frequent-ru.html"')
replace('sorting-applications-ru.html', 'href="problem-merge-without-space.html"', 'href="problem-merge-without-space-ru.html"')
replace('sorting-applications-ru.html', '<span class="application-practice-label">Практика · EN</span>\n          <a href="problem-top-k-frequent-ru.html">', '<span class="application-practice-label">Практика</span>\n          <a href="problem-top-k-frequent-ru.html">')
replace('sorting-applications-ru.html', '<span class="application-practice-label">Практика · EN</span>\n          <a href="problem-merge-without-space-ru.html">', '<span class="application-practice-label">Практика</span>\n          <a href="problem-merge-without-space-ru.html">')

print('Hard practice links synchronized.')
