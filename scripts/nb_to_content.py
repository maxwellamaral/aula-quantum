#!/usr/bin/env python3
"""Conversor integral notebook -> _content.qmd (sem resumo: todo o conteudo entra)."""
import json, re, sys, pathlib, urllib.parse

def ensure_blank_before_lists(text):
    lines = text.split('\n')
    new_lines = []
    list_item_re = re.compile(r'^\s*([-*+]|\d+\.)\s')
    in_code_block = False
    for i, line in enumerate(lines):
        if line.strip().startswith('```'):
            in_code_block = not in_code_block
        if not in_code_block and list_item_re.match(line):
            if i > 0 and lines[i-1].strip() != '':
                prev = lines[i-1].strip()
                if not list_item_re.match(lines[i-1]) and not prev.startswith(('#', '>', '|', '```', ':::')):
                    new_lines.append('')
        new_lines.append(line)
    return '\n'.join(new_lines)

def cell_to_qmd(cell, idx):
    src = ''.join(cell.get('source', []))
    if not src.strip():
        return ''
    ct = cell['cell_type']
    if ct == 'markdown':
        # fix image links relative to notebooks/img/
        def imgfix(m):
            alt, path = m.group(1), m.group(2)
            if path.startswith(('http', '/')):
                return m.group(0)
            p = urllib.parse.unquote(path.split(':')[-1])
            base = pathlib.Path(p).name
            return f'![{alt}](/notebooks/img/{base})'
        src = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', imgfix, src)
        src = ensure_blank_before_lists(src)
        return src + '\n\n'
    if ct == 'code':
        outputs = []
        for out in cell.get('outputs', []):
            data = out.get('data', {})
            if 'text/plain' in out.get('data', {}) and out.get('output_type') == 'execute_result':
                continue  # echo do resultado já visível; mantém stream e erros
            if out.get('output_type') in ('stream',):
                txt = ''.join(out.get('text', []))
                if txt.strip():
                    outputs.append(f"```\n{txt}\n```\n")
            elif out.get('output_type') == 'error':
                outputs.append(f"> **Erro (saída original):** `{out.get('ename','')}`\n")
        code = f"```{{python}}\n{src}\n```\n"
        return code + ('\n' + '\n'.join(outputs) if outputs else '') + '\n'
    if ct == 'raw':
        return src + '\n\n'
    return ''

def convert(nb_path, title, subtitle, order_note=''):
    nb = json.load(open(nb_path, encoding='utf-8'))
    parts = [f"# {title}\n\n"]
    if order_note:
        parts.append(order_note + '\n\n')
    for i, c in enumerate(nb['cells']):
        parts.append(cell_to_qmd(c, i))
    body = ''.join(parts)
    # collapse >2 blank lines
    body = re.sub(r'\n{3,}', '\n\n', body)
    return body

if __name__ == '__main__':
    nb_path, out_path, title = sys.argv[1], sys.argv[2], sys.argv[3]
    note = sys.argv[4] if len(sys.argv) > 4 else ''
    pathlib.Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    pathlib.Path(out_path).write_text(convert(nb_path, title, '', note), encoding='utf-8')
    n_cells = len(json.load(open(nb_path))['cells'])
    print(f'{out_path}: {len(pathlib.Path(out_path).read_text())} chars from {n_cells} cells')
