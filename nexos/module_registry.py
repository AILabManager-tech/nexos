"""Registre modulaire NEXOS avec contrats I/O JSON Schema."""

from __future__ import annotations

import importlib
import json
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path
from types import ModuleType
from typing import Any, cast

from jsonschema import Draft202012Validator
from jsonschema.exceptions import ValidationError as JsonSchemaValidationError


class ModuleRegistryError(Exception):
    """Erreur de registre modulaire."""


class ModuleNotFoundError(ModuleRegistryError):
    """Module NEXOS introuvable."""


class ModuleContractError(ModuleRegistryError):
    """Contrat JSON Schema invalide ou non respecté."""


@dataclass(frozen=True)
class NexosModule:
    """Métadonnées et chemins d'un module NEXOS exécutable."""

    id: str
    name: str
    version: str
    description: str
    package: str
    entrypoint: str
    manifest_path: Path
    input_schema_path: Path
    output_schema_path: Path
    tags: list[str] = field(default_factory=list)
    capabilities: list[str] = field(default_factory=list)
    inputs: list[str] = field(default_factory=list)
    outputs: list[str] = field(default_factory=list)
    side_effects: list[str] = field(default_factory=list)
    requires_network: bool = False
    writes_files: bool = False
    status: str = "experimental"

    @property
    def base_dir(self) -> Path:
        return self.manifest_path.parent


def _load_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ModuleContractError(f"Fichier manquant: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ModuleContractError(f"JSON invalide dans {path}: {exc}") from exc

    if not isinstance(data, dict):
        raise ModuleContractError(f"JSON objet attendu dans {path}")
    return data


def _schema_errors(schema: dict[str, Any], payload: dict[str, Any]) -> list[str]:
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(payload), key=lambda error: list(error.path))
    return [_format_validation_error(error) for error in errors]


def _format_validation_error(error: JsonSchemaValidationError) -> str:
    location = ".".join(str(part) for part in error.path)
    prefix = f"{location}: " if location else ""
    return f"{prefix}{error.message}"


def _string_list(manifest: dict[str, Any], key: str, manifest_path: Path) -> list[str]:
    raw = manifest.get(key, [])
    if not isinstance(raw, list) or not all(isinstance(item, str) for item in raw):
        raise ModuleContractError(f"Champ {key} invalide dans {manifest_path}")
    return raw


def _bool_field(manifest: dict[str, Any], key: str, manifest_path: Path) -> bool:
    raw = manifest.get(key, False)
    if not isinstance(raw, bool):
        raise ModuleContractError(f"Champ {key} invalide dans {manifest_path}")
    return raw


class ModuleRegistry:
    """Découvre, valide et exécute les modules NEXOS déclarés."""

    def __init__(self, modules_package: str = "nexos.modules") -> None:
        self.modules_package = modules_package
        self.modules_dir = self._resolve_modules_dir(modules_package)
        self._modules = self._discover()

    @staticmethod
    def _resolve_modules_dir(modules_package: str) -> Path:
        package = importlib.import_module(modules_package)
        package_file = getattr(package, "__file__", None)
        if not package_file:
            raise ModuleRegistryError(f"Package modules invalide: {modules_package}")
        return Path(package_file).resolve().parent

    def _discover(self) -> dict[str, NexosModule]:
        discovered: dict[str, NexosModule] = {}
        if not self.modules_dir.is_dir():
            return discovered

        for manifest_path in sorted(self.modules_dir.glob("*/manifest.json")):
            module = self._load_manifest(manifest_path)
            if module.id in discovered:
                raise ModuleRegistryError(f"Module dupliqué: {module.id}")
            discovered[module.id] = module

        return discovered

    def _load_manifest(self, manifest_path: Path) -> NexosModule:
        manifest = _load_json(manifest_path)
        base_dir = manifest_path.parent
        required = ["id", "name", "version", "description", "entrypoint"]
        missing = [key for key in required if not manifest.get(key)]
        if missing:
            raise ModuleContractError(
                f"Manifest incomplet dans {manifest_path}: {', '.join(missing)}"
            )

        contracts = manifest.get("contracts")
        if not isinstance(contracts, dict):
            raise ModuleContractError(f"Contrats absents dans {manifest_path}")

        input_schema = contracts.get("input")
        output_schema = contracts.get("output")
        if not isinstance(input_schema, str) or not isinstance(output_schema, str):
            raise ModuleContractError(f"Contrats input/output invalides dans {manifest_path}")

        tags = _string_list(manifest, "tags", manifest_path)

        package = str(
            manifest.get("package") or f"{self.modules_package}.{manifest_path.parent.name}"
        )
        return NexosModule(
            id=str(manifest["id"]),
            name=str(manifest["name"]),
            version=str(manifest["version"]),
            description=str(manifest["description"]),
            package=package,
            entrypoint=str(manifest["entrypoint"]),
            manifest_path=manifest_path,
            input_schema_path=base_dir / input_schema,
            output_schema_path=base_dir / output_schema,
            tags=tags,
            capabilities=_string_list(manifest, "capabilities", manifest_path),
            inputs=_string_list(manifest, "inputs", manifest_path),
            outputs=_string_list(manifest, "outputs", manifest_path),
            side_effects=_string_list(manifest, "side_effects", manifest_path),
            requires_network=_bool_field(manifest, "requires_network", manifest_path),
            writes_files=_bool_field(manifest, "writes_files", manifest_path),
            status=str(manifest.get("status", "experimental")),
        )

    @property
    def total(self) -> int:
        return len(self._modules)

    def list_modules(self) -> list[NexosModule]:
        return sorted(self._modules.values(), key=lambda module: module.id)

    def get(self, module_id: str) -> NexosModule:
        module = self._modules.get(module_id)
        if module is None:
            raise ModuleNotFoundError(f"Module inconnu: {module_id}")
        return module

    def load_input_schema(self, module_id: str) -> dict[str, Any]:
        return _load_json(self.get(module_id).input_schema_path)

    def load_output_schema(self, module_id: str) -> dict[str, Any]:
        return _load_json(self.get(module_id).output_schema_path)

    def validate_input(self, module_id: str, payload: dict[str, Any]) -> list[str]:
        return _schema_errors(self.load_input_schema(module_id), payload)

    def validate_output(self, module_id: str, payload: dict[str, Any]) -> list[str]:
        return _schema_errors(self.load_output_schema(module_id), payload)

    def run(self, module_id: str, payload: dict[str, Any]) -> dict[str, Any]:
        input_errors = self.validate_input(module_id, payload)
        if input_errors:
            raise ModuleContractError(f"Input invalide pour {module_id}: {'; '.join(input_errors)}")

        module = self.get(module_id)
        runner = self._load_runner(module)
        output = runner(payload)
        if not isinstance(output, dict):
            raise ModuleContractError(f"Output non-objet pour {module_id}")

        output_errors = self.validate_output(module_id, output)
        if output_errors:
            raise ModuleContractError(
                f"Output invalide pour {module_id}: {'; '.join(output_errors)}"
            )
        return output

    def _load_runner(self, module: NexosModule) -> Callable[[dict[str, Any]], dict[str, Any]]:
        package: ModuleType = importlib.import_module(module.package)
        runner = getattr(package, module.entrypoint, None)
        if not callable(runner):
            raise ModuleRegistryError(
                f"Entrypoint introuvable: {module.package}.{module.entrypoint}"
            )
        return cast(Callable[[dict[str, Any]], dict[str, Any]], runner)


__all__ = [
    "ModuleContractError",
    "ModuleNotFoundError",
    "ModuleRegistry",
    "ModuleRegistryError",
    "NexosModule",
]
