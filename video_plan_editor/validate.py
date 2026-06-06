# video_plan_editor/validate.py
from __future__ import annotations

from dataclasses import dataclass

from .models import EditPlan

# Bounds inspirados nos guardrails do mcp-video (preflight antes do render).
MIN_CUT_SECONDS = 0.4
MAX_CUT_SECONDS = 30.0


@dataclass(frozen=True)
class Issue:
    severity: str  # "error" | "warning"
    code: str
    message: str


def validate_plan(plan: EditPlan) -> list[Issue]:
    issues: list[Issue] = []
    pacing = plan.style.pacing

    if pacing.avg_cut_seconds < MIN_CUT_SECONDS:
        issues.append(Issue("error", "cut_too_fast",
                            f"avg_cut_seconds {pacing.avg_cut_seconds} < {MIN_CUT_SECONDS}"))
    if pacing.avg_cut_seconds > MAX_CUT_SECONDS:
        issues.append(Issue("warning", "cut_too_slow",
                            f"avg_cut_seconds {pacing.avg_cut_seconds} > {MAX_CUT_SECONDS}"))

    if not plan.timeline:
        issues.append(Issue("error", "empty_timeline", "timeline tem 0 itens"))

    for item in plan.timeline:
        if item.source_in is not None and item.source_out is not None:
            if item.source_out <= item.source_in:
                issues.append(Issue("error", "bad_range",
                                    f"item {item.id}: source_out <= source_in"))
        for cap in item.captions:
            if cap.t_out <= cap.t_in:
                issues.append(Issue("error", "bad_caption_timing",
                                    f"item {item.id}: caption t_out <= t_in"))

    roles = {item.role.value for item in plan.timeline}
    if plan.timeline and "hook" not in roles:
        issues.append(Issue("warning", "no_hook", "plano sem cena de hook"))

    return issues


def is_valid(plan: EditPlan) -> bool:
    return not any(i.severity == "error" for i in validate_plan(plan))
