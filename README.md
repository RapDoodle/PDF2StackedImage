# PDF2StackedImage
A simple tool that converts PDFs into a stacked image.

## Usage

For Windows users,

```
Convert a PDF to a vertically-stacked image.

optional arguments:
  -h, --help            show this help message and exit
  -i DIR, --input DIR   Input PDF file
  -o DIR, --output DIR  Output image file
  -w INT, --width INT   Output image width. Default: maximum width among all pages
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

