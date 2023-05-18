#!/usr/bin/env python3

"""
pdf_to_stacked_img.py

Converts a PDF file to a vertically-stack image.

Usage:
    python pdf_to_stacked_img.py -i /path/to/your/pdf/file.pdf -o /path/to/output/image.jpg
"""

import os
import argparse
import warnings
from PIL import Image
from pdf2image import convert_from_path

MAX_IMG_DIM = 65000


def is_jpeg(filename):
    _, ext = os.path.splitext(filename)
    return ext.lower() in ('.jpg', '.jpeg')


def main(pdf_path: str, output_path: str, output_width: int):
    images = convert_from_path(pdf_path)

    # Get the maximum width
    if output_width is None:
        output_width = max([img.width for img in images])
    if output_width > MAX_IMG_DIM:
        output_width = MAX_IMG_DIM
        warnings.warn('Width exceeding 65000. Capped at 65000.')

    # Resize to equal width
    for i in range(len(images)):
        img = images[i]
        if img.width != output_width:
            print(f'Resizing page {i} to width {output_width}...')
            wpercent = (output_width / float(img.size[0]))
            hsize = int((float(img.size[1]) * float(wpercent)))
            rescaled_img = img.resize((output_width, hsize), Image.Resampling.LANCZOS)
            images[i] = rescaled_img

    # Generate the stacked image
    total_height = sum([img.height for img in images])
    if is_jpeg(output_path) and total_height > MAX_IMG_DIM:
        print('Error: Output height exceeded JPEG\'s maximum width (65000). Consider using PNG.')
        exit(1)
    new_img = Image.new('RGB', (output_width, total_height))
    y_offset = 0
    for img in images:
        new_img.paste(img, (0, y_offset))
        y_offset += img.height
    new_img.save(output_path)
    print(f'Image successfully saved in {output_path}. Dimension {new_img.width} x {new_img.height}.')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert a PDF to a vertically-stacked image.")
    parser.add_argument(
        '-i', 
        '--input', 
        metavar='DIR',
        required=True, 
        help='Input PDF file')
    parser.add_argument(
        '-o', 
        '--output', 
        metavar='DIR',
        required=False,
        default='stacked.png',
        help='Output image file')
    parser.add_argument(
        '-w', 
        '--width', 
        metavar='INT',
        required=False,
        type=int,
        default=None,
        help='Output image width. Default: maximum width among all pages')
    args = parser.parse_args()

    main(args.input, args.output, args.width)