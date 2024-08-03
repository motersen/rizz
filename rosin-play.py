#!/usr/bin/env python3
import sys
import os.path
import re
import pymupdf

try:
    [chord_list, pdf] = sys.argv[1:3]
except ValueError:
    print("Not enough arguments")
    sys.exit(1)

out = sys.argv[3] if len(sys.argv) > 3 else os.path.splitext(pdf)[0] + "-chords.pdf"

try:
    doc = pymupdf.open(pdf)
except pymupdf.FileNotFoundError as E:
    for a in E.args: print(a)
    sys.exit(1)

try:
    with open(chord_list) as f:
        chords = f.read().splitlines()
except OSError as E:
    print(f"Could not open '{E.filename}': {E.strerror}")
    sys.exit(1)

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
    sh.finish(color=(1,1,1), fill=(1,1,1))
    sh.commit()

## replace with chord symbol pdf
def replace(page, rects):
    for c in range(len(chords)):
        chord = pymupdf.open(f"pdf/{c+1}.pdf")
        slashc = re.search("/[A-H]", chords[c])
        for rec in rects[c]:
            ## slashchords are taller and need more vertical space
            ## double rectangle height and move bottom border down by 2/5 orig. height
            page.show_pdf_page(rec - (0,
                                      .6 * rec.height if slashc else 0,
                                      0,
                                      - .4 * rec.height if slashc else 0),
                               chord, 0)
        chord.close()

for page in doc:
    rects = collect(page)
    conceal(page, rects)
    replace(page, rects)

doc.save(out)
