from __future__ import annotations

import pytest
from pydantic import ValidationError

from video_plan_editor.models import (
    EditPlan, Meta, Source, Intent, Style, Output, Pacing, Music,
    Captions, Color, TimelineItem, Caption, Content, Render,
    SourceKind, Goal, PresetName, Transition, CaptionStyle, ColorLook,
    Aspect, Role, EngineHint,
)


def _minimal_plan() -> EditPlan:
    return EditPlan(
        meta=Meta(title="Teste"),
        source=Source(kind=SourceKind.topic, ref="como fazer pão"),
        intent=Intent(goal=Goal.explainer, best_action_rationale="assunto curto"),
        style=Style(
            preset=PresetName.suave,
            pacing=Pacing(avg_cut_seconds=5.0, energy=0.3),
            transitions=[Transition.crossfade],
            music=Music(energy=0.3),
            captions=Captions(style=CaptionStyle.minimal),
            color=Color(look=ColorLook.cinematic),
        ),
        output=Output(aspect=Aspect.landscape, duration_target_seconds=30.0),
        timeline=[
            TimelineItem(
                id="s1", role=Role.hook,
                content=Content(headline="Pão em casa", narration="Vamos começar."),
                captions=[Caption(t_in=0.0, t_out=2.0, text="Pão em casa")],
            )
        ],
    )


def test_minimal_plan_builds_and_defaults():
    plan = _minimal_plan()
    assert plan.version == "1.0"
    assert plan.meta.language == "pt-BR"
    assert plan.render.engine_hint == EngineHint.auto
    assert plan.timeline[0].transition_out == Transition.cut


def test_roundtrip_json():
    plan = _minimal_plan()
    raw = plan.model_dump_json()
    again = EditPlan.model_validate_json(raw)
    assert again == plan


def test_energy_bounds_rejected():
    with pytest.raises(ValidationError):
        Pacing(avg_cut_seconds=1.0, energy=1.5)


def test_avg_cut_must_be_positive():
    with pytest.raises(ValidationError):
        Pacing(avg_cut_seconds=0.0, energy=0.5)


def test_aspect_enum_serializes_to_ratio_string():
    assert Aspect.portrait.value == "9:16"
