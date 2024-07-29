import sys
import pymupdf

try:
    doc = pymupdf.open(sys.argv[1])
except pymupdf.FileNotFoundError as E:
    for a in E.args: print(a)
    sys.exit()

try:
    with open("chords.txt") as f:
        chords = f.read().splitlines()
except OSError as E:
    print(f"Could not open '{E.filename}': {E.strerror}")
    sys.exit()

## collect rects for occurences of target chords
def collect(page):
    wl = page.get_text("words")
    rects = [[] for _ in range(len(chords))]

    for w in wl:
        try:
            i = chords.index(w[4])
            rec = pymupdf.Rect(*[*w][0:4])
            rects[i].append(rec)
        except ValueError:
            pass
    return rects

## cover up original text
def conceal(page, rects):
    sh = page.new_shape()
    for rect in [instance for c in rects for instance in c]:
        sh.draw_rect(rect)
    # sh.finish(color=(1,0,0))
    sh.finish(color=(1,1,1), fill=(1,1,1))
    sh.commit()


## replace with chord symbol pdf
def replace(page, rects):
    for c in range(len(chords)-1):
        chord = pymupdf.open(f"pdf/{c+1}.pdf")
        for rec in rects[c]:
            page.show_pdf_page(rec - (rec.height,
                                       .2 * rec.height,
                                       0,
                                       .2 * rec.height),
                            chord, 0)
        chord.close()

for page in doc:
    rects = collect(page)
    conceal(page, rects)
    replace(page, rects)

doc.save("nb-e.pdf")
