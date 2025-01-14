"""Update documentation in readme.

This tool extracts the documentation (docstrings) for all layout commands
(startings with "cmd_") from the layout class and inserts them as a table into
the readme file, in the marked area.

It should be run with every API change.
"""

import ast
import re


readme_path = 'README.md'
layout_path = 'flex_tree/layout.py'
marker = '<!--commands-{pos}-->\n'
start_marker = marker.format(pos='start')
end_marker = marker.format(pos='end')

def table(text):
    return '<table>\n%s</table>\n' % text

def row(text):
    return '  <tr>\n%s  </tr>\n' % text

def col(text):
    return '    <td>%s</td>\n' % text

def code(text):
    return '<code>%s</code>' % text

def function_name(name, args):
    return '%s(%s)' % (name, ', '.join(args))

def function_desc(text):
    return re.sub('`([^`]*)`', code('\\1'), text.replace('\n\n', '<br>\n'))

def main():
    with open(readme_path) as f:
        text = f.read()
    text_pre, rest = text.split(start_marker)
    _, text_post = rest.split(end_marker)

    with open(layout_path) as f:
        tree = ast.parse(f.read())

    rows = ''
    for node in ast.walk(tree):
        if not isinstance(node, ast.FunctionDef):
            continue
        if not node.name.startswith('cmd_'):
            continue
        name = node.name[4:]
        args = [a.arg for a in node.args.args[1:]]
        docstring = ast.get_docstring(node)
        rows += row(
            col(code(function_name(name, args))) +
            col(function_desc(docstring))
        )
    text_table = table(rows)

    with open(readme_path, 'w') as f:
        f.write(text_pre + start_marker + text_table + end_marker + text_post)
    print('Commands written to "%s".' % readme_path)

if __name__ == '__main__':
    main()
