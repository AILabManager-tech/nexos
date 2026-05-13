"""Tests Bloc C du registre modulaire NEXOS."""

from __future__ import annotations

import pytest

from nexos.module_registry import ModuleContractError, ModuleNotFoundError, ModuleRegistry


def test_discovers_hello_module() -> None:
    registry = ModuleRegistry()

    module = registry.get("hello")

    assert registry.total >= 1
    assert module.id == "hello"
    assert module.capabilities == ["contract-validation", "deterministic-transform"]
    assert module.inputs == ["name", "uppercase"]
    assert module.outputs == ["module_id", "message", "echo"]
    assert module.side_effects == []
    assert module.requires_network is False
    assert module.writes_files is False
    assert module.input_schema_path.exists()
    assert module.output_schema_path.exists()


def test_run_validates_input_and_output() -> None:
    registry = ModuleRegistry()

    output = registry.run("hello", {"name": "Nobert", "uppercase": True})

    assert output == {
        "module_id": "hello",
        "message": "BONJOUR NOBERT",
        "echo": {"name": "Nobert", "uppercase": True},
    }


def test_rejects_invalid_input() -> None:
    registry = ModuleRegistry()

    with pytest.raises(ModuleContractError, match="Input invalide"):
        registry.run("hello", {"name": ""})


def test_unknown_module_raises_clear_error() -> None:
    registry = ModuleRegistry()

    with pytest.raises(ModuleNotFoundError, match="Module inconnu"):
        registry.get("missing")
