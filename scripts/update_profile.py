#!/usr/bin/env python3
"""Refresh verified project links and contribution snake references. Python standard library only."""
import json
import os
from pathlib import Path
import re
import time
import urllib.error
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
# Single source of truth; repository owner is also checked by the workflow.
USERNAME = 'firdavsyangiev'
PROJECTS = [
    ('space-rental-platform', 'Discover and rent unique spaces for any occasion.', ['Next.js', 'TypeScript', 'MongoDB']),
    ('real-estate-platform', 'A modern real estate platform with advanced search and filters.', ['React', 'Node.js', 'GraphQL']),
    ('portfolio', 'My personal developer portfolio.', ['Next.js', 'TypeScript', 'Tailwind CSS']),
]


def api(path, payload=None):
    headers = {'Accept': 'application/vnd.github+json', 'User-Agent': 'ray-profile', 'X-GitHub-Api-Version': '2022-11-28'}
    token = os.environ.get('GITHUB_TOKEN')
    if token:
        headers['Authorization'] = f'Bearer {token}'
    data = json.dumps(payload).encode() if payload is not None else None
    if data:
        headers['Content-Type'] = 'application/json'
    for attempt in range(3):
        try:
            with urllib.request.urlopen(urllib.request.Request('https://api.github.com/' + path, data=data, headers=headers), timeout=45) as response:
                result = json.load(response)
            if isinstance(result, dict) and result.get('errors'):
                raise RuntimeError('GitHub GraphQL returned errors; preserving previous assets.')
            return result
        except urllib.error.HTTPError as error:
            if error.code < 500 or attempt == 2:
                raise
        except urllib.error.URLError:
            if attempt == 2:
                raise
        time.sleep(2 ** attempt)
    raise RuntimeError('GitHub API request failed')


def collect():
    repositories = []
    page = 1
    while True:
        batch = api(f'users/{USERNAME}/repos?type=owner&per_page=100&page={page}')
        repositories.extend(r for r in batch if not r['private'])
        if len(batch) < 100:
            break
        page += 1
    return repositories


def replace_block(content, name, body):
    pattern = rf'<!-- {name}:start -->.*?<!-- {name}:end -->'
    updated, count = re.subn(pattern, lambda _: f'<!-- {name}:start -->\n{body}\n<!-- {name}:end -->', content, flags=re.S)
    if count != 1:
        raise ValueError(f'Expected exactly one {name} block; found {count}')
    return updated


def project_block(repositories):
    names = {r['name'].lower(): r['html_url'] for r in repositories}
    blocks = []
    for name, description, stack in PROJECTS:
        url = names.get(name.lower())
        heading = f'[{name}]({url})' if url else name
        block = f'#### {heading}\n\n{description}\n\n' + ' · '.join(f'`{tech}`' for tech in stack)
        if not url:
            block += '\n\n<sub>Repository link pending — no public repository with this name found.</sub>'
        blocks.append(block)
    return '\n\n'.join(blocks)


def main():
    repositories = collect()
    readme = replace_block((ROOT / 'README.md').read_text(), 'projects', project_block(repositories))
    if os.environ.get('SNAKE_PUBLISHED') == 'true':
        repository = os.environ['GITHUB_REPOSITORY']
        if repository.lower() != f'{USERNAME}/{USERNAME}'.lower():
            raise ValueError('Publish this package in the intended GitHub profile repository.')
        base = f'https://raw.githubusercontent.com/{repository}/output'
        readme = replace_block(readme, 'snake', f'<picture>\n  <source media="(prefers-color-scheme: dark)" srcset="{base}/github-snake-dark.svg">\n  <source media="(prefers-color-scheme: light)" srcset="{base}/github-snake.svg">\n  <img src="{base}/github-snake.svg" width="100%" alt="Animated contribution snake for {USERNAME}">\n</picture>')
    # No writes until all API calls and block validation have succeeded.
    (ROOT / 'README.md').write_text(readme)
    print(f'Updated verified project links for {USERNAME}.')


if __name__ == '__main__':
    main()
