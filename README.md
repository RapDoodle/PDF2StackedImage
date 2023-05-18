# PDF2StackedImage
A simple tool that converts PDFs into a stacked image.

## Usage

For Windows users,

```
Convert a PDF to a vertically-stacked image.

optional arguments:
  -h, --help            show this help message and exit
  -i DIR, --input DIR   Input PDF file.
  -o DIR, --output DIR  Output image file.
  -w INT, --width INT   Output image width. Default: maximum width among all pages.
  --pdf-to-img-dpi INT  Image quality for the images converted from PDF, in DPI. Default: 300.
  --first-page INT      First page to process. Default: None.
  --last-page INT       Last page to process. Default: None.
  -s, --include-separators
                        Add a separator between pages. Default: False.
  --separator-height SEPARATOR_HEIGHT
                        Separator height. Only used when --separator is used. Default: 5.
```

### Examples

All the examples are for Linux and macOS users. If you are on Windows, you may need to replace `python3` with `python` to avoid bringing up Windows Store.


1. Convert `TestPDF.pdf` to `TestPDF.png`

    ```bash
    $ python3 pdf_to_stacked_img.py -i "TestPDF.pdf" -o "TestPDF.png"
    ```

2. Convert `TestPDF.pdf` to `TestPDF.png`. The expected output image width is `2000`.

    ```bash
    $ python3 pdf_to_stacked_img.py -i "TestPDF.pdf" -o "TestPDF.png" -w 2000
    ```

3. Convert `TestPDF.pdf` to `TestPDF.png`, with a separator between pages.

    ```bash
    $ python3 pdf_to_stacked_img.py -i "TestPDF.pdf" -o "TestPDF.png" --include-separators
    ```

4. Convert `TestPDF.pdf` to `TestPDF.png`, with a separator between pages. The width of the separator should be 10 pixels (the default is 5).

    ```bash
    $ python3 pdf_to_stacked_img.py -i "TestPDF.pdf" -o "TestPDF.png" --include-separators --separator-height 10
    ```

5. Convert `TestPDF.pdf` to `TestPDF.png`, with a PDF-to-image conversion DPI of 72.

    ```bash
    $ python3 pdf_to_stacked_img.py -i "TestPDF.pdf" -o "TestPDF.png" --pdf-to-img-dpi 72
    ```

6. Convert `TestPDF.pdf`'s page 2 to 5, to `TestPDF.png`

    ```bash
    $ python3 pdf_to_stacked_img.py -i "TestPDF.pdf" -o "TestPDF.png" --first-page 2 --last-page 5
    ```