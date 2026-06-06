# video_plan_editor/presets.py
from __future__ import annotations

from dataclasses import dataclass

from .models import (
    Aspect, CaptionStyle, Captions, Color, ColorLook, Music, Pacing,
    PresetName, Style, Transition,
)


@dataclass(frozen=True)
class PresetProfile:
    avg_cut_seconds: float
    energy: float
    transitions: tuple[Transition, ...]
    music_energy: float
    caption_style: CaptionStyle
    color_look: ColorLook
    default_aspect: Aspect


PRESETS: dict[PresetName, PresetProfile] = {
    PresetName.acao: PresetProfile(
        avg_cut_seconds=1.5, energy=0.9,
        transitions=(Transition.whip, Transition.zoom, Transition.cut),
        music_energy=0.9, caption_style=CaptionStyle.karaoke,
        color_look=ColorLook.punchy, default_aspect=Aspect.portrait,
    ),
    PresetName.suave: PresetProfile(
        avg_cut_seconds=5.0, energy=0.3,
        transitions=(Transition.crossfade,),
        music_energy=0.35, caption_style=CaptionStyle.minimal,
        color_look=ColorLook.cinematic, default_aspect=Aspect.landscape,
    ),
    PresetName.promo: PresetProfile(
        avg_cut_seconds=2.5, energy=0.7,
        transitions=(Transition.cut, Transition.zoom),
        music_energy=0.75, caption_style=CaptionStyle.block,
        color_look=ColorLook.punchy, default_aspect=Aspect.landscape,
    ),
    PresetName.vendas: PresetProfile(
        avg_cut_seconds=3.0, energy=0.6,
        transitions=(Transition.cut,),
        music_energy=0.6, caption_style=CaptionStyle.block,
        color_look=ColorLook.neutral, default_aspect=Aspect.landscape,
    ),
    PresetName.viral: PresetProfile(
        avg_cut_seconds=1.1, energy=0.95,
        transitions=(Transition.cut, Transition.zoom),
        music_energy=0.95, caption_style=CaptionStyle.karaoke,
        color_look=ColorLook.punchy, default_aspect=Aspect.portrait,
    ),
}


def style_for(preset: PresetName) -> Style:
    p = PRESETS[preset]
    return Style(
        preset=preset,
        pacing=Pacing(avg_cut_seconds=p.avg_cut_seconds, energy=p.energy),
        transitions=list(p.transitions),
        music=Music(energy=p.music_energy),
        captions=Captions(style=p.caption_style),
        color=Color(look=p.color_look),
    )
