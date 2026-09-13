from pathlib import Path


def transform(path, replacements):
    p = Path(path)
    text = p.read_text(encoding='utf-8')
    for old, new in replacements:
        if old not in text:
            raise RuntimeError(f'Missing text in {path}: {old}')
        text = text.replace(old, new)
    p.write_text(text, encoding='utf-8')


transform('problem-closest-pair.html', [
    (
        'Split that rectangle at the recursion boundary and then divide each half into four <code>d/2 × d/2</code> cells. Inside one half, two points cannot occupy the same cell: their distance would be less than <code>d</code>, contradicting the recursive answer for that half. Thus there are at most eight points in the rectangle including <code>p</code>, so at most seven following candidates need to be checked.',
        'Divide that rectangle into eight <code>d/2 × d/2</code> cells. Two points from the same recursive half cannot occupy one cell: the cell diameter is <code>d/√2 &lt; d</code>, contradicting the recursive answer for that half. A cell can therefore contain at most two points — one from each half. Across eight cells there are at most sixteen points including <code>p</code>, so at most fifteen following candidates need to be checked. The classical analysis can sharpen this constant to seven with a tighter packing argument, but fifteen is already sufficient for the same O(n log n) running time.'
    ),
    ('<strong>next 7</strong>', '<strong>next 15</strong>'),
    ('Why at most seven following points?', 'Why at most fifteen following points?'),
    ('test at most the next seven points.', 'test at most the next fifteen points.'),
    ('among the next seven points in y-order.', 'among the next fifteen points in y-order.'),
    ('min(i + 8, len(strip))', 'min(i + 16, len(strip))'),
    ('<b><code>min(i + 8, ...)</code></b><p>Checks at most seven following points, exactly as guaranteed by the packing lemma.</p>', '<b><code>min(i + 16, ...)</code></b><p>Checks at most fifteen following points, exactly as guaranteed by the packing lemma used on this page.</p>'),
])

transform('problem-closest-pair-ru.html', [
    (
        'Разделим его линией рекурсии, а каждую половину — на четыре квадрата <code>d/2 × d/2</code>. В одном таком квадрате внутри одной рекурсивной половины не могут находиться две точки: их расстояние было бы меньше <code>d</code>, что противоречит уже найденному расстоянию для этой половины. Поэтому в прямоугольнике помещается не более восьми точек вместе с <code>p</code>, то есть после <code>p</code> нужно проверить не более семи кандидатов.',
        'Разделим этот прямоугольник на восемь квадратов <code>d/2 × d/2</code>. Две точки из одной и той же рекурсивной половины не могут попасть в один квадрат: диаметр такого квадрата равен <code>d/√2 &lt; d</code>, что противоречит уже найденному расстоянию внутри этой половины. Поэтому в одном квадрате может быть не более двух точек — по одной из каждой половины. Всего в восьми квадратах находится не более шестнадцати точек вместе с <code>p</code>, то есть после <code>p</code> достаточно проверить не более пятнадцати кандидатов. Классический более тонкий packing-аргумент уменьшает эту константу до семи, но для той же сложности O(n log n) достаточно пятнадцати.'
    ),
    ('<strong>следующие 7</strong>', '<strong>следующие 15</strong>'),
    ('Почему достаточно семи следующих точек?', 'Почему достаточно пятнадцати следующих точек?'),
    ('для каждой проверяем максимум семь следующих.', 'для каждой проверяем максимум пятнадцать следующих.'),
    ('среди следующих семи точек в y-порядке.', 'среди следующих пятнадцати точек в y-порядке.'),
    ('min(i + 8, len(strip))', 'min(i + 16, len(strip))'),
    ('<b><code>min(i + 8, ...)</code></b><p>Проверяет не более семи следующих точек — ровно столько разрешает packing-лемма.</p>', '<b><code>min(i + 16, ...)</code></b><p>Проверяет не более пятнадцати следующих точек — именно такую простую и полностью общую границу доказывает packing-лемма на этой странице.</p>'),
])

print('Closest Pair proof and implementation updated to the robust 15-neighbor bound.')
