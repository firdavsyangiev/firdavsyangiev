#!/usr/bin/env python3
"""Refresh contribution snake references. Python standard library only."""
import os
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
# Single source of truth; repository owner is also checked by the workflow.
USERNAME = 'firdavsyangiev'


def replace_block(content, name, body):
    pattern = rf'<!-- {name}:start -->.*?<!-- {name}:end -->'
    updated, count = re.subn(pattern, lambda _: f'<!-- {name}:start -->\n{body}\n<!-- {name}:end -->', content, flags=re.S)
    if count != 1:
        raise ValueError(f'Expected exactly one {name} block; found {count}')
    return updated


def main():
    readme = (ROOT / 'README.md').read_text()
    if os.environ.get('SNAKE_PUBLISHED') == 'true':
        repository = os.environ['GITHUB_REPOSITORY']
        if repository.lower() != f'{USERNAME}/{USERNAME}'.lower():
            raise ValueError('Publish this package in the intended GitHub profile repository.')
        base = f'https://raw.githubusercontent.com/{repository}/output'
        readme = replace_block(readme, 'snake', f'<picture>\n  <source media="(prefers-color-scheme: dark)" srcset="{base}/github-contribution-grid-snake-dark.svg">\n  <source media="(prefers-color-scheme: light)" srcset="{base}/github-contribution-grid-snake.svg">\n  <img src="{base}/github-contribution-grid-snake.svg" width="900" alt="Animated contribution snake for {USERNAME}">\n</picture>')
    # No writes until block validation has succeeded.
    (ROOT / 'README.md').write_text(readme)
    print(f'Updated contribution snake references for {USERNAME}.')


if __name__ == '__main__':
    main()
