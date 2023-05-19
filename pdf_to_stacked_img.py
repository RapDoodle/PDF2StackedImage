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
from string import Template

from PIL import Image
from pdf2image import convert_from_path

MAX_IMG_DIM = 65000


def is_jpeg(filename):
    _, ext = os.path.splitext(filename)
    return ext.lower() in ('.jpg', '.jpeg')


def main(args):
    pdf_files = []
    if os.path.isdir(args.input):
        for root, dirs, files in os.walk(args.input):
            for file in files:
                if file.lower().endswith('.pdf'):
                    pdf_files.append(os.path.join(root, file))
    else:
        # A file
        pdf_files.append(args.input)
    
    # Template for output string
    for index, pdf_file in enumerate(pdf_files):
        print(f'Processing {pdf_file}...')
        pdf_filename, _ = os.path.splitext(os.path.basename(pdf_file))
        output_path = args.output.format(**{
            'filename': pdf_filename,
            'number': index
        })
        output_width = args.width
        include_separators = args.include_separators
        separator_height = args.separator_height
        is_target_img_jpeg = is_jpeg(output_path)

        # Convert PDF into images
        pdf_images = convert_from_path(
            pdf_file,
            first_page=args.first_page,
            last_page=args.last_page,
            dpi=args.pdf_to_img_dpi
        )

        # Get the maximum width
        if output_width is None:
            output_width = max([img.width for img in pdf_images])
        if is_target_img_jpeg and output_width > MAX_IMG_DIM:
            output_width = MAX_IMG_DIM
            warnings.warn('Width exceeding 65000. Capped at 65000.')

        # Resize to equal width
        for i in range(len(pdf_images)):
            img = pdf_images[i]
            if img.width != output_width:
                print(f'Resizing page {i} to width {output_width}...')
                wpercent = (output_width / float(img.size[0]))
                hsize = int((float(img.size[1]) * float(wpercent)))
                rescaled_img = img.resize((output_width, hsize), Image.Resampling.LANCZOS)
                pdf_images[i] = rescaled_img
        
        # (Optionally) add a separator image after each page, except the last one
        output_images = []
        for i, img in enumerate(pdf_images):
            output_images.append(img)
            if include_separators and i < len(pdf_images) - 1:
                separator = Image.new('RGB', (output_width, separator_height), 'black')
                output_images.append(separator)

        # Generate the stacked image
        total_height = sum([img.height for img in output_images])
        if is_target_img_jpeg and total_height > MAX_IMG_DIM:
            print('Error: Output height exceeded JPEG\'s maximum width (65000). Consider using PNG.')
            exit(1)
        new_img = Image.new('RGB', (output_width, total_height))
        y_offset = 0
        for img in output_images:
            new_img.paste(img, (0, y_offset))
            y_offset += img.height
        new_img.save(output_path)
        print(f'Stacked {pdf_file} was successfully saved as {output_path}. Image resolution: {new_img.width} x {new_img.height}.')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert a PDF to a vertically-stacked image.")
    parser.add_argument(
        '-i', 
        '--input', 
        metavar='DIR',
        required=True, 
        help='Input PDF file or folder containing PDF files.')
    parser.add_argument(
        '-o', 
        '--output', 
        metavar='DIR',
        required=False,
        default='stacked {filename}.png',
        help='Output image file. Default: stacked {filename}.png')
    parser.add_argument(
        '-w', 
        '--width', 
        metavar='INT',
        required=False,
        type=int,
        default=None,
        help='Output image width. Default: maximum width among all pages.')
    parser.add_argument(
        '--pdf-to-img-dpi', 
        metavar='INT',
        required=False,
        type=int,
        default=300,
        help='Image quality for the images converted from PDF, in DPI. Default: 300.')
    parser.add_argument(
        '--first-page', 
        metavar='INT',
        required=False,
        type=int,
        default=None,
        help='First page to process. Default: None.')
    parser.add_argument(
        '--last-page', 
        metavar='INT',
        required=False,
        type=int,
        default=None,
        help='Last page to process. Default: None.')
    parser.add_argument(
        '-s',
        '--include-separators',
        required=False,
        default=False,
        action='store_true',
        help='Add a separator between pages. Default: False.')
    parser.add_argument(
        '--separator-height',
        required=False,
        type=int,
        default=5,
        help='Separator height. Only used when --separator is used. Default: 5.')
    args = parser.parse_args()

    main(args)

