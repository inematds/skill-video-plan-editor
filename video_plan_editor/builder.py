# video_plan_editor/builder.py
from __future__ import annotations

from .detect import classify_input
from .models import (
    Aspect, EditPlan, Goal, Intent, Meta, Output, PresetName, Source,
)
from .presets import PRESETS, style_for

_PRESET_GOAL: dict[PresetName, Goal] = {
    PresetName.acao: Goal.highlights,
    PresetName.suave: Goal.explainer,
    PresetName.promo: Goal.promo,
    PresetName.vendas: Goal.sales,
    PresetName.viral: Goal.viral,
}


def scaffold_plan(
    raw_input: str,
    preset: PresetName,
    *,
    title: str | None = None,
    goal: Goal | None = None,
    aspect: Aspect | None = None,
    duration_target_seconds: float = 30.0,
) -> EditPlan:
    kind = classify_input(raw_input)
    style = style_for(preset)
    resolved_goal = goal or _PRESET_GOAL[preset]
    resolved_aspect = aspect or PRESETS[preset].default_aspect
    return EditPlan(
        meta=Meta(title=title or f"Plano {preset.value}"),
        source=Source(kind=kind, ref=raw_input),
        intent=Intent(
            goal=resolved_goal,
            best_action_rationale=(
                f"Input classificado como '{kind.value}'; preset '{preset.value}' "
                f"sugere objetivo '{resolved_goal.value}'. A timeline criativa é "
                f"preenchida na etapa de análise da skill."
            ),
        ),
        style=style,
        output=Output(aspect=resolved_aspect, duration_target_seconds=duration_target_seconds),
        timeline=[],
    )
