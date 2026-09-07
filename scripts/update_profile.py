#!/usr/bin/env python3
"""Refresh local SVG cards and verified project links. Python standard library only."""
import collections
import datetime as dt
import html
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
    user = api(f'users/{USERNAME}')
    repositories = []
    page = 1
    while True:
        batch = api(f'users/{USERNAME}/repos?type=owner&per_page=100&page={page}')
        repositories.extend(r for r in batch if not r['private'])
        if len(batch) < 100:
            break
        page += 1
    languages = collections.Counter()
    for repository in repositories:
        if not repository['fork']:
            languages.update(api(f"repos/{USERNAME}/{repository['name']}/languages"))
    commits = None
    if os.environ.get('GITHUB_TOKEN'):
        result = api('graphql', {'query': 'query($login:String!){user(login:$login){contributionsCollection{startedAt endedAt totalCommitContributions}}}', 'variables': {'login': USERNAME}})
        commits = result['data']['user']['contributionsCollection']['totalCommitContributions']
    return user, repositories, languages, commits


def text(x, y, value, size=15, color='#a1a1aa', extra=''):
    return f'<text x="{x}" y="{y}" fill="{color}" font-family="Arial,Helvetica,sans-serif" font-size="{size}" {extra}>{html.escape(str(value))}</text>'


def card(title, body, description):
    return '<svg xmlns="http://www.w3.org/2000/svg" width="440" height="265" viewBox="0 0 440 265" role="img"><title>' + html.escape(description) + '</title><rect x=".5" y=".5" width="439" height="264" rx="12" fill="#0b0d0e" stroke="#242729"/>' + text(24, 37, title, 20, '#f4f4f5') + body + '</svg>\n'


def render(user, repositories, languages, commits, date):
    metrics = [
        ('Commits · past year', f'{commits:,}' if commits is not None else 'Unavailable'),
        ('Followers', f"{user['followers']:,}"),
        ('Public repositories', f"{user['public_repos']:,}"),
        ('Stars · owned non-forks', f"{sum(r['stargazers_count'] for r in repositories if not r['fork']):,}"),
    ]
    body = ''
    for i, (label, value) in enumerate(metrics):
        y = 79 + i * 39
        body += text(24, y, label, 14) + text(414, y, value, 21, '#f4f4f5', 'text-anchor="end"')
    body += text(24, 242, f'GitHub API · {date} UTC', 12)
    stats = card('GitHub activity', body, '; '.join(f'{k}: {v}' for k, v in metrics) + f'. Updated {date} UTC.')
    total = sum(languages.values())
    body = ''
    top = languages.most_common(5)
    for i, (name, count) in enumerate(top):
        y = 71 + i * 32
        percentage = count / total * 100
        body += text(24, y, name, 14, '#d4d4d8') + text(414, y, f'{percentage:.1f}%', 13, extra='text-anchor="end"')
        body += f'<rect x="24" y="{y+8}" width="390" height="3" rx="1.5" fill="#272b2e"/><rect x="24" y="{y+8}" width="{390*count/total:.2f}" height="3" rx="1.5" fill="#a1a1aa"/>'
    if not top:
        body += text(24, 113, 'No public language data available.', 16)
    body += text(24, 242, f'Owned non-forks · code bytes · {date}', 12)
    lang = card('Top languages', body, 'Top languages by code bytes in public owned non-forks. ' + ', '.join(f'{n}: {c/total:.1%}' for n, c in top))
    return stats, lang


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
    user, repositories, languages, commits = collect()
    date = dt.datetime.now(dt.timezone.utc).date().isoformat()
    stats, lang = render(user, repositories, languages, commits, date)
    readme = replace_block((ROOT / 'README.md').read_text(), 'projects', project_block(repositories))
    if os.environ.get('SNAKE_PUBLISHED') == 'true':
        repository = os.environ['GITHUB_REPOSITORY']
        if repository.lower() != f'{USERNAME}/{USERNAME}'.lower():
            raise ValueError('Publish this package in the intended GitHub profile repository.')
        base = f'https://raw.githubusercontent.com/{repository}/output'
        readme = replace_block(readme, 'snake', f'<picture>\n  <source media="(prefers-color-scheme: dark)" srcset="{base}/github-snake-dark.svg">\n  <source media="(prefers-color-scheme: light)" srcset="{base}/github-snake.svg">\n  <img src="{base}/github-snake.svg" width="100%" alt="Animated contribution snake for {USERNAME}">\n</picture>')
    # No writes until all API calls and block validation have succeeded.
    (ROOT / 'assets/stats.svg').write_text(stats)
    (ROOT / 'assets/languages.svg').write_text(lang)
    (ROOT / 'README.md').write_text(readme)
    print(f'Updated verified public data for {USERNAME} on {date}.')


if __name__ == '__main__':
    main()
