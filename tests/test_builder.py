from __future__ import annotations

from video_plan_editor.builder import scaffold_plan
from video_plan_editor.models import PresetName, SourceKind, Goal, Aspect
from video_plan_editor.presets import PRESETS


def test_scaffold_detects_topic_and_applies_preset():
    plan = scaffold_plan("como fazer pão caseiro", PresetName.suave)
    assert plan.source.kind == SourceKind.topic
    assert plan.style.preset == PresetName.suave
    assert plan.output.aspect == PRESETS[PresetName.suave].default_aspect
    assert plan.intent.goal == Goal.explainer


def test_scaffold_video_link_is_video_kind():
    plan = scaffold_plan("https://youtu.be/abc", PresetName.viral)
    assert plan.source.kind == SourceKind.video
    assert plan.intent.goal == Goal.viral
    assert plan.output.aspect == Aspect.portrait


def test_scaffold_overrides_goal_aspect_title_duration():
    plan = scaffold_plan(
        "vender curso de IA", PresetName.vendas,
        title="VSL IA", goal=Goal.sales, aspect=Aspect.portrait,
        duration_target_seconds=90.0,
    )
    assert plan.meta.title == "VSL IA"
    assert plan.intent.goal == Goal.sales
    assert plan.output.aspect == Aspect.portrait
    assert plan.output.duration_target_seconds == 90.0


def test_scaffold_timeline_starts_empty():
    plan = scaffold_plan("assunto x", PresetName.acao)
    assert plan.timeline == []
