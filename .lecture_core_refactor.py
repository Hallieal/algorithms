from pathlib import Path
import re

ROOT = Path('.')


def read(name):
    return (ROOT / name).read_text(encoding='utf-8')


def write(name, text):
    (ROOT / name).write_text(text, encoding='utf-8', newline='\n')


def ensure_core_script(text):
    if 'lecture-core.js' in text:
        return text
    marker = '<script>\n(() => {'
    if marker not in text:
        raise RuntimeError('Could not find inline lecture script')
    return text.replace(marker, '<script src="lecture-core.js"></script>\n' + marker, 1)


def remove_common_tail(text):
    pattern = re.compile(
        r'\n  document\.addEventListener\("click", event => \{.*?\n\}\)\(\);\n</script>',
        re.S,
    )
    text, n = pattern.subn('\n})();\n</script>', text, count=1)
    if n != 1:
        raise RuntimeError('Could not remove duplicated lecture tail')
    return text


# Selection + Insertion: keep step generation/rendering page-specific, share controls.
def refactor_selection(name):
    text = read(name)
    text = ensure_core_script(text)
    pattern = re.compile(
        r'  document\.querySelectorAll\("\.visualizer"\)\.forEach\(viz => \{.*?\n  \}\);\n\n(?=  document\.addEventListener)',
        re.S,
    )
    replacement = '''  document.querySelectorAll(".visualizer").forEach(viz => {
    const type = viz.dataset.algorithm;
    LectureCore.mountStepper(viz, {
      initial: DEFAULTS[type],
      build: array => buildSteps(type, array),
      render: renderVisualizer,
      randomize: randomArray,
      store: "_steps"
    });
  });

'''
    text, n = pattern.subn(replacement, text, count=1)
    if n != 1:
        raise RuntimeError(f'{name}: visualizer controller not found')
    text = remove_common_tail(text)
    write(name, text)


# Bubble Sort.
def refactor_bubble(name):
    text = read(name)
    text = ensure_core_script(text)
    pattern = re.compile(
        r'  const viz = document\.querySelector\(\'\.visualizer\[data-algorithm="bubble"\]\'\);.*?\n  \}\n\n(?=  document\.addEventListener)',
        re.S,
    )
    replacement = '''  const viz = document.querySelector('.visualizer[data-algorithm="bubble"]');
  if (viz) {
    LectureCore.mountStepper(viz, {
      initial: DEFAULT,
      build: bubbleSteps,
      render,
      randomize: randomArray,
      store: "_steps"
    });
  }

'''
    text, n = pattern.subn(replacement, text, count=1)
    if n != 1:
        raise RuntimeError(f'{name}: bubble controller not found')
    text = remove_common_tail(text)
    write(name, text)


# Merge Sort has two independent stepped demonstrations.
def refactor_merge(name):
    text = read(name)
    text = ensure_core_script(text)

    p1 = re.compile(
        r'  const mergeDemo = document\.getElementById\("merge-operation-demo"\);.*?\n  \}\n\n(?=  /\* ---------------- Full Merge Sort)',
        re.S,
    )
    r1 = '''  const mergeDemo = document.getElementById("merge-operation-demo");
  if (mergeDemo) {
    LectureCore.mountStepper(mergeDemo, {
      initial: { left: LEFT, right: RIGHT },
      build: data => mergeOperationStates(data.left, data.right),
      render: renderMergeOperation,
      store: "_states",
      nextAction: "next-merge",
      resetAction: "reset-merge"
    });
  }

'''
    text, n1 = p1.subn(r1, text, count=1)
    if n1 != 1:
        raise RuntimeError(f'{name}: merge-operation controller not found')

    p2 = re.compile(
        r'  const mergeSortViz = document\.querySelector\(\s*\'\.visualizer\[data-algorithm="merge-sort"\]\'\s*\);.*?\n  \}\n\n(?=  /\* ---------------- Revealable answers)',
        re.S,
    )
    r2 = '''  const mergeSortViz = document.querySelector('.visualizer[data-algorithm="merge-sort"]');
  if (mergeSortViz) {
    LectureCore.mountStepper(mergeSortViz, {
      initial: DEFAULT_SORT,
      build: mergeSortStates,
      render: renderMergeSort,
      randomize: randomArray,
      store: "_states",
      nextAction: "next-sort",
      resetAction: "reset-sort",
      randomizeAction: "randomize-sort"
    });
  }

'''
    text, n2 = p2.subn(r2, text, count=1)
    if n2 != 1:
        raise RuntimeError(f'{name}: merge-sort controller not found')

    text = remove_common_tail(text)
    write(name, text)


# Quick Sort partition visualizer.
def refactor_quick(name):
    text = read(name)
    text = ensure_core_script(text)
    pattern = re.compile(
        r'  const partitionDemo = document\.getElementById\("quick-partition-demo"\);.*?\n  \}\n\n(?=  /\* -------------------------------------------------------\n     Revealable answers)',
        re.S,
    )
    replacement = '''  const partitionDemo = document.getElementById("quick-partition-demo");
  if (partitionDemo) {
    LectureCore.mountStepper(partitionDemo, {
      initial: DEFAULT_PARTITION,
      build: partitionStates,
      render: renderPartition,
      randomize: randomUniqueArray,
      store: "_states",
      nextAction: "next-partition",
      resetAction: "reset-partition",
      randomizeAction: "new-partition"
    });
  }

'''
    text, n = pattern.subn(replacement, text, count=1)
    if n != 1:
        raise RuntimeError(f'{name}: partition controller not found')
    text = remove_common_tail(text)
    write(name, text)


for page in ('sorting-selection-insertion.html', 'sorting-selection-insertion-ru.html'):
    refactor_selection(page)
for page in ('sorting-bubble.html', 'sorting-bubble-ru.html'):
    refactor_bubble(page)
for page in ('sorting-merge.html', 'sorting-merge-ru.html'):
    refactor_merge(page)
for page in ('sorting-quick.html', 'sorting-quick-ru.html'):
    refactor_quick(page)


# The current core sequence ends at Quick Sort; do not link into an inactive placeholder.
quick = read('sorting-quick.html')
quick_pattern = re.compile(
    r'<div class="next-part">\s*<h3>Next section: Counting Sort</h3>.*?<a class="next-part-link" href="sorting-counting\.html">.*?</a>\s*</div>',
    re.S,
)
quick_replacement = '''<div class="next-part">
<h3>Continue with practice</h3>
<p>
          The published core sorting sequence ends here for now. Apply the ideas from this chapter to problems of increasing difficulty.
        </p>
<a class="next-part-link" href="sorting-problems.html">Practice Problems →</a>
</div>'''
quick, n = quick_pattern.subn(quick_replacement, quick, count=1)
if n != 1:
    raise RuntimeError('English Quick Sort next-section block not found')
write('sorting-quick.html', quick)

quick_ru = read('sorting-quick-ru.html')
quick_ru_pattern = re.compile(
    r'<div class="next-part">\s*<h3>.*?</h3>.*?<a class="next-part-link" href="sorting-counting-ru\.html">.*?</a>\s*</div>',
    re.S,
)
quick_ru_replacement = '''<div class="next-part">
<h3>Перейти к практике</h3>
<p>
          На этом опубликованная основная часть главы о сортировках пока заканчивается. Закрепите идеи главы на задачах возрастающей сложности.
        </p>
<a class="next-part-link" href="sorting-problems-ru.html">Практические задачи →</a>
</div>'''
quick_ru, n = quick_ru_pattern.subn(quick_ru_replacement, quick_ru, count=1)
if n != 1:
    raise RuntimeError('Russian Quick Sort next-section block not found')
write('sorting-quick-ru.html', quick_ru)


# Ensure language-switch persistence is present on Applications pages too.
for page in ('sorting-applications.html', 'sorting-applications-ru.html'):
    text = read(page)
    if 'language-switch.js' not in text:
        text = text.replace('</body>', '<script src="language-switch.js"></script>\n</body>', 1)
        write(page, text)


# Validation.
for page in (
    'sorting-selection-insertion.html', 'sorting-selection-insertion-ru.html',
    'sorting-bubble.html', 'sorting-bubble-ru.html',
    'sorting-merge.html', 'sorting-merge-ru.html',
    'sorting-quick.html', 'sorting-quick-ru.html',
):
    text = read(page)
    assert 'lecture-core.js' in text, page
    assert 'document.addEventListener("click", event =>' not in text, page
    assert 'function updateProgress()' not in text, page

assert 'href="sorting-counting.html"' not in read('sorting-quick.html')
assert 'href="sorting-counting-ru.html"' not in read('sorting-quick-ru.html')
assert 'sorting-problems.html' in read('sorting-quick.html')
assert 'sorting-problems-ru.html' in read('sorting-quick-ru.html')
print('Lecture interaction refactor validated.')
