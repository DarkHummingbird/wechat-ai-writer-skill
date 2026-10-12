"""Project-scoped local subset of the upstream CLI; not an OS security sandbox."""
import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
ALLOWED = {'home', 'diagnose', 'run', 'sources', 'score', 'content-eval', 'learn-edits', 'check', '--version', '-V'}


def reject(message):
    print('Project WeWrite: ' + message, file=sys.stderr)
    raise SystemExit(2)


def main():
    args = sys.argv[1:]
    if not args or args[0] in ('--help', '-h'):
        print('项目本地入口：wewrite ' + ' | '.join(sorted(ALLOWED)))
        print('仅用于本地任务、来源记录与编辑辅助；写作入口为 $wechat-ai-science。')
        return
    if args[0] not in ALLOWED:
        reject('本项目未启用该命令。')
    if args[0] == 'learn-edits' and any(a.startswith('--from') for a in args):
        reject('改稿学习只使用本地文件。')
    if args[0] == 'run':
        if len(args) > 1 and args[1] == 'permission':
            reject('本项目不配置发布授权。')
        if len(args) > 1 and args[1] == 'start' and '--help' not in args:
            # Own parser prevents argparse abbreviations and duplicate options from bypassing policy.
            import argparse
            parser = argparse.ArgumentParser(allow_abbrev=False)
            parser.add_argument('--topic', required=True)
            parser.add_argument('--mode', choices=['draft'], default='draft')
            parser.add_argument('--visual-mode', choices=['none'], default='none')
            values = parser.parse_args(args[2:])
            if not values.topic.strip():
                reject('需要用户给定主题或标题。')
            args = ['run', 'start', '--topic', values.topic, '--mode', 'draft', '--visual-mode', 'none']
    # Do not inherit globally configured WeWrite/WeChat credentials or a foreign current run.
    for name in list(os.environ):
        if name.startswith(('WEWRITE_', 'WECHAT_')):
            os.environ.pop(name)
    os.environ['WEWRITE_HOME'] = str(ROOT / '.wewrite')
    os.environ['TZ'] = 'Asia/Shanghai'
    os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
    import time
    time.tzset()
    if args[0] == 'sources' and len(args) > 1 and args[1] == 'add' and '--help' not in args:
        import argparse
        import yaml
        import json
        from wewrite.sources import add_source
        from wewrite.runs import resolve_run_id, run_dir
        parser = argparse.ArgumentParser(allow_abbrev=False)
        for key in ['run-id', 'url', 'publisher', 'published-at']:
            parser.add_argument('--' + key)
        parser.add_argument('--title', required=True)
        parser.add_argument('--claim', required=True)
        parser.add_argument('--status', choices=['unverified', 'user_provided', 'verified'], default='unverified')
        parser.add_argument('--verification-note')
        values = vars(parser.parse_args(args[2:]))
        note = values.pop('verification_note')
        if values['status'] == 'verified' and not (note or '').strip():
            reject('verified 必须提供 --verification-note：核查材料路径/链接、核查方法、范围与限制；录入或抓取不算核实。')
        values = {k: v for k, v in values.items() if v is not None}
        values.setdefault('url', '')
        entry = add_source(**values)
        if values['status'] == 'verified':
            path = run_dir(resolve_run_id(values.get('run_id'))) / 'source-verifications.yaml'
            notes = yaml.safe_load(path.read_text()) if path.exists() else {}
            notes[entry['id']] = note
            path.write_text(yaml.safe_dump(notes, allow_unicode=True))
        print(json.dumps(entry, ensure_ascii=False, indent=2))
        return
    if args[0] == 'check' or args[:2] == ['run', 'finish']:
        import argparse
        import json
        from wewrite_checks import check
        parser = argparse.ArgumentParser(allow_abbrev=False)
        parser.add_argument('--run-id')
        values = parser.parse_args(args[1:] if args[0] == 'check' else args[2:])
        try:
            result = check(values.run_id)
        except (ValueError, OSError, KeyError) as exc:
            reject(str(exc))
        if args[0] == 'check':
            print(json.dumps(result, ensure_ascii=False, indent=2))
            return
    sys.argv = ['wewrite', *args]
    from wewrite.cli import main as upstream_main
    upstream_main()


if __name__ == '__main__':
    main()
