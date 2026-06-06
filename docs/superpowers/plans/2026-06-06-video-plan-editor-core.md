# video-plan-editor — Núcleo do gerador de plano (Fase 1) — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Construir o núcleo Python que transforma um input (assunto/link) num plano de edição de vídeo tipado (`EditPlan`), valida-o com guardrails, e o expõe via CLI (`vpe scaffold|validate|resumo`).

**Architecture:** Pacote Python `video_plan_editor` com módulos de responsabilidade única: `models` (schema pydantic), `presets` (perfis de estilo), `detect` (classifica input), `validate` (guardrails sobre o plano), `resumo` (plano→markdown), `builder` (monta o esqueleto do plano), `cli` (argparse). O plano é o dado central; o preenchimento criativo da timeline é feito pela orquestração da skill (`SKILL.md`), não por este código. Ingest de vídeo real e render são planos posteriores.

**Tech Stack:** Python ≥3.11, pydantic 2, pytest, hatchling. Console script `vpe`.

---

## Escopo / decomposição

- **Fase 1 (este plano):** núcleo gerador de plano — Python puro, totalmente testável.
- **Fase 2 (plano futuro):** ingest de vídeo real — yt-dlp, ffprobe, transcrição, detecção de silêncio/cena (Auto-Editor), auto-highlights.
- **Fase 3 (plano futuro):** adaptadores de render — FFmpeg, HyperFrames; export EDL/OTIO (v3).

## File Structure

| Arquivo | Responsabilidade |
|---|---|
| `pyproject.toml` | metadata, deps (pydantic), console script `vpe`, config pytest |
| `video_plan_editor/__init__.py` | marca o pacote, reexporta `EditPlan` |
| `video_plan_editor/models.py` | enums + modelos pydantic (`EditPlan` e aninhados) |
| `video_plan_editor/presets.py` | `PresetProfile`, registry `PRESETS`, `style_for()` |
| `video_plan_editor/detect.py` | `classify_input()` → `SourceKind` |
| `video_plan_editor/validate.py` | `Issue`, `validate_plan()`, `is_valid()` |
| `video_plan_editor/resumo.py` | `render_resumo()` plano→markdown |
| `video_plan_editor/builder.py` | `scaffold_plan()` monta o esqueleto do plano |
| `video_plan_editor/cli.py` | `main()` — subcomandos scaffold/validate/resumo |
| `tests/test_*.py` | um arquivo de teste por módulo |
| `SKILL.md` | orquestração (como a skill usa o pacote) |

---

### Task 0: Scaffold do projeto Python

**Files:**
- Create: `pyproject.toml`
- Create: `video_plan_editor/__init__.py`
- Create: `tests/__init__.py`

- [ ] **Step 1: Criar `pyproject.toml`**

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "video-plan-editor"
version = "0.1.0"
description = "Gera planos profissionais de edição de vídeo a partir de assunto/link"
requires-python = ">=3.11"
dependencies = ["pydantic>=2.6"]

[project.optional-dependencies]
dev = ["pytest>=8.0"]

[project.scripts]
vpe = "video_plan_editor.cli:main"

[tool.hatch.build.targets.wheel]
packages = ["video_plan_editor"]

[tool.pytest.ini_options]
testpaths = ["tests"]
```

- [ ] **Step 2: Criar `video_plan_editor/__init__.py`**

```python
from __future__ import annotations

from .models import EditPlan

__all__ = ["EditPlan"]
```

(Este import só funciona após a Task 1. Se executando esta task isolada, deixe o arquivo vazio e ajuste após a Task 1. Para evitar ordem quebrada, crie o `__init__.py` vazio agora e adicione o reexport ao final da Task 1.)

Conteúdo inicial:

```python
```

- [ ] **Step 3: Criar `tests/__init__.py` vazio**

```python
```

- [ ] **Step 4: Instalar em modo dev e confirmar pytest disponível**

Run: `python -m venv .venv && . .venv/bin/activate && pip install -e ".[dev]" && pytest --version`
Expected: imprime a versão do pytest (ex.: `pytest 8.x`).

- [ ] **Step 5: Commit**

```bash
git add pyproject.toml video_plan_editor/__init__.py tests/__init__.py
git commit -m "chore: scaffold projeto video-plan-editor (pyproject, pacote, pytest)"
```

---

### Task 1: Schema do plano (`models.py`)

**Files:**
- Create: `video_plan_editor/models.py`
- Test: `tests/test_models.py`
- Modify: `video_plan_editor/__init__.py` (reexport ao final)

- [ ] **Step 1: Escrever o teste que falha**

```python
# tests/test_models.py
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
```

- [ ] **Step 2: Rodar e confirmar falha**

Run: `pytest tests/test_models.py -v`
Expected: FAIL com `ModuleNotFoundError: No module named 'video_plan_editor.models'`.

- [ ] **Step 3: Implementar `models.py`**

```python
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
```

- [ ] **Step 4: Adicionar reexport no `__init__.py`**

```python
# video_plan_editor/__init__.py
from __future__ import annotations

from .models import EditPlan

__all__ = ["EditPlan"]
```

- [ ] **Step 5: Rodar e confirmar que passa**

Run: `pytest tests/test_models.py -v`
Expected: PASS (5 testes).

- [ ] **Step 6: Commit**

```bash
git add video_plan_editor/models.py video_plan_editor/__init__.py tests/test_models.py
git commit -m "feat: schema EditPlan (pydantic) com enums e bounds"
```

---

### Task 2: Presets de estilo (`presets.py`)

**Files:**
- Create: `video_plan_editor/presets.py`
- Test: `tests/test_presets.py`

- [ ] **Step 1: Escrever o teste que falha**

```python
# tests/test_presets.py
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
```

- [ ] **Step 2: Rodar e confirmar falha**

Run: `pytest tests/test_presets.py -v`
Expected: FAIL com `ModuleNotFoundError: No module named 'video_plan_editor.presets'`.

- [ ] **Step 3: Implementar `presets.py`**

```python
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
```

- [ ] **Step 4: Rodar e confirmar que passa**

Run: `pytest tests/test_presets.py -v`
Expected: PASS (4 testes).

- [ ] **Step 5: Commit**

```bash
git add video_plan_editor/presets.py tests/test_presets.py
git commit -m "feat: presets de estilo (acao/suave/promo/vendas/viral) + style_for"
```

---

### Task 3: Detecção de input (`detect.py`)

**Files:**
- Create: `video_plan_editor/detect.py`
- Test: `tests/test_detect.py`

- [ ] **Step 1: Escrever o teste que falha**

```python
# tests/test_detect.py
from __future__ import annotations

import pytest

from video_plan_editor.detect import classify_input
from video_plan_editor.models import SourceKind


@pytest.mark.parametrize("text,expected", [
    ("como fazer pão caseiro", SourceKind.topic),
    ("Os 5 erros mais comuns em vendas", SourceKind.topic),
    ("https://youtube.com/watch?v=abc123", SourceKind.video),
    ("https://youtu.be/abc123", SourceKind.video),
    ("https://www.tiktok.com/@x/video/123", SourceKind.video),
    ("https://cdn.exemplo.com/clipe.mp4", SourceKind.video),
    ("https://exemplo.com/post/artigo-sobre-vendas", SourceKind.page),
    ("https://blog.exemplo.com/", SourceKind.page),
])
def test_classify_input(text, expected):
    assert classify_input(text) == expected


def test_whitespace_is_stripped():
    assert classify_input("   https://youtu.be/abc   ") == SourceKind.video
```

- [ ] **Step 2: Rodar e confirmar falha**

Run: `pytest tests/test_detect.py -v`
Expected: FAIL com `ModuleNotFoundError: No module named 'video_plan_editor.detect'`.

- [ ] **Step 3: Implementar `detect.py`**

```python
# video_plan_editor/detect.py
from __future__ import annotations

import re
from urllib.parse import urlparse

from .models import SourceKind

VIDEO_EXTENSIONS = (".mp4", ".mov", ".mkv", ".webm", ".avi", ".m4v")
VIDEO_DOMAINS = ("youtube.com", "youtu.be", "vimeo.com", "tiktok.com", "instagram.com")

_URL_RE = re.compile(r"^https?://", re.IGNORECASE)


def classify_input(text: str) -> SourceKind:
    s = text.strip()
    if not _URL_RE.match(s):
        return SourceKind.topic
    parsed = urlparse(s)
    host = (parsed.netloc or "").lower()
    path = (parsed.path or "").lower()
    if path.endswith(VIDEO_EXTENSIONS):
        return SourceKind.video
    if any(host == d or host.endswith("." + d) for d in VIDEO_DOMAINS):
        return SourceKind.video
    return SourceKind.page
```

- [ ] **Step 4: Rodar e confirmar que passa**

Run: `pytest tests/test_detect.py -v`
Expected: PASS (9 testes).

- [ ] **Step 5: Commit**

```bash
git add video_plan_editor/detect.py tests/test_detect.py
git commit -m "feat: classify_input (topic/page/video) por URL e domínio"
```

---

### Task 4: Validação / guardrails (`validate.py`)

**Files:**
- Create: `video_plan_editor/validate.py`
- Test: `tests/test_validate.py`

- [ ] **Step 1: Escrever o teste que falha**

```python
# tests/test_validate.py
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
```

- [ ] **Step 2: Rodar e confirmar falha**

Run: `pytest tests/test_validate.py -v`
Expected: FAIL com `ModuleNotFoundError: No module named 'video_plan_editor.validate'`.

- [ ] **Step 3: Implementar `validate.py`**

```python
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
```

- [ ] **Step 4: Rodar e confirmar que passa**

Run: `pytest tests/test_validate.py -v`
Expected: PASS (6 testes).

- [ ] **Step 5: Commit**

```bash
git add video_plan_editor/validate.py tests/test_validate.py
git commit -m "feat: validate_plan + guardrails (cut bounds, ranges, captions, hook)"
```

---

### Task 5: Resumo legível (`resumo.py`)

**Files:**
- Create: `video_plan_editor/resumo.py`
- Test: `tests/test_resumo.py`

- [ ] **Step 1: Escrever o teste que falha**

```python
# tests/test_resumo.py
from __future__ import annotations

from video_plan_editor.models import (
    EditPlan, Meta, Source, Intent, Style, Output, Pacing, Music,
    Captions, Color, TimelineItem, Caption, Content,
    SourceKind, Goal, PresetName, Transition, CaptionStyle, ColorLook,
    Aspect, Role,
)
from video_plan_editor.resumo import render_resumo


def _plan() -> EditPlan:
    return EditPlan(
        meta=Meta(title="Plano Viral Pão"),
        source=Source(kind=SourceKind.topic, ref="como fazer pão"),
        intent=Intent(goal=Goal.viral, best_action_rationale="assunto curto e visual"),
        style=Style(
            preset=PresetName.viral,
            pacing=Pacing(avg_cut_seconds=1.1, energy=0.95),
            transitions=[Transition.cut, Transition.zoom],
            music=Music(energy=0.95),
            captions=Captions(style=CaptionStyle.karaoke),
            color=Color(look=ColorLook.punchy),
        ),
        output=Output(aspect=Aspect.portrait, duration_target_seconds=20.0, platform="tiktok"),
        timeline=[
            TimelineItem(
                id="s1", role=Role.hook,
                content=Content(headline="Pão em 20s", narration="Olha isso."),
                captions=[Caption(t_in=0.0, t_out=1.5, text="Pão em 20s")],
            ),
            TimelineItem(id="s2", role=Role.cta, source_in=10.0, source_out=12.0),
        ],
    )


def test_resumo_contains_title_and_preset():
    md = render_resumo(_plan())
    assert "# Plano Viral Pão" in md
    assert "viral" in md
    assert "9:16" in md


def test_resumo_lists_timeline_roles_and_captions():
    md = render_resumo(_plan())
    assert "hook" in md
    assert "cta" in md
    assert "Pão em 20s" in md
    assert "10.0s→12.0s" in md


def test_resumo_ends_with_newline():
    md = render_resumo(_plan())
    assert md.endswith("\n")
```

- [ ] **Step 2: Rodar e confirmar falha**

Run: `pytest tests/test_resumo.py -v`
Expected: FAIL com `ModuleNotFoundError: No module named 'video_plan_editor.resumo'`.

- [ ] **Step 3: Implementar `resumo.py`**

```python
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
```

- [ ] **Step 4: Rodar e confirmar que passa**

Run: `pytest tests/test_resumo.py -v`
Expected: PASS (3 testes).

- [ ] **Step 5: Commit**

```bash
git add video_plan_editor/resumo.py tests/test_resumo.py
git commit -m "feat: render_resumo (plano -> markdown legível)"
```

---

### Task 6: Builder do esqueleto (`builder.py`)

**Files:**
- Create: `video_plan_editor/builder.py`
- Test: `tests/test_builder.py`

- [ ] **Step 1: Escrever o teste que falha**

```python
# tests/test_builder.py
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
```

- [ ] **Step 2: Rodar e confirmar falha**

Run: `pytest tests/test_builder.py -v`
Expected: FAIL com `ModuleNotFoundError: No module named 'video_plan_editor.builder'`.

- [ ] **Step 3: Implementar `builder.py`**

```python
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
```

- [ ] **Step 4: Rodar e confirmar que passa**

Run: `pytest tests/test_builder.py -v`
Expected: PASS (4 testes).

- [ ] **Step 5: Commit**

```bash
git add video_plan_editor/builder.py tests/test_builder.py
git commit -m "feat: scaffold_plan (detect + preset -> esqueleto de EditPlan)"
```

---

### Task 7: CLI (`cli.py`)

**Files:**
- Create: `video_plan_editor/cli.py`
- Test: `tests/test_cli.py`

- [ ] **Step 1: Escrever o teste que falha**

```python
# tests/test_cli.py
from __future__ import annotations

import json

from video_plan_editor.cli import main
from video_plan_editor.builder import scaffold_plan
from video_plan_editor.models import PresetName, EditPlan, TimelineItem, Role


def test_scaffold_prints_valid_json(capsys):
    rc = main(["scaffold", "como fazer pão", "--preset", "suave"])
    out = capsys.readouterr().out
    assert rc == 0
    data = json.loads(out)
    assert data["style"]["preset"] == "suave"
    assert data["source"]["kind"] == "topic"


def test_validate_returns_1_on_error(tmp_path, capsys):
    plan = scaffold_plan("assunto x", PresetName.acao)  # timeline vazia -> erro
    path = tmp_path / "plan.json"
    path.write_text(plan.model_dump_json(), encoding="utf-8")
    rc = main(["validate", str(path)])
    out = capsys.readouterr().out
    assert rc == 1
    assert "empty_timeline" in out


def test_validate_returns_0_when_valid(tmp_path, capsys):
    plan = scaffold_plan("assunto x", PresetName.acao)
    plan.timeline.append(TimelineItem(id="s1", role=Role.hook))
    path = tmp_path / "plan.json"
    path.write_text(plan.model_dump_json(), encoding="utf-8")
    rc = main(["validate", str(path)])
    assert rc == 0


def test_resumo_prints_markdown(tmp_path, capsys):
    plan = scaffold_plan("assunto x", PresetName.viral)
    plan.timeline.append(TimelineItem(id="s1", role=Role.hook))
    path = tmp_path / "plan.json"
    path.write_text(plan.model_dump_json(), encoding="utf-8")
    rc = main(["resumo", str(path)])
    out = capsys.readouterr().out
    assert rc == 0
    assert out.startswith("# ")
    assert "Timeline" in out
```

- [ ] **Step 2: Rodar e confirmar falha**

Run: `pytest tests/test_cli.py -v`
Expected: FAIL com `ModuleNotFoundError: No module named 'video_plan_editor.cli'`.

- [ ] **Step 3: Implementar `cli.py`**

```python
# video_plan_editor/cli.py
from __future__ import annotations

import argparse
import sys

from .builder import scaffold_plan
from .models import EditPlan, PresetName
from .resumo import render_resumo
from .validate import validate_plan


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="vpe", description="video-plan-editor")
    sub = parser.add_subparsers(dest="command", required=True)

    sc = sub.add_parser("scaffold", help="Gera um plano-esqueleto a partir do input")
    sc.add_argument("input", help="assunto, link de página ou link de vídeo")
    sc.add_argument("--preset", required=True, choices=[p.value for p in PresetName])
    sc.add_argument("--title", default=None)

    va = sub.add_parser("validate", help="Valida um plano-edicao.json")
    va.add_argument("plan", help="caminho do plano JSON")

    rs = sub.add_parser("resumo", help="Renderiza RESUMO.md de um plano")
    rs.add_argument("plan", help="caminho do plano JSON")

    args = parser.parse_args(argv)

    if args.command == "scaffold":
        plan = scaffold_plan(args.input, PresetName(args.preset), title=args.title)
        print(plan.model_dump_json(indent=2))
        return 0

    if args.command == "validate":
        plan = EditPlan.model_validate_json(_read(args.plan))
        issues = validate_plan(plan)
        for issue in issues:
            print(f"[{issue.severity}] {issue.code}: {issue.message}")
        return 1 if any(i.severity == "error" for i in issues) else 0

    if args.command == "resumo":
        plan = EditPlan.model_validate_json(_read(args.plan))
        print(render_resumo(plan), end="")
        return 0

    return 2


def _read(path: str) -> str:
    with open(path, encoding="utf-8") as f:
        return f.read()


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 4: Rodar e confirmar que passa**

Run: `pytest tests/test_cli.py -v`
Expected: PASS (4 testes).

- [ ] **Step 5: Rodar a suíte inteira**

Run: `pytest -v`
Expected: PASS (todos os testes das Tasks 1–7).

- [ ] **Step 6: Smoke test do console script**

Run: `vpe scaffold "como fazer pão" --preset viral`
Expected: imprime um JSON com `"preset": "viral"` e `"kind": "topic"`.

- [ ] **Step 7: Commit**

```bash
git add video_plan_editor/cli.py tests/test_cli.py
git commit -m "feat: CLI vpe (scaffold/validate/resumo)"
```

---

### Task 8: SKILL.md (orquestração da skill)

**Files:**
- Create: `SKILL.md`

Este arquivo não tem teste automatizado; é a interface da skill. A validação é a revisão humana + o smoke test do CLI da Task 7.

- [ ] **Step 1: Escrever `SKILL.md`**

````markdown
---
name: video-plan-editor
description: Gera um plano profissional de edição de vídeo a partir de um assunto ou um link (página/vídeo). Detecta o tipo de input, analisa a melhor ação de edição, escolhe um preset de estilo (acao/suave/promo/vendas/viral) e emite plano-edicao.json + RESUMO.md. Render é opcional (planos futuros). Use quando o usuário der um assunto/link e pedir "plano de edição", "editar vídeo", "clipe", "corte para Reels/TikTok", "vídeo promocional/de vendas", ou um plano de edição de vídeo.
---

# video-plan-editor

Transforma um **assunto** ou **link** num **plano profissional de edição** (JSON
renderer-agnóstico) + resumo legível. O plano é o entregável; o render é opcional.

## Pré-requisitos
- Pacote instalado: `pip install -e .` (expõe o CLI `vpe`).

## Fluxo (sempre nesta ordem)

1. **Detectar + esqueleto** — rode o CLI para classificar o input e aplicar o preset:
   ```bash
   vpe scaffold "<assunto ou link>" --preset <acao|suave|promo|vendas|viral> > plano-edicao.json
   ```
   Se o usuário não pediu preset, escolha o mais adequado ao objetivo (ver tabela abaixo)
   e diga qual escolheu e por quê.

2. **Analisar a melhor ação** — com base no `source.kind`:
   - `topic`/`page`: o objetivo é um vídeo gerado (explainer/promo/vendas). Escreva um
     roteiro curto e preencha `timeline` com cenas (`role`: hook→point(s)→cta), cada uma
     com `content.headline`, `content.narration` e `captions`.
   - `video`: o objetivo é cortar footage real (highlights/supercut/viral). Preencha
     `timeline` com `source_in`/`source_out` por trecho relevante + `captions`.
   Atualize `intent.best_action_rationale` explicando a decisão.

3. **Validar** — rode os guardrails antes de qualquer render:
   ```bash
   vpe validate plano-edicao.json
   ```
   Corrija todos os itens `[error]` (timeline vazia, ranges invertidos, timing de
   legenda). `[warning]` (ex.: sem hook) são recomendações.

4. **Resumo** — gere o documento legível para o usuário aprovar:
   ```bash
   vpe resumo plano-edicao.json > RESUMO.md
   ```
   Mostre o RESUMO ao usuário.

5. **Render (opcional)** — ainda não implementado nesta fase. Quando o usuário pedir o
   MP4, isso será coberto pelos planos de Fase 2 (ingest de vídeo) e Fase 3 (adaptadores
   FFmpeg/HyperFrames). Por ora, entregue o plano + resumo.

## Presets

| Preset | corte médio | transições | trilha | legenda | aspect | uso |
|---|---|---|---|---|---|---|
| acao   | 1–2s | whip/zoom | alta | karaoke | 9:16 | dinâmico |
| suave  | 4–6s | crossfade | baixa | minimal | 16:9 | institucional |
| promo  | 2–3s | cut+zoom | média-alta | block | 16:9/1:1 | clipe promocional |
| vendas | 2–4s | cut | média | block+CTA | 16:9/9:16 | VSL/oferta |
| viral  | 0.8–1.5s | jump cut | alta | karaoke | 9:16 | TikTok/Instagram |

## Regras de ouro
- O plano é **renderer-agnóstico**: descreva intenção (cenas, cortes, ritmo, legendas),
  não comandos FFmpeg.
- Sempre rode `vpe validate` e zere os `[error]` antes de apresentar.
- Sempre mostre o `RESUMO.md` e peça aprovação antes de qualquer render futuro.
- Identidade default PT-BR; CTA INEMA.CLUB como última cena quando for vídeo gerado
  (consistente com as skills video-explicativo / videos-cursos-inema), desligável a pedido.
````

- [ ] **Step 2: Commit**

```bash
git add SKILL.md
git commit -m "docs: SKILL.md (orquestração detect->plano->validate->resumo)"
```

---

## Self-Review

**Spec coverage:**
- Detect (topic/page/video) → Task 3 ✓
- Best action + `intent.best_action_rationale` → builder (Task 6) + SKILL.md (Task 8) ✓
- Presets (acao/suave/promo/vendas/viral) → Task 2 ✓
- Schema `EditPlan` abstrato/serializável → Task 1 ✓
- Validação/guardrails preflight → Task 4 ✓
- Resumo legível → Task 5 ✓
- CLI (gera plano + resumo) → Task 7 ✓
- Identidade PT-BR/INEMA → SKILL.md (Task 8) ✓
- **Fora desta fase (declarado):** ingest de vídeo real (Fase 2), render FFmpeg/HyperFrames (Fase 3), Remotion/OTIO (v2/v3). Coberto pela seção Escopo. ✓

**Placeholder scan:** sem TBD/TODO; todo passo de código tem código completo. ✓

**Type consistency:** `classify_input`, `SourceKind`, `style_for`, `PRESETS`, `PresetProfile`, `validate_plan`/`is_valid`/`Issue`, `render_resumo`, `scaffold_plan`, `EditPlan`/`Meta`/`Source`/`Intent`/`Style`/`Output`/`TimelineItem`/`Caption`/`Content`/`Render`, `PresetName`, `Aspect.portrait="9:16"`, `EngineHint.auto` — nomes idênticos entre tasks e testes. ✓
