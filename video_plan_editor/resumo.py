# video_plan_editor/resumo.py
from __future__ import annotations

from .models import EditPlan


def render_resumo(plan: EditPlan) -> str:
    lines: list[str] = []
    lines.append(f"# {plan.meta.title}")
    lines.append("")
    lines.append(f"- **Fonte:** {plan.source.kind.value} — {plan.source.ref}")
    lines.append(f"- **Objetivo:** {plan.intent.goal.value}")
    lines.append(f"- **Por que essa ação:** {plan.intent.best_action_rationale}")
    lines.append(
        f"- **Preset:** {plan.style.preset.value} "
        f"(corte ~{plan.style.pacing.avg_cut_seconds}s, energia {plan.style.pacing.energy})"
    )
    lines.append(
        f"- **Saída:** {plan.output.aspect.value}, "
        f"alvo {plan.output.duration_target_seconds}s, {plan.output.platform}"
    )
    lines.append("")
    lines.append("## Timeline")
    for i, item in enumerate(plan.timeline, 1):
        head = f"{i}. **{item.role.value}** (`{item.id}`)"
        if item.source_in is not None and item.source_out is not None:
            head += f" — corte {item.source_in:.1f}s→{item.source_out:.1f}s"
        lines.append(head)
        if item.content and item.content.headline:
            lines.append(f"   - Headline: {item.content.headline}")
        if item.content and item.content.narration:
            lines.append(f"   - Narração: {item.content.narration}")
        for cap in item.captions:
            lines.append(f"   - Legenda [{cap.t_in:.1f}-{cap.t_out:.1f}]: {cap.text}")
    return "\n".join(lines) + "\n"
