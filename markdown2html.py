#!/usr/bin/env python3

import sys
import os
import re
import hashlib

def markdown_to_html(markdown_file, output_file):
    if not os.path.isfile(markdown_file):
        print(f"Missing {markdown_file}", file=sys.stderr)
        exit(1)
    
    with open(markdown_file, 'r') as f:
        lines = f.readlines()

    html_lines = []
    in_list = False
    in_ordered_list = False

    for line in lines:
        line = line.rstrip()

        if line.startswith('#'):
            header_level = len(line.split(' ')[0])
            header_content = line[header_level + 1:]
            html_lines.append(f"<h{header_level}>{header_content}</h{header_level}>")
        elif line.startswith('- '):
            if not in_list:
                in_list = True
                html_lines.append("<ul>")
            html_lines.append(f"<li>{line[2:]}</li>")
        elif line.startswith('* '):
            if not in_ordered_list:
                in_ordered_list = True
                html_lines.append("<ol>")
            html_lines.append(f"<li>{line[2:]}</li>")
        else:
            if in_list:
                in_list = False
                html_lines.append("</ul>")
            if in_ordered_list:
                in_ordered_list = False
                html_lines.append("</ol>")
            if line:
                line = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', line)
                line = re.sub(r'__(.*?)__', r'<em>\1</em>', line)
                line = re.sub(r'\[\[(.*?)\]\]', lambda m: hashlib.md5(m.group(1).encode()).hexdigest(), line)
                line = re.sub(r'\(\((.*?)\)\)', lambda m: m.group(1).replace('c', '').replace('C', ''), line)
                line = line.replace('\n', '<br/>\n')
                html_lines.append(f"<p>{line}</p>")

    if in_list:
        html_lines.append("</ul>")
    if in_ordered_list:
        html_lines.append("</ol>")

    with open(output_file, 'w') as f:
        for html_line in html_lines:
            f.write(html_line + '\n')

    exit(0)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: ./markdown2html.py README.md README.html", file=sys.stderr)
        exit(1)
    
    markdown_file = sys.argv[1]
    output_file = sys.argv[2]

    markdown_to_html(markdown_file, output_file)
