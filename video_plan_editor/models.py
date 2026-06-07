# video_plan_editor/models.py
from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, Field


class SourceKind(str, Enum):
    video = "video"
    page = "page"
    topic = "topic"


class Goal(str, Enum):
    highlights = "highlights"
    supercut = "supercut"
    promo = "promo"
    explainer = "explainer"
    sales = "sales"
    viral = "viral"


class PresetName(str, Enum):
    acao = "acao"
    suave = "suave"
    promo = "promo"
    vendas = "vendas"
    viral = "viral"


class Transition(str, Enum):
    cut = "cut"
    crossfade = "crossfade"
    whip = "whip"
    zoom = "zoom"


class CaptionStyle(str, Enum):
    karaoke = "karaoke"
    block = "block"
    minimal = "minimal"


class ColorLook(str, Enum):
    neutral = "neutral"
    punchy = "punchy"
    cinematic = "cinematic"


class Aspect(str, Enum):
    landscape = "16:9"
    portrait = "9:16"
    square = "1:1"


class Role(str, Enum):
    hook = "hook"
    intro = "intro"
    point = "point"
    broll = "broll"
    cta = "cta"


class EngineHint(str, Enum):
    auto = "auto"
    ffmpeg = "ffmpeg"
    hyperframes = "hyperframes"


class Emotion(str, Enum):
    facts = "facts"
    feelings = "feelings"
    fun = "fun"


class RenderKind(str, Enum):
    motion = "motion"
    generated_still = "generated_still"
    generated_clip = "generated_clip"


class Media(BaseModel):
    path: str | None = None
    duration: float | None = None
    fps: float | None = None
    resolution: str | None = None


class Source(BaseModel):
    kind: SourceKind
    ref: str
    media: Media | None = None


class Intent(BaseModel):
    goal: Goal
    best_action_rationale: str
    angle: str | None = None
    pain: str | None = None
    emotion: Emotion | None = None
    framework: str | None = None
    hook_variants: list[str] = Field(default_factory=list)


class Pacing(BaseModel):
    avg_cut_seconds: float = Field(gt=0)
    energy: float = Field(ge=0, le=1)


class Music(BaseModel):
    energy: float = Field(ge=0, le=1)


class Captions(BaseModel):
    enabled: bool = True
    style: CaptionStyle = CaptionStyle.block
    position: str | None = None


class Color(BaseModel):
    look: ColorLook = ColorLook.neutral


class Style(BaseModel):
    preset: PresetName
    pacing: Pacing
    transitions: list[Transition]
    music: Music
    captions: Captions
    color: Color


class Output(BaseModel):
    aspect: Aspect
    duration_target_seconds: float = Field(gt=0)
    platform: str = "generic"


class Caption(BaseModel):
    t_in: float = Field(ge=0)
    t_out: float = Field(ge=0)
    text: str


class Content(BaseModel):
    headline: str | None = None
    narration: str | None = None
    broll_query: str | None = None


class TimelineItem(BaseModel):
    id: str
    role: Role
    source_in: float | None = None
    source_out: float | None = None
    content: Content | None = None
    captions: list[Caption] = Field(default_factory=list)
    overlays: list[dict] = Field(default_factory=list)
    transition_out: Transition = Transition.cut
    # camada de execução (knowledge base): camera/vocabulary, archetypes, motion/recipes
    camera: str | None = None
    archetype: str | None = None
    motion: list[str] = Field(default_factory=list)
    render_kind: RenderKind = RenderKind.motion
    gen_prompt: str | None = None


class Render(BaseModel):
    engine_hint: EngineHint = EngineHint.auto


class Meta(BaseModel):
    title: str
    language: str = "pt-BR"


class EditPlan(BaseModel):
    version: str = "1.0"
    meta: Meta
    source: Source
    intent: Intent
    style: Style
    output: Output
    timeline: list[TimelineItem] = Field(default_factory=list)
    render: Render = Field(default_factory=Render)
