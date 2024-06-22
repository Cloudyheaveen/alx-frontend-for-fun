s is a script to convert a Markdown file to HTML.

Usage:
    ./markdown2html.py [input_file] [output_file]

Arguments:
    input_file: the name of the Markdown file to be converted
    output_file: the name of the output HTML file

Example:
    ./markdown2html.py README.md README.html
"""

import sys
import argparse
import pathlib
import markdown


def convert_md_to_html(input_file, output_file):
    '''
    Converts markdown file to HTML file
    '''
    with open(input_file, 'r', encoding='utf-8') as md_file:
        markdown_text = md_file.read()

    html_text = markdown.markdown(markdown_text)

    with open(output_file, 'w', encoding='utf-8') as html_file:
        html_file.write(html_text)


def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Convert markdown to HTML')
    parser.add_argument('input_file', help='path to input markdown file')
    parser.add_argument('output_file', help='path to output HTML file')
    args = parser.parse_args()

    # Check if the input file exists
    input_path = pathlib.Path(args.input_file)
    if not input_path.is_file():
        print(f'Missing {input_path}', file=sys.stderr)
        sys.exit(1)

    # Convert the markdown file to HTML
    convert_md_to_html(args.input_file, args.output_file)


if __name__ == '__main__':
    main()

