# skill-video-plan-editor

Skill (Claude Code) que transforma um **assunto** ou um **link** num **plano profissional
de edição de vídeo** — dado estruturado, renderer-agnóstico — e, opcionalmente, renderiza
o vídeo.

> Você passa um assunto/link → a skill **analisa a melhor ação de edição** → gera
> `plano-edicao.json` + `RESUMO.md`. Render é um passo opcional depois.

## Por que

As ferramentas de edição programática são fragmentadas: FFmpeg (CLI bruto), Auto-Editor
(corte por análise), MoviePy (Python), Remotion (React), HyperFrames (HTML→MP4). Falta a
camada que, a partir de linguagem natural, **decide o que fazer** e emite um plano de
edição limpo e portável. É isso que esta skill faz.

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

- **Detect:** classifica o input (assunto / página / vídeo).
- **Ingest + Analyze:** vídeo → download (yt-dlp) + `ffprobe` + transcrição + detecção de
  silêncio/cenas + auto-legenda de highlights (padrão LAVE). Página → extrai texto.
  Assunto → vira roteiro.
- **Best action:** escolhe o modo (highlights/supercut/corte de silêncio para footage
  real; vídeo gerado para assunto/página) e registra o porquê no plano.
- **Preset de estilo:** `acao | suave | promo | vendas | viral`.
- **Plano:** JSON abstrato (não amarrado a nenhuma ferramenta) + `RESUMO.md` legível.
- **Render (opcional):** adaptadores executam o plano via FFmpeg / Auto-Editor /
  HyperFrames.

## Presets

| Preset | corte médio | transições | trilha | legenda | aspect | uso |
|---|---|---|---|---|---|---|
| **acao**   | 1–2s | whip/zoom | alta | karaoke | 9:16 | dinâmico |
| **suave**  | 4–6s | crossfade | baixa | block minimal | 16:9 | institucional |
| **promo**  | 2–3s | cut+zoom | média-alta | block | 16:9 / 1:1 | clipe promocional |
| **vendas** | 2–4s | cut | média | block + CTA | 16:9 / 9:16 | VSL/oferta |
| **viral**  | 0.8–1.5s | jump cut | alta | karaoke | 9:16 | TikTok/Instagram |

## Stack

- **FFmpeg** — corte/concat/overlay/transições.
- **Auto-Editor** — corte por silêncio/movimento, export EDL.
- **HyperFrames** (heygen-com) — HTML→MP4 para cenas geradas, TTS local (Kokoro).
- Base de guardrails/validação reaproveitada de
  [`inematds/mcp-video`](https://github.com/inematds/mcp-video) (fork Apache-2.0 de
  KyaniteLabs/mcp-video).

## Status

Em desenvolvimento — design v1 aprovado. Veja o spec em
[`docs/superpowers/specs/2026-06-06-video-plan-editor-design.md`](docs/superpowers/specs/2026-06-06-video-plan-editor-design.md)
e a pesquisa em [`PESQUISA-E-DESIGN.md`](PESQUISA-E-DESIGN.md).

### Roadmap

- **v2:** render nativo **Remotion** (plano → Tracks/Items).
- **v3:** export **pipeline mcp-video** + **OTIO `.otio`** para NLEs (Premiere/Resolve/
  Final Cut).

## Licença

A definir.
