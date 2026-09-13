from pathlib import Path
import re
import sys

ROOT = Path.cwd()

# 1) Fix the accidental placeholder used inside mathematical complexity notation.
# Keep the ordinary English adjective "loglinear" untouched in prose/headings.
complexity_files = [
    "sorting-merge.html",
    "sorting-quick.html",
    "sorting-merge-ru.html",
    "sorting-quick-ru.html",
]

print("AHA sorting update")
print("=" * 48)

total_math_fixes = 0
missing = []
for name in complexity_files:
    path = ROOT / name
    if not path.exists():
        missing.append(name)
        print(f"[missing] {name}")
        continue

    text = path.read_text(encoding="utf-8")
    count = text.count("Θ(loglinear)")
    if count:
        text = text.replace("Θ(loglinear)", "Θ(n log n)")
        path.write_text(text, encoding="utf-8", newline="\n")
        total_math_fixes += count
        print(f"[fixed]   {name}: {count} mathematical occurrence(s)")
    else:
        print(f"[ok]      {name}: no Θ(loglinear) remains")

# 2) Connect Applications of Sorting directly to relevant practice problems.
apps = ROOT / "sorting-applications.html"
if not apps.exists():
    missing.append("sorting-applications.html")
    print("[missing] sorting-applications.html")
else:
    text = apps.read_text(encoding="utf-8")

    if ".application-practice {" not in text:
        css = r'''

    .application-practice {
      display:flex;
      flex-wrap:wrap;
      gap:8px;
      margin-top:16px;
      padding-top:14px;
      border-top:1px solid var(--line);
    }

    .application-practice-label {
      flex-basis:100%;
      color:#8a9299;
      font-size:10px;
      font-weight:800;
      letter-spacing:.07em;
      text-transform:uppercase;
    }

    .application-practice a {
      display:inline-flex;
      align-items:center;
      min-height:30px;
      padding:6px 10px;
      border-radius:999px;
      background:#f3f6ed;
      color:#58762f;
      font-size:12px;
      font-weight:760;
      line-height:1.35;
      text-decoration:none;
      transition:background .15s ease, color .15s ease;
    }

    .application-practice a:hover {
      background:#e8f0dc;
      color:#405b1f;
    }
'''
        marker = "\n    @media (max-width:760px) {"
        if marker not in text:
            raise RuntimeError("Could not find the Applications CSS insertion point.")
        text = text.replace(marker, css + marker, 1)

    practice_by_title = {
        "Pairs and intervals": [
            ("problem-two-sum-sorted.html", "Two Sum in a Sorted Array"),
            ("problem-meeting-rooms.html", "Meeting Rooms"),
        ],
        "Combining ordered data": [
            ("problem-merge-without-space.html", "Merge Without Extra Space"),
        ],
        "Order-based summaries": [
            ("problem-k-smallest.html", "K Smallest Elements"),
        ],
    }

    def add_practice(block: str, links):
        if 'class="application-practice"' in block:
            return block, False
        lines = [
            '          <div class="application-practice">',
            '            <span class="application-practice-label">Practice</span>',
        ]
        for href, label in links:
            lines.append(f'            <a href="{href}">{label} →</a>')
        lines.append('          </div>')
        addition = "\n" + "\n".join(lines) + "\n        "
        return block.replace("</article>", addition + "</article>", 1), True

    added_cards = 0
    for title, links in practice_by_title.items():
        pattern = re.compile(
            r'(<article class="application-card">(?:(?!<article class="application-card">).)*?'
            + re.escape(f"<h3>{title}</h3>")
            + r'.*?</article>)',
            re.DOTALL,
        )
        match = pattern.search(text)
        if not match:
            raise RuntimeError(f"Could not find application card: {title}")
        new_block, changed = add_practice(match.group(1), links)
        if changed:
            text = text[:match.start(1)] + new_block + text[match.end(1):]
            added_cards += 1

    apps.write_text(text, encoding="utf-8", newline="\n")
    print(f"[fixed]   sorting-applications.html: practice links added to {added_cards} card(s)")

# 3) Sanity checks.
errors = []
for name in complexity_files:
    path = ROOT / name
    if path.exists() and "Θ(loglinear)" in path.read_text(encoding="utf-8"):
        errors.append(f"{name} still contains Θ(loglinear)")

if apps.exists():
    app_text = apps.read_text(encoding="utf-8")
    required_links = [
        "problem-two-sum-sorted.html",
        "problem-meeting-rooms.html",
        "problem-merge-without-space.html",
        "problem-k-smallest.html",
    ]
    for href in required_links:
        if href not in app_text:
            errors.append(f"sorting-applications.html is missing {href}")

# Practice pages intentionally remain English-only until a complete RU translation exists.
practice_index = ROOT / "sorting-problems.html"
if practice_index.exists():
    ptext = practice_index.read_text(encoding="utf-8")
    if "sorting-problems-ru.html" in ptext:
        errors.append("sorting-problems.html contains a premature RU link")

print("-" * 48)
print(f"Mathematical replacements made: {total_math_fixes}")
if missing:
    print("Missing files (not modified): " + ", ".join(dict.fromkeys(missing)))

if errors:
    print("Validation failed:")
    for error in errors:
        print(" - " + error)
    sys.exit(1)

print("Validation passed.")
print("You can now review the changes with: git diff")
