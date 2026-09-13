from pathlib import Path

path = Path('styles.css')
text = path.read_text(encoding='utf-8')

old = '''.course-card.planned {
  background: #f1f0ec;
  border-color: #e7e3dc;
  opacity: .54;
  cursor: default;
  user-select: none;
}
.course-card.planned .course-icon { background: #eceae5; }
.course-card.planned .course-icon img { filter: grayscale(.55); opacity: .78; }
.course-card.planned h3 { color: #596169; }
.course-card.planned p { color: #858b90; }

.chapter-card.planned {
  background: #f3f2ee !important;
  border-color: #e5e1da !important;
  opacity: .56;
  cursor: default;
  box-shadow: none !important;
  transform: none !important;
  user-select: none;
}
.chapter-card.planned:hover { box-shadow: none !important; transform: none !important; }
.chapter-card.planned .chapter-card-icon { filter: grayscale(.5); opacity: .75; }
.chapter-card.planned .planned-link {
  color: #7f868b;
  letter-spacing: .01em;
}
'''

new = '''.course-card.planned {
  background: #f8f5ef;
  border-color: #e8e0d5;
  opacity: .78;
  cursor: default;
  user-select: none;
}
.course-card.planned .course-icon {
  background: #e7dfd3;
  border-color: #ddd3c5;
}
.course-card.planned .course-icon img {
  filter: grayscale(1);
  opacity: .46;
}
.course-card.planned h3 { color: #656c72; }
.course-card.planned p { color: #858a8d; }

.chapter-card.planned {
  background: #f8f5ef !important;
  border-color: #e8e0d5 !important;
  opacity: .78;
  cursor: default;
  box-shadow: none !important;
  transform: none !important;
  user-select: none;
}
.chapter-card.planned:hover { box-shadow: none !important; transform: none !important; }
.chapter-card.planned .chapter-card-icon {
  background: #e7dfd3;
  border: 1px solid #ddd3c5;
  border-radius: 16px;
  padding: 7px;
  opacity: 1;
}
.chapter-card.planned .chapter-card-icon img {
  width: 100%;
  height: 100%;
  filter: grayscale(1);
  opacity: .46;
}
.chapter-card.planned .planned-link {
  color: #858a8d;
  letter-spacing: .01em;
}
'''

if old not in text:
    raise SystemExit('Inactive-topic CSS block not found')

path.write_text(text.replace(old, new, 1), encoding='utf-8', newline='\n')
print('Inactive topic palette updated.')
