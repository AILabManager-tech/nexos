"""Workflows modulaires NEXOS composés de modules à contrats I/O."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from nexos.module_registry import ModuleRegistry


@dataclass(frozen=True)
class WorkflowStep:
    """Étape exécutable d'un workflow modulaire."""

    id: str
    module_id: str
    input_builder: Callable[[dict[str, Any], dict[str, Any]], dict[str, Any]]


@dataclass(frozen=True)
class WorkflowDefinition:
    """Définition d'un workflow NEXOS."""

    id: str
    description: str
    steps: tuple[WorkflowStep, ...]


def _root_payload(payload: dict[str, Any], _context: dict[str, Any]) -> dict[str, Any]:
    return payload


def _brief_from_synthesizer(_payload: dict[str, Any], context: dict[str, Any]) -> dict[str, Any]:
    synthesizer_output = context["steps"]["brief-synthesizer"]["output"]
    return {"brief": synthesizer_output["brief"]}


def _gaps_with_mu(_payload: dict[str, Any], context: dict[str, Any]) -> dict[str, Any]:
    """Input builder pour intake-question-prioritizer."""
    gaps = context["steps"]["legal-gap-checker"]["output"]["gaps"]
    scorer = context["steps"].get("brief-preview-scorer", {}).get("output", {})
    return {"gaps": gaps, "estimated_mu": scorer.get("estimated_mu", 0.0)}


def _brief_for_prerecommender(_payload: dict[str, Any], context: dict[str, Any]) -> dict[str, Any]:
    """Input builder pour pattern-prerecommender depuis le brief canonique."""
    synthesizer_output = context["steps"]["brief-synthesizer"]["output"]
    return {"brief": synthesizer_output["brief"], "top_k": 3}


WORKFLOWS: dict[str, WorkflowDefinition] = {
    "intake-preflight": WorkflowDefinition(
        id="intake-preflight",
        description="Transforme un intake réduit en brief canonique, puis vérifie les gaps Loi 25.",
        steps=(
            WorkflowStep(
                id="brief-synthesizer",
                module_id="brief-synthesizer",
                input_builder=_root_payload,
            ),
            WorkflowStep(
                id="legal-gap-checker",
                module_id="legal-gap-checker",
                input_builder=_brief_from_synthesizer,
            ),
        ),
    ),
    "saas-preview": WorkflowDefinition(
        id="saas-preview",
        description=(
            "Pipeline de preview SaaS — intake réduit → brief canonique → "
            "gaps Loi 25 → score SOIC estimé → questions priorisées → "
            "patterns design recommandés. Aucun appel pipeline complet."
        ),
        steps=(
            WorkflowStep(
                id="brief-synthesizer",
                module_id="brief-synthesizer",
                input_builder=_root_payload,
            ),
            WorkflowStep(
                id="legal-gap-checker",
                module_id="legal-gap-checker",
                input_builder=_brief_from_synthesizer,
            ),
            WorkflowStep(
                id="brief-preview-scorer",
                module_id="brief-preview-scorer",
                input_builder=_brief_from_synthesizer,
            ),
            WorkflowStep(
                id="intake-question-prioritizer",
                module_id="intake-question-prioritizer",
                input_builder=_gaps_with_mu,
            ),
            WorkflowStep(
                id="pattern-prerecommender",
                module_id="pattern-prerecommender",
                input_builder=_brief_for_prerecommender,
            ),
        ),
    ),
}


class WorkflowNotFoundError(ValueError):
    """Workflow inconnu."""


def list_workflows() -> list[WorkflowDefinition]:
    """Retourne les workflows connus."""
    return sorted(WORKFLOWS.values(), key=lambda workflow: workflow.id)


def get_workflow(workflow_id: str) -> WorkflowDefinition:
    """Retourne un workflow par ID."""
    workflow = WORKFLOWS.get(workflow_id)
    if workflow is None:
        raise WorkflowNotFoundError(f"Workflow inconnu: {workflow_id}")
    return workflow


def run_workflow(
    workflow_id: str,
    payload: dict[str, Any],
    *,
    registry: ModuleRegistry | None = None,
) -> dict[str, Any]:
    """Exécute un workflow modulaire et trace chaque étape."""
    workflow = get_workflow(workflow_id)
    module_registry = registry or ModuleRegistry()
    context: dict[str, Any] = {"steps": {}}
    step_results: list[dict[str, Any]] = []

    for step in workflow.steps:
        step_input = step.input_builder(payload, context)
        try:
            output = module_registry.run(step.module_id, step_input)
        except Exception as exc:
            step_results.append(
                {
                    "id": step.id,
                    "module_id": step.module_id,
                    "status": "failed",
                    "error": str(exc),
                }
            )
            return {
                "workflow_id": workflow.id,
                "status": "failed",
                "steps": step_results,
                "final_output": None,
            }

        result = {
            "id": step.id,
            "module_id": step.module_id,
            "status": "passed",
            "output": output,
        }
        step_results.append(result)
        context["steps"][step.id] = result

    return {
        "workflow_id": workflow.id,
        "status": "passed",
        "steps": step_results,
        "final_output": step_results[-1]["output"] if step_results else None,
    }
