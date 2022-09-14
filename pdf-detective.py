#!/usr/bin/env python3
'''
Read PDF titles and guess source URL.
2022-09 Jack Haden-Enneking
'''

import os
import argparse
import pikepdf
from glob import glob
from collections import namedtuple

parser = argparse.ArgumentParser()
parser.add_argument('-v', '--verbose', action='store_true')
parser.add_argument('-d', '--debug', action='store_true')
parser.add_argument('-o', '--output', default='./pdfs.html')
parser.add_argument(      '--open', action='store_true')
args = parser.parse_args()
if args.debug == True:
    args.verbose = True

url_base = 'https://hdl.handle.net/2027/'
Pdf = namedtuple('Pdf', ['file', 'title', 'url'])

pdfs = []
for file in glob('*.pdf'):
    with pikepdf.open(file) as pdf:
        title = str(pdf.docinfo.Title)  # e.g. 'njp-32101048157471-21-1626472259'
    title_parts = title.split('-')
    url = url_base + title_parts[0] + '.' + title_parts[1]  # e.g. 'https://hdl.handle.net/2027/njp.32101048157471'
    if args.verbose:
        print(f'{file}\t{title}\t{url}')
    pdfs.append(Pdf(file, title, url))

rows = '\n'.join(
    ('\n'.join([
        '    <tr>',
        f'      <td>{pdf.file}</td>',
        f'      <td>{pdf.title}</td>',
        f'      <td><a href="{pdf.url}">{pdf.url}</a></td>',
        '    </tr>',
    ]) for pdf in pdfs)
)

html = f'''<html>
<head>
  <title>PDFs</title>
</head>
<body>
<h1>PDFs in {os.getcwd()}</h1>
<table border="1" style="border-collapse: collapse;" cellpadding="5">
  <tbody>
    <tr><th>File</th><th>Title</th><th>URL</th></td>
{rows}
  </tbody>
</table>
<p style="margin-top: 5em;"><details><summary>Hi Jenny!</summary>I love you 💘</details></p>
</body>
</html>
'''
if args.debug:
    print('\n' + html)

if args.debug:
    print('Writing to', args.output)
with open(args.output, 'w') as f:
    f.write(html)

if args.open:
    os.system('open ' + args.output)

