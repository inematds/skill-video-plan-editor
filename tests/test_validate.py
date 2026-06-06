from __future__ import annotations

from video_plan_editor.models import (
    EditPlan, Meta, Source, Intent, Style, Output, Pacing, Music,
    Captions, Color, TimelineItem, Caption,
    SourceKind, Goal, PresetName, Transition, CaptionStyle, ColorLook,
    Aspect, Role,
)
from video_plan_editor.validate import validate_plan, is_valid, Issue


def _plan(timeline) -> EditPlan:
    return EditPlan(
        meta=Meta(title="T"),
        source=Source(kind=SourceKind.topic, ref="x"),
        intent=Intent(goal=Goal.explainer, best_action_rationale="r"),
        style=Style(
            preset=PresetName.suave,
            pacing=Pacing(avg_cut_seconds=5.0, energy=0.3),
            transitions=[Transition.crossfade],
            music=Music(energy=0.3),
            captions=Captions(style=CaptionStyle.minimal),
            color=Color(look=ColorLook.cinematic),
        ),
        output=Output(aspect=Aspect.landscape, duration_target_seconds=30.0),
        timeline=timeline,
    )


def test_valid_plan_has_no_errors():
    plan = _plan([TimelineItem(id="s1", role=Role.hook)])
    issues = validate_plan(plan)
    assert is_valid(plan)
    assert all(i.severity != "error" for i in issues)


def test_empty_timeline_is_error():
    plan = _plan([])
    codes = {i.code for i in validate_plan(plan)}
    assert "empty_timeline" in codes
    assert not is_valid(plan)


def test_bad_source_range_is_error():
    plan = _plan([TimelineItem(id="s1", role=Role.hook, source_in=10.0, source_out=5.0)])
    codes = {i.code for i in validate_plan(plan) if i.severity == "error"}
    assert "bad_range" in codes


def test_bad_caption_timing_is_error():
    item = TimelineItem(id="s1", role=Role.hook, captions=[Caption(t_in=3.0, t_out=2.0, text="x")])
    plan = _plan([item])
    codes = {i.code for i in validate_plan(plan) if i.severity == "error"}
    assert "bad_caption_timing" in codes


def test_no_hook_is_warning_not_error():
    plan = _plan([TimelineItem(id="s1", role=Role.point)])
    issues = validate_plan(plan)
    assert any(i.code == "no_hook" and i.severity == "warning" for i in issues)
    assert is_valid(plan)


def test_issue_is_frozen_dataclass():
    i = Issue(severity="error", code="x", message="y")
    assert (i.severity, i.code, i.message) == ("error", "x", "y")
