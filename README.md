# skill-video-plan-editor

Skill (Claude Code) + pacote Python que transforma um **assunto** ou um **link**
(página/vídeo) num **plano profissional de edição de vídeo** — dado estruturado,
renderer-agnóstico — e, opcionalmente, renderiza o vídeo.

> Você passa um assunto/link → a skill **detecta o tipo de input**, **analisa a melhor
> ação de edição**, escolhe um **preset de estilo** e emite `plano-edicao.json` +
> `RESUMO.md`. O render é um passo opcional depois (Fase 2/3).

---

## Por que

A edição programática de vídeo é fragmentada: FFmpeg (CLI bruto), Auto-Editor (corte por
análise), MoviePy (Python), Remotion (React), HyperFrames (HTML→MP4). Falta a camada que,
a partir de **linguagem natural**, **decide o que fazer** e emite um plano de edição limpo
e portável. É isso que esta skill faz — e o plano, sendo JSON renderer-agnóstico, pode ser
consumido por qualquer um desses backends ou por outros sistemas.

## Instalação

Requer Python ≥ 3.11.

```bash
python3 -m venv .venv && . .venv/bin/activate
pip install -e ".[dev]"
```

Isso expõe o console script **`vpe`**.

## Início rápido

```bash
# 1. Gerar o esqueleto do plano a partir do input + preset
vpe scaffold "como fazer pão caseiro" --preset viral > plano-edicao.json

# 2. (a skill preenche a timeline criativa — veja examples/)

# 3. Validar os guardrails antes de qualquer render
vpe validate plano-edicao.json

# 4. Gerar o resumo legível para aprovação
vpe resumo plano-edicao.json > RESUMO.md
```

## Como funciona

```
input (assunto | link de página | link de vídeo)
   │
   ▼
 detect ─→ ingest+analyze ─→ best action ─→ preset de estilo ─→ PLANO (json + resumo)
                                                                      │
                                                          (opcional)  ▼
                                                                   render → MP4
```

- **Detect** (`vpe`/`detect.py`): classifica o input em `topic`, `page` ou `video` (por
  URL, extensão e domínio).
- **Analyze / best action**: a skill (via `SKILL.md`) decide o modo — vídeo gerado para
  assunto/página, corte de footage real para vídeo — e registra o porquê em
  `intent.best_action_rationale`.
- **Preset de estilo**: `acao | suave | promo | vendas | viral` (perfis de parâmetro).
- **Plano**: JSON abstrato (`EditPlan`, pydantic) + `RESUMO.md` legível.
- **Render (opcional)**: adaptadores FFmpeg / Auto-Editor / HyperFrames (Fase 2/3).

## CLI — exemplos reais

### `vpe scaffold` — detecta o input e aplica o preset

```bash
$ vpe scaffold "https://youtu.be/dQw4w9WgXcQ" --preset viral --title "Corte Viral"
```
```jsonc
{
  "version": "1.0",
  "meta": { "title": "Corte Viral", "language": "pt-BR" },
  "source": { "kind": "video", "ref": "https://youtu.be/dQw4w9WgXcQ", "media": null },
  "intent": {
    "goal": "viral",
    "best_action_rationale": "Input classificado como 'video'; preset 'viral' sugere objetivo 'viral'. ..."
  },
  "style": {
    "preset": "viral",
    "pacing": { "avg_cut_seconds": 1.1, "energy": 0.95 },
    "transitions": ["cut", "zoom"],
    "music": { "energy": 0.95 },
    "captions": { "enabled": true, "style": "karaoke", "position": null },
    "color": { "look": "punchy" }
  },
  "output": { "aspect": "9:16", "duration_target_seconds": 30.0, "platform": "generic" },
  "timeline": [],
  "render": { "engine_hint": "auto" }
}
```
> O input do YouTube foi classificado como `video` e o preset `viral` já aplicou corte
> ~1.1s, legenda karaoke e aspect 9:16. A `timeline` nasce vazia — é preenchida pela skill.

### `vpe validate` — guardrails antes do render

```bash
$ vpe validate examples/exemplo-viral-pao.json
$ echo $?
0
```
Plano com problemas reporta os itens (e retorna código 1 se houver `[error]`):
```text
[error] empty_timeline: timeline tem 0 itens
[warning] no_hook: plano sem cena de hook
```

### `vpe resumo` — documento legível para aprovação

```bash
$ vpe resumo examples/exemplo-viral-pao.json
```
```markdown
# Pão caseiro em 20s

- **Fonte:** topic — como fazer pão caseiro rápido
- **Objetivo:** viral
- **Por que essa ação:** Assunto curto, visual e com payoff imediato — ideal para vídeo gerado vertical com cortes rápidos.
- **Preset:** viral (corte ~1.1s, energia 0.95)
- **Saída:** 9:16, alvo 20.0s, tiktok

## Timeline
1. **hook** (`s1`)
   - Headline: Pão em 20 segundos?!
   - Narração: Olha só que rápido.
   - Legenda [0.0-1.5]: Pão em 20s?!
2. **point** (`s2`)
   - Headline: 3 ingredientes
   - Narração: Farinha, água e fermento.
   - Legenda [1.5-4.0]: Só 3 ingredientes
3. **cta** (`s3`)
   - Headline: INEMA.CLUB
   - Narração: Receita completa no inema ponto club.
   - Legenda [18.0-20.0]: inema.club
```

Veja o plano completo de exemplo em [`examples/exemplo-viral-pao.json`](examples/exemplo-viral-pao.json).

## Presets

| Preset | corte médio | transições | trilha | legenda | aspect | uso |
|---|---|---|---|---|---|---|
| **acao**   | 1–2s | whip/zoom | alta | karaoke | 9:16 | dinâmico |
| **suave**  | 4–6s | crossfade | baixa | minimal | 16:9 | institucional |
| **promo**  | 2–3s | cut+zoom | média-alta | block | 16:9 / 1:1 | clipe promocional |
| **vendas** | 2–4s | cut | média | block + CTA | 16:9 / 9:16 | VSL/oferta |
| **viral**  | 0.8–1.5s | jump cut | alta | karaoke | 9:16 | TikTok/Instagram |

Cada preset é um perfil de parâmetros sobre o **mesmo** schema — trocar o preset muda
ritmo/transições/trilha/legenda/aspect sem reescrever o plano base.

## Schema do plano (`EditPlan`)

JSON serializável (pydantic 2). Campos principais:

| Bloco | Conteúdo |
|---|---|
| `meta` | `title`, `language` |
| `source` | `kind` (video/page/topic), `ref`, `media` (duration/fps/resolution) |
| `intent` | `goal` (highlights/supercut/promo/explainer/sales/viral), `best_action_rationale` |
| `style` | `preset`, `pacing{avg_cut_seconds,energy}`, `transitions[]`, `music{energy}`, `captions{style}`, `color{look}` |
| `output` | `aspect` (16:9/9:16/1:1), `duration_target_seconds`, `platform` |
| `timeline[]` | `id`, `role` (hook/intro/point/broll/cta), `source_in/out` (corte real) **ou** `content{headline,narration,broll_query}` (cena gerada), `captions[]`, `overlays[]`, `transition_out` |
| `render` | `engine_hint` (auto/ffmpeg/hyperframes) |

## Como a skill orquestra (`SKILL.md`)

1. `vpe scaffold "<input>" --preset <...>` → esqueleto do plano.
2. Preenche a `timeline` (roteiro/cenas para assunto/página; `source_in/out` para vídeo).
3. `vpe validate` → zera os `[error]`.
4. `vpe resumo` → mostra ao usuário para aprovar.
5. Render (Fase 2/3) quando solicitado.

Identidade default PT-BR; CTA INEMA.CLUB como última cena em vídeos gerados (desligável).

## Base de conhecimento (`knowledge/`)

O que dá "talento" à skill — vocabulário e padrões que ela usa para **criar** (não copiar).
A composição de cada vídeo é autoral; estes arquivos são os blocos de construção.

| Pilar | Conteúdo |
|---|---|
| `strategy/` | NARRATIVA — Viral5, Save the Cat, Hero, Hook-Value-CTA, hooks 3s, cases, formatos (Reels/VSL/Autoridade), templates, matriz, checklist |
| `camera/vocabulary.md` | linguagem de câmera (ponte: vira prompt **e** parâmetro de motion) |
| `storyboard.md` | **direção de cena** — conflito visual, câmera por função, continuidade sagrada, freeze final (**absorvido do MDD**) |
| `prompting/` | expandir cada beat em prompt cinematográfico; `clip-direction.md` = prompt-final + negativo |
| `motion/` | eases cinematográficos, recipes GSAP/CSS time-driven, texturas feTurbulence (grão/halação sem assets) |
| `archetypes/` | cenas prontas (HTML+CSS+GSAP), ex.: `cinematic-hero` |
| `tokens.md` · `pacing.md` | identidade (paleta/fontes) e ritmo (word-by-word, pattern interrupt) |

**Integração com o MDD** ([`mestre-direcao-dinamica`](#)): para beats
`render_kind: generated_clip`/`generated_still`, a skill **delega a direção cinematográfica
ao MDD** — que devolve storyboard painel-a-painel + prompt final + prompt negativo de
qualidade de diretor. `video-plan-editor` é o **orquestrador** (estratégia → plano →
execução); o MDD é o **motor de direção** dos beats generativos. Os princípios do MDD
(conflito visual, continuidade, freeze, CTA fora do prompt) estão destilados em
`knowledge/storyboard.md` e `knowledge/prompting/clip-direction.md`.

## Arquitetura

```
video_plan_editor/
├── models.py     # schema EditPlan (pydantic) + enums
├── presets.py    # PresetProfile, registry PRESETS, style_for()
├── detect.py     # classify_input() -> SourceKind
├── validate.py   # Issue, validate_plan(), is_valid()  (guardrails preflight)
├── resumo.py     # render_resumo() plano -> markdown
├── builder.py    # scaffold_plan() detect + preset -> EditPlan
└── cli.py        # vpe scaffold | validate | resumo
```

A camada de guardrails/validação é inspirada no fork
[`inematds/mcp-video`](https://github.com/inematds/mcp-video) (Apache-2.0, de
KyaniteLabs/mcp-video), que envolve FFmpeg + HyperFrames.

## Desenvolvimento

```bash
. .venv/bin/activate
pytest -v          # 35 testes
vpe scaffold "teste" --preset acao
```

## Roadmap

- **Fase 1 (atual):** núcleo gerador de plano — schema, presets, detect, validação,
  resumo, CLI. ✅
- **Fase 2:** ingest de vídeo real — yt-dlp + ffprobe + transcrição + detecção de
  silêncio/cena (Auto-Editor) + auto-highlights (padrão LAVE).
- **Fase 3:** adaptadores de render — FFmpeg, HyperFrames.
- **v2 (B):** render nativo **Remotion** (plano → Tracks/Items).
- **v3 (C):** export **pipeline mcp-video** + **OTIO `.otio`** para NLEs
  (Premiere/Resolve/Final Cut).

## Documentos

- Spec de design: [`docs/superpowers/specs/2026-06-06-video-plan-editor-design.md`](docs/superpowers/specs/2026-06-06-video-plan-editor-design.md)
- Plano de implementação (Fase 1): [`docs/superpowers/plans/2026-06-06-video-plan-editor-core.md`](docs/superpowers/plans/2026-06-06-video-plan-editor-core.md)
- Pesquisa profunda: [`PESQUISA-E-DESIGN.md`](PESQUISA-E-DESIGN.md)

## Licença

A definir.
