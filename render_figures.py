"""Render paper figures with Pillow and pypdfium2; run from any directory."""
import argparse
from pathlib import Path

from PIL import Image
import pypdfium2 as pdfium

ASSETS = Path(__file__).resolve().parent / 'assets'
# Zero-based PDF pages; crop boxes in PDF points, measured from the top left.
FIGURES = [
    ('problem', 1, (105, 78, 508, 283)),
    ('pipeline', 4, (105, 78, 508, 309)),
    ('training', 5, (105, 78, 508, 261)),
    ('case-1', 18, (105, 78, 508, 428)),
    ('case-2', 19, (105, 78, 508, 377)),
]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('manuscript', type=Path, help='Source manuscript PDF (not included in site assets)')
    args = parser.parse_args()
    pdf = pdfium.PdfDocument(args.manuscript)
    try:
        for name, page_number, box in FIGURES:
            page = pdf[page_number]
            scale = 8
            bitmap = page.render(scale=scale)
            full = bitmap.to_pil().convert('RGB')
            figure = full.crop(tuple(round(v * scale) for v in box))
            figure.save(ASSETS / f'{name}-hd.webp', quality=94, method=6)
            retina = figure.resize((figure.width * 3 // 4, figure.height * 3 // 4), Image.Resampling.LANCZOS)
            retina.save(ASSETS / f'{name}-2x.webp', quality=90, method=6)
            preview = figure.resize((figure.width // 2, figure.height // 2), Image.Resampling.LANCZOS)
            preview.save(ASSETS / f'{name}.webp', quality=92, method=6)
            print(f'{name}: {preview.size} preview; {figure.size} full resolution', flush=True)
            bitmap.close()
            page.close()
    finally:
        pdf.close()


if __name__ == '__main__':
    main()
