import sys
from pathlib import Path
from unittest.mock import patch

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from nexos.session_launcher import (
    HostCLI,
    _confirm_selection,
    build_launcher_command,
    build_mode_session_prompt,
    build_session_prompt,
    detect_host_cli,
    launch_session,
    select_mode_and_host,
)


def test_build_session_prompt_contains_hierarchy(tmp_path):
    prompt = build_session_prompt(tmp_path, "codex")
    assert "AGENTS.md" in prompt
    assert "ph0 → ph5" in prompt
    assert "CLI hôte détecté: codex" in prompt


def test_build_session_prompt_claude_uses_claude_md(tmp_path):
    prompt = build_session_prompt(tmp_path, "claude")
    assert "CLAUDE.md" in prompt
    assert "CLI hôte détecté: claude" in prompt


def test_build_mode_session_prompt_contains_mode(tmp_path):
    prompt = build_mode_session_prompt(tmp_path, "codex", "create")
    assert "Mode NEXOS sélectionné par l'utilisateur: create" in prompt
    assert "Confirmer que tu entres en mode `create`" in prompt


@pytest.mark.parametrize(
    ("host", "expected"),
    [
        (HostCLI("codex", "codex"), ["codex", "--cd"]),
        (HostCLI("claude", "claude"), ["claude", "--add-dir"]),
        (HostCLI("gemini", "gemini"), ["gemini", "--include-directories"]),
    ],
)
def test_build_launcher_command_prefixes(tmp_path, host, expected):
    cmd = build_launcher_command(host, tmp_path, "bootstrap")
    assert cmd[:2] == expected


def test_detect_host_cli_prefers_parent_process():
    with (
        patch("nexos.session_launcher._which", return_value=True),
        patch("nexos.session_launcher._read_parent_command", return_value="codex --cd /tmp"),
    ):
        host = detect_host_cli()
    assert host.name == "codex"


def test_detect_host_cli_respects_explicit_host():
    with patch("nexos.session_launcher._which", return_value=True):
        host = detect_host_cli("claude")
    assert host.name == "claude"


def test_select_mode_and_host_interactive():
    with (
        patch(
            "nexos.session_launcher._available_hosts",
            return_value=[HostCLI("codex", "codex"), HostCLI("claude", "claude")],
        ),
        patch("builtins.input", side_effect=["1", "2", "1"]),
    ):
        mode, host = select_mode_and_host()
    assert mode == "create"
    assert host.name == "claude"


def test_select_mode_and_host_uses_defaults_on_enter():
    with (
        patch(
            "nexos.session_launcher._available_hosts",
            return_value=[HostCLI("codex", "codex"), HostCLI("claude", "claude")],
        ),
        patch("builtins.input", side_effect=["", "", ""]),
    ):
        mode, host = select_mode_and_host()
    assert mode == "create"
    assert host.name == "codex"


def test_confirm_selection_defaults_to_launch():
    with patch("builtins.input", side_effect=[""]):
        action = _confirm_selection("create", HostCLI("codex", "codex"))
    assert action == "launch"


def test_confirm_selection_b_means_back_to_host():
    with patch("builtins.input", side_effect=["b"]):
        action = _confirm_selection("create", HostCLI("codex", "codex"))
    assert action == "host"


def test_select_mode_and_host_can_go_back_to_mode():
    with (
        patch(
            "nexos.session_launcher._available_hosts",
            return_value=[HostCLI("codex", "codex"), HostCLI("claude", "claude")],
        ),
        patch("builtins.input", side_effect=["1", "1", "3", "4", "2", "1"]),
    ):
        mode, host = select_mode_and_host()
    assert mode == "content"
    assert host.name == "claude"


def test_select_mode_and_host_b_goes_back_from_host_menu():
    with (
        patch(
            "nexos.session_launcher._available_hosts",
            return_value=[HostCLI("codex", "codex"), HostCLI("claude", "claude")],
        ),
        patch("builtins.input", side_effect=["1", "b", "4", "2", "1"]),
    ):
        mode, host = select_mode_and_host()
    assert mode == "content"
    assert host.name == "claude"


def test_select_mode_and_host_q_quits():
    with (
        patch(
            "nexos.session_launcher._available_hosts",
            return_value=[HostCLI("codex", "codex")],
        ),
        patch("builtins.input", side_effect=["q"]),
        pytest.raises(SystemExit) as exc,
    ):
        select_mode_and_host()
    assert exc.value.code == 0


def test_launch_session_print_prompt_only(tmp_path):
    with (
        patch(
            "nexos.session_launcher.select_mode_and_host",
            return_value=("create", HostCLI("codex", "codex")),
        ),
        patch("nexos.session_launcher.console") as mock_console,
    ):
        code = launch_session(tmp_path, print_prompt_only=True)
    assert code == 0
    mock_console.print.assert_called()


def test_launch_session_executes_host_command(tmp_path):
    with (
        patch(
            "nexos.session_launcher.select_mode_and_host",
            return_value=("analyze", HostCLI("gemini", "gemini")),
        ),
        patch("nexos.session_launcher.print_session_banner"),
        patch("nexos.session_launcher.subprocess.run") as mock_run,
    ):
        mock_run.return_value.returncode = 0
        code = launch_session(tmp_path)
    assert code == 0
    mock_run.assert_called_once()
    cmd = mock_run.call_args.args[0]
    assert cmd[0] == "gemini"
