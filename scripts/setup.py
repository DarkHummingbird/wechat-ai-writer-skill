"""Install pinned tools and initialize local state without replacing existing files."""
import shutil
import subprocess
import sys
import venv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    if sys.version_info < (3, 11):
        raise SystemExit('需要 Python 3.11 或更新版本。')
    if sys.platform == 'win32':
        raise SystemExit('当前入口支持 macOS/Linux；Windows 请使用 WSL。')
    environment = ROOT / '.venv'
    if not (environment / 'bin/python').exists():
        venv.EnvBuilder(with_pip=True).create(environment)
    python = environment / 'bin/python'
    subprocess.run([str(python), '-m', 'pip', 'install', '-r', str(ROOT / 'requirements.txt')], check=True)
    subprocess.run([str(python), '-m', 'pip', 'check'], check=True)
    for source in sorted((ROOT / 'defaults').rglob('*.yaml')):
        target = ROOT / '.wewrite' / source.relative_to(ROOT / 'defaults')
        target.parent.mkdir(parents=True, exist_ok=True)
        try:
            with target.open('x') as output:
                output.write(source.read_text())
            target.chmod(0o600)
        except FileExistsError:
            pass
    discovery = ROOT / '.agents/skills/wechat-ai-science'
    discovery.parent.mkdir(parents=True, exist_ok=True)
    if not discovery.exists() and not discovery.is_symlink():
        discovery.symlink_to('../../skills/wechat-ai-science', target_is_directory=True)
    if discovery.resolve() != (ROOT / 'skills/wechat-ai-science').resolve():
        raise SystemExit('发现同名 skill 指向其他位置，未覆盖；请检查 .agents/skills/wechat-ai-science。')
    print('安装完成。运行 bin/wewrite diagnose --json；在此目录中使用 $wechat-ai-science。')


if __name__ == '__main__':
    main()
