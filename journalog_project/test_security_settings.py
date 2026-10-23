"""本番設定（DEBUG=False）のセキュリティ設定が、check --deploy で警告なしになることを確認する。

テストの設定（settings_test.py）では、HTTPS関連の設定を無効にしているため、
本番の設定そのもの（journalog_project.settings）を別プロセスで読み込んで確認する。
"""

import os
import secrets
import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


def run_check_deploy(debug: str) -> subprocess.CompletedProcess:
    """指定した DEBUG の値で `manage.py check --deploy` を別プロセスで実行する。"""
    env = {
        key: value
        for key, value in os.environ.items()
        if key not in ("DATABASE_URL", "DJANGO_SETTINGS_MODULE", "SECRET_KEY", "DEBUG")
    }
    env["DJANGO_SETTINGS_MODULE"] = "journalog_project.settings"
    env["DEBUG"] = debug
    # W009（SECRET_KEYの強度）の確認用に、毎回ランダムな十分に長い値を使う（実際の値ではない）。
    env["SECRET_KEY"] = secrets.token_urlsafe(50)
    return subprocess.run(
        [sys.executable, "manage.py", "check", "--deploy"],
        cwd=BASE_DIR,
        env=env,
        capture_output=True,
        text=True,
        timeout=60,
    )


def test_production_settings_have_no_deploy_warnings():
    """DEBUG=False（本番）では、check --deploy の警告が出ない。"""
    result = run_check_deploy(debug="False")
    output = result.stdout + result.stderr  # 警告は標準エラー出力に出る

    assert result.returncode == 0, output
    assert "System check identified no issues" in output, output


def test_debug_true_still_warns_so_production_settings_are_not_applied_locally():
    """DEBUG=True（ローカル開発）では本番用の設定が効かず、これまでどおり警告が出る。

    ローカルがHTTPS必須になって、http://localhost で開発できなくなることを防ぐ確認。
    """
    result = run_check_deploy(debug="True")
    output = result.stdout + result.stderr  # 警告は標準エラー出力に出る

    assert "security.W008" in output, output
    assert "security.W018" in output, output
