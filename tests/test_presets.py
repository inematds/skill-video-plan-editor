from __future__ import annotations

from video_plan_editor.models import PresetName, Aspect, CaptionStyle, Transition
from video_plan_editor.presets import PRESETS, PresetProfile, style_for


def test_all_presets_present():
    assert set(PRESETS.keys()) == set(PresetName)


def test_viral_is_fast_and_portrait():
    p = PRESETS[PresetName.viral]
    assert p.avg_cut_seconds <= 1.5
    assert p.default_aspect == Aspect.portrait
    assert p.caption_style == CaptionStyle.karaoke


def test_suave_is_slow_and_landscape():
    p = PRESETS[PresetName.suave]
    assert p.avg_cut_seconds >= 4.0
    assert p.default_aspect == Aspect.landscape


def test_style_for_builds_valid_style():
    style = style_for(PresetName.acao)
    assert style.preset == PresetName.acao
    assert style.pacing.avg_cut_seconds == PRESETS[PresetName.acao].avg_cut_seconds
    assert Transition.cut in style.transitions or len(style.transitions) >= 1
    assert 0.0 <= style.music.energy <= 1.0
