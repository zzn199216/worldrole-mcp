"""Build public marketplace metadata and a secret-free plugin ZIP from one manifest."""
import argparse
import hashlib
import json
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]


def encoded(data):
    return (json.dumps(data, ensure_ascii=False, indent=2) + '\n').encode('utf-8')


def generated_files():
    m = json.loads((ROOT / 'distribution/manifest.json').read_text(encoding='utf-8'))
    review = json.loads((ROOT / 'distribution/review-cases.json').read_text(encoding='utf-8'))
    identity = {k: m[k] for k in ('name', 'version', 'description', 'author', 'homepage', 'repository', 'license', 'keywords')}
    extension = {'interface': m['interface'], 'review': {'test_cases': review, 'commerce': False,
        'commerce_description': 'Free job discovery and career workflows. No checkout, payment tools, or billing credentials.'}}
    portable = {'$schema': 'https://agent-plugins.org/schemas/1.0.0/plugin.schema.json', **identity,
        'extensions': {'com.openai': extension}}
    legacy_mcp = {'mcpServers': {'worldrole': {'type': 'http', 'url': m['endpoint']}}}
    portable_mcp = {'$schema': 'https://agent-plugins.org/schemas/1.0.0/mcp.schema.json',
        'mcpServers': {'worldrole': {'type': 'streamable-http', 'url': m['endpoint']}}}
    codex = {**identity, 'skills': './skills/', 'mcpServers': './.mcp.json',
        'interface': m['interface'], 'extensions': {'com.openai': {'review': extension['review']}}}
    claude = {**identity, 'skills': './skills/', 'mcpServers': './.mcp.json'}
    cursor = {**identity, 'skills': './skills/', 'mcpServers': './.mcp.json', 'logo': './assets/icon.svg'}
    marketplace = {'name': 'worldrole', 'owner': m['author'],
        'metadata': {'description': m['description'], 'version': m['version']},
        'plugins': [{'name': m['name'], 'source': './', 'version': m['version'], 'description': m['description']}]}
    codex_marketplace = {'name': 'worldrole', 'interface': {'displayName': 'WorldRole'},
        'plugins': [{'name': m['name'], 'source': {'source': 'local', 'path': './'},
            'policy': {'installation': 'AVAILABLE', 'authentication': 'ON_INSTALL'},
            'category': 'Productivity'}]}
    extension_config = {'name': m['name'], 'version': m['version'],
        'mcpServers': {'worldrole': {'httpUrl': m['endpoint']}}}
    server = {'$schema': 'https://static.modelcontextprotocol.io/schemas/2025-12-11/server.schema.json',
        'name': 'io.github.zzn199216/worldrole', 'title': 'WorldRole', 'version': m['version'],
        'description': 'Free remote and overseas job search with sources and eligibility checks. Usage limits apply.',
        'websiteUrl': m['homepage'], 'repository': {'url': m['repository'], 'source': 'github'},
        'remotes': [{'type': 'streamable-http', 'url': m['endpoint']}],
        'icons': [{'src': m['repository'].replace('github.com', 'raw.githubusercontent.com') + '/main/assets/icon.svg',
            'mimeType': 'image/svg+xml', 'sizes': ['any']} ]}
    return {name: encoded(value) for name, value in {
        'plugin.json': portable, 'mcp.json': portable_mcp, '.mcp.json': legacy_mcp,
        '.codex-plugin/plugin.json': codex, '.claude-plugin/plugin.json': claude,
        '.cursor-plugin/plugin.json': cursor, '.claude-plugin/marketplace.json': marketplace,
        '.agents/plugins/marketplace.json': codex_marketplace,
        'gemini-extension.json': extension_config, 'qwen-extension.json': {**extension_config, 'skills': 'skills'},
        'server.json': server}.items()}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--zip', action='store_true')
    args = parser.parse_args()
    files = generated_files()
    stale = []
    for name, content in files.items():
        path = ROOT / name
        if args.check:
            if not path.exists() or path.read_bytes() != content:
                stale.append(name)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content)
    if stale:
        raise SystemExit('Regenerate marketplace metadata: ' + ', '.join(stale))
    if args.zip:
        # Explicit allowlist: no source backend, auth stores, local config, or logs.
        for name in ('LICENSE', 'README.md', 'README.en.md', 'INSTALL.md', 'INSTALL_FREE_SOURCES.md'):
            files[name] = (ROOT / name).read_bytes()
        for directory in ('skills', 'assets', 'docs'):
            for path in sorted((ROOT / directory).rglob('*')):
                if path.is_file() and path.suffix in ('.md', '.svg', '.png', '.yaml'):
                    files[path.relative_to(ROOT).as_posix()] = path.read_bytes()
        version = json.loads(files['plugin.json'])['version']
        dest = ROOT / 'dist' / f'worldrole-plugin-{version}.zip'
        dest.parent.mkdir(exist_ok=True)
        with zipfile.ZipFile(dest, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
            for name, content in sorted(files.items()):
                info = zipfile.ZipInfo(name, date_time=(2026, 10, 24, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                archive.writestr(info, content)
        digest = hashlib.sha256(dest.read_bytes()).hexdigest()
        dest.with_suffix('.zip.sha256').write_text(f'{digest}  {dest.name}\n', encoding='utf-8')
        print(json.dumps({'artifact': str(dest), 'sha256': digest, 'bytes': dest.stat().st_size}))
    else:
        print(f'{len(files)} marketplace files are consistent.')


if __name__ == '__main__':
    main()
