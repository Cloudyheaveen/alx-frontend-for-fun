#!/usr/bin/env python3
"""
This is a script to convert a Markdown file to HTML.

Usage:
    ./markdown2html.py [input_file] [output_file]

Arguments:
    input_file: the name of the Markdown file to be converted
    output_file: the name of the output HTML file

Example:
    ./markdown2html.py README.md README.html
"""

import argparse
import pathlib
import re
import sys
import hashlib

def convert_md_to_html(input_file, output_file):
    """
    Converts markdown file to HTML file.
    """
    with open(input_file, 'r', encoding='utf-8') as f:
        md_content = f.readlines()

    html_content = []
    in_list = False
    in_ordered_list = False

    for line in md_content:
        line = line.rstrip()

        # Headings
        match = re.match(r'^(#{1,6})\s+(.*)', line)
        if match:
            h_level = len(match.group(1))
            h_content = match.group(2)
            html_content.append(f"<h{h_level}>{h_content}</h{h_level}>")
            continue

        # Unordered list
        if line.startswith('- '):
            if not in_list:
                in_list = True
                html_content.append("<ul>")
            html_content.append(f"<li>{line[2:]}</li>")
            continue
        elif in_list:
            in_list = False
            html_content.append("</ul>")

        # Ordered list
        if line.startswith('* '):
            if not in_ordered_list:
                in_ordered_list = True
                html_content.append("<ol>")
            html_content.append(f"<li>{line[2:]}</li>")
            continue
        elif in_ordered_list:
            in_ordered_list = False
            html_content.append("</ol>")

        # Paragraphs and other inline elements
        if line:
            line = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', line)
            line = re.sub(r'__(.*?)__', r'<em>\1</em>', line)
            line = re.sub(r'\[\[(.*?)\]\]', lambda m: hashlib.md5(m.group(1).encode()).hexdigest(), line)
            line = re.sub(r'\(\((.*?)\)\)', lambda m: m.group(1).replace('c', '').replace('C', ''), line)
            line = line.replace('\n', '<br/>\n')
            html_content.append(f"<p>{line}</p>")

    if in_list:
        html_content.append("</ul>")
    if in_ordered_list:
        html_content.append("</ol>")

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(html_content))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert markdown to HTML')
    parser.add_argument('input_file', help='path to input markdown file')
    parser.add_argument('output_file', help='path to output HTML file')
    args = parser.parse_args()

    input_path = pathlib.Path(args.input_file)
    if not input_path.is_file():
        print(f"Missing {input_path}", file=sys.stderr)
        sys.exit(1)

    convert_md_to_html(args.input_file, args.output_file)
