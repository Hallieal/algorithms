from pathlib import Path


def swap(path, old, new):
    p = Path(path)
    text = p.read_text(encoding='utf-8')
    if old not in text:
        raise RuntimeError(f'Missing text in {path}: {old}')
    p.write_text(text.replace(old, new), encoding='utf-8')

# English: use the simpler robust 15-neighbor packing bound.
swap('problem-closest-pair.html', 'next 7', 'next 15')
swap('problem-closest-pair.html', 'at most the next seven points', 'at most the next fifteen points')
swap('problem-closest-pair.html', 'among the next seven points in y-order', 'among the next fifteen points in y-order')
swap('problem-closest-pair.html', 'at most seven following candidates', 'at most fifteen following candidates')
swap('problem-closest-pair.html', 'min(i + 8, len(strip))', 'min(i + 16, len(strip))')
swap('problem-closest-pair.html', 'Checks at most seven following points, exactly as guaranteed by the packing lemma.', 'Checks at most fifteen following points, exactly as guaranteed by the packing lemma used on this page.')
swap(
    'problem-closest-pair.html',
    'Split that rectangle at the recursion boundary and then divide each half into four <code>d/2 × d/2</code> cells. Inside one half, two points cannot occupy the same cell: their distance would be less than <code>d</code>, contradicting the recursive answer for that half. Thus there are at most eight points in the rectangle including <code>p</code>, so at most seven following candidates need to be checked.',
    'Divide that rectangle into eight <code>d/2 × d/2</code> cells. Two points from the same recursive half cannot occupy one cell: the cell diameter is <code>d/√2 &lt; d</code>, contradicting the recursive answer for that half. A cell can therefore contain at most two points — one from each half. Across eight cells there are at most sixteen points including <code>p</code>, so at most fifteen following candidates need to be checked. The classical analysis can sharpen this constant to seven under a slightly tighter packing argument, but fifteen is already enough for the same O(n log n) bound.',
)

# Russian mirror.
swap('problem-closest-pair-ru.html', 'следующие 7', 'следующие 15')
swap('problem-closest-pair-ru.html', 'максимум семь следующих', 'максимум пятнадцать следующих')
swap('problem-closest-pair-ru.html', 'среди следующих семи точек в y-порядке', 'среди следующих пятнадцати точек в y-порядке')
swap('problem-closest-pair-ru.html', 'не более семи следующих точек', 'не более пятнадцати следующих точек')
swap('problem-closest-pair-ru.html', 'min(i + 8, len(strip))', 'min(i + 16, len(strip))')
swap('problem-closest-pair-ru.html', 'Проверяет не более семи следующих точек — ровно столько разрешает packing-лемма.', 'Проверяет не более пятнадцати следующих точек — именно такую простую и полностью общую границу доказывает packing-лемма на этой странице.')
swap(
    'problem-closest-pair-ru.html',
    'Разделим его линией рекурсии, а каждую половину — на четыре квадрата <code>d/2 × d/2</code>. В одном таком квадрате внутри одной рекурсивной половины не могут находиться две точки: их расстояние было бы меньше <code>d</code>, что противоречит уже найденному расстоянию для этой половины. Поэтому в прямоугольнике помещается не более восьми точек вместе с <code>p</code>, то есть после <code>p</code> нужно проверить не более семи кандидатов.',
    'Разделим этот прямоугольник на восемь квадратов <code>d/2 × d/2</code>. Две точки из одной и той же рекурсивной половины не могут попасть в один квадрат: диаметр такого квадрата равен <code>d/√2 &lt; d</code>, что противоречит уже найденному расстоянию внутри этой половины. Поэтому в одном квадрате может быть не более двух точек — по одной из каждой половины. Всего в восьми квадратах находится не более шестнадцати точек вместе с <code>p</code>, то есть после <code>p</code> достаточно проверить не более пятнадцати кандидатов. Классический более тонкий packing-аргумент уменьшает константу до семи, но для сложности O(n log n) это не требуется.',
)

print('Closest Pair proof and implementation updated to the robust 15-neighbor bound.')
