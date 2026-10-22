"""Validate this instruction-only skill with Python's standard library."""
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = (
    'SKILL.md', 'README.md', 'LICENSE', 'CHANGELOG.md',
    'references/notebooklm-protocol.md', 'references/source-priority.md',
    'references/query-templates.md', 'examples/youtube-research.md',
    'examples/project-knowledge-base.md', 'examples/large-document-research.md',
    'tests/scenarios.md',
)


def validate(root):
    root = root.resolve()
    errors = []
    documents = {}
    for name in REQUIRED:
        path = root / name
        if not path.is_file() or not path.read_text().strip():
            errors.append(f'missing or empty: {name}')
    for path in root.rglob('*.md'):
        if '.git' not in path.parts:
            documents[path.resolve()] = path.read_text()
    skill = documents.get((root / 'SKILL.md').resolve(), '')
    match = re.match(r'\A---\n(.*?)\n---\n', skill, re.S)
    fields = {}
    if not match:
        errors.append('SKILL.md requires YAML frontmatter')
    else:
        # Intentionally restricted to portable scalar frontmatter used here.
        for line in match[1].splitlines():
            key, sep, value = line.partition(':')
            if not sep or not value.strip() or key in fields:
                errors.append(f'invalid/duplicate frontmatter field: {line}')
            fields[key] = value.strip()
        name = fields.get('name', '')
        if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', name) or len(name) > 64:
            errors.append('invalid skill name')
        if name != root.name:
            errors.append('name does not match skill folder')
        if not 1 <= len(fields.get('description', '')) <= 1024:
            errors.append('description must contain 1–1024 characters')
        if fields.get('license') != 'MIT':
            errors.append('expected MIT license metadata')
        if set(fields) - {'name', 'description', 'license'}:
            errors.append('validator expects only the documented scalar fields')
    graph = {path: set() for path in documents}
    local_count = 0
    for path, content in documents.items():
        if re.search(r'\b(?:TODO|FIXME|TBD)\b|\[INSERT\b', content):
            errors.append(f'unfinished placeholder: {path.relative_to(root)}')
        if sum(line.startswith('```') for line in content.splitlines()) % 2:
            errors.append(f'unclosed code fence: {path.relative_to(root)}')
        for target in re.findall(r'(?<!!)\[[^\]\n]+\]\(([^)\s]+)\)', content):
            url = urlsplit(target)
            if url.scheme or url.netloc:
                continue
            local_count += 1
            resolved = (path.parent / unquote(url.path)).resolve() if url.path else path
            if not resolved.is_relative_to(root.resolve()):
                errors.append(f'link escapes package: {target}')
                continue
            if not resolved.is_file():
                errors.append(f'broken link in {path.relative_to(root)}: {target}')
                continue
            if resolved in graph:
                graph[path].add(resolved)
            if url.fragment:
                headings = re.findall(r'^#{1,6}\s+(.+)$', resolved.read_text(), re.M)
                anchors = {re.sub(r'[^\w\- ]', '', h.lower()).replace(' ', '-') for h in headings}
                if unquote(url.fragment) not in anchors:
                    errors.append(f'broken heading fragment: {target}')
    seen, pending = set(), [(root / 'SKILL.md').resolve()]
    while pending:
        current = pending.pop()
        if current not in seen:
            seen.add(current)
            pending.extend(graph.get(current, set()) - seen)
    for folder in ('references', 'examples'):
        for path in (root / folder).glob('*.md'):
            if path.resolve() not in seen:
                errors.append(f'not reachable from SKILL.md: {path.relative_to(root)}')
    license_path = root / 'LICENSE'
    if not license_path.is_file() or 'Permission is hereby granted, free of charge' not in license_path.read_text():
        errors.append('MIT grant missing')
    return errors, local_count


if __name__ == '__main__':
    failures, links = validate(ROOT)
    for failure in failures:
        print(f'FAIL: {failure}')
    if failures:
        sys.exit(1)
    print(f'PASS: {len(REQUIRED)} required files; metadata, {links} local links, reachability, fences and placeholders')
