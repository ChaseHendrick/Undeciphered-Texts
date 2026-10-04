# Pen pressure, 4 October 2026

Not a reading of any historical page. The ink and the pressure are different channels.

## What pressure can hide

Francis Bacon's biliteral cipher does not hide the secret in the choice of words. Each secret letter is five marks, and each mark is one of two forms. In the 1623 *De Augmentis Scientiarum* he drew two handwritten forms of each letter, an a-form and a b-form. A heavy stroke and a light stroke are one physical way to make those two forms. The sentence a casual reader sees is cover text. The secret is the pressure, or the typeface, or whichever other pair of forms the writer agreed on. The repo already decodes a supplied a/b string in `engine/solvers/baconian.py`. `engine/pen_pressure.py` only translates an explicit `L`/`H` string into that channel. Light is the a-form and heavy is the b-form. A string of ordinary letters is rejected.

A pinprick is the other old pressure method. A pin is pushed through chosen letters of a printed page or a letter. Held up to a lamp, the holes pick out the message and the rest of the printing is cover. The module reads those holes only when the caller gives the positions. It does not decide which letters look as if they were pricked.

## What pressure leaves behind by accident

Writing on a pad indents the sheet underneath. That indent is not a designed cipher. It is leakage. Oblique light shows the deeper marks. Rubbing a pencil across the sheet can show them too, and it can spoil the page, which is why a document lab avoids it. In 1979 Foster and Morantz described an electrostatic image that develops indentations, including some oblique light misses (*Forensic Science International* 13, 51-54). The Foster and Freeman ESDA became the usual instrument. It is not magic. Welch's 2021 note records indentations that oblique light still showed and ESDA did not, after the paper had been pressed against plastic.

Carbon paper is the intentional version of the same transfer. Pressure on the top sheet lays graphite on the sheet below. Early agency practice used that as a way to keep a second copy, which is a pressure channel on purpose.

## What a transcription cannot do

If the only record is the letters, the heavy strokes, the light strokes, the pinholes, and the indent on the next sheet are already gone. `ink_alone` returns no text. A language score on those letters does not reconstruct the pressure, and this note does not claim one.
