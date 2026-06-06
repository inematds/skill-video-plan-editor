# Spec — Skill `video-plan-editor`

**Data:** 2026-06-06
**Status:** Aprovado (design v1)
**Autor:** Nei + Claude

## Propósito

Skill que recebe um **input** (assunto em texto, link de página/artigo, ou link de
vídeo) → **analisa a melhor ação de edição** → gera um **plano profissional de edição de
vídeo** como dado estruturado (JSON abstrato, renderer-agnóstico) acompanhado de um resumo
legível. O **render é um passo opcional** posterior — o plano é o entregável principal e
deve ser usável por outros sistemas.

Referência de inspiração: https://demo.reactvideoeditor.com (React + Remotion).
Base de código reaproveitada: fork `github.com/inematds/mcp-video` (Apache-2.0).

## Decisões de design

- **Plano abstrato renderer-agnóstico (Abordagem A)** — escolhido. O plano descreve a
  *intenção* de edição, não comandos de uma ferramenta específica. Adaptadores traduzem
  para a ferramenta na hora do render.
- **Abordagem B (plano nativo Remotion)** e **Abordagem C (pipeline mcp-video / OTIO
  `.otio`)** ficam no roadmap como v2 e v3.
- Entregável = plano; render = opcional.

## Fluxo

1. **Detect** — classifica o input:
   - texto puro → `topic` (assunto)
   - URL resolvível por yt-dlp / extensão de vídeo / domínio de vídeo → `video`
   - outra URL → `page`
2. **Ingest + Analyze**
   - `video`: baixa (yt-dlp) → `ffprobe` (metadata) → transcrição com timestamps por
     palavra → detecção de silêncio/cenas (Auto-Editor + ffmpeg `silencedetect`/scene) →
     auto-legenda de trechos para localizar highlights (padrão LAVE).
   - `page`: extrai texto + imagens relevantes.
   - `topic`: vira roteiro (sem ingest).
3. **Best action** — decide o modo:
   - footage real → `highlights` / `supercut` / corte de silêncio / clipes
   - página/assunto → vídeo gerado (motion graphics + narração)
   - grava `best_action_rationale` no plano (transparência da decisão).
4. **Preset de estilo** — `acao | suave | promo | vendas | viral` (inferido do
   assunto/objetivo ou passado explicitamente pelo usuário).
5. **Generate** — emite `plano-edicao.json` + `RESUMO.md` (legível: cenas, cortes, ritmo,
   trilha, legendas, aspecto).
6. **Render (opcional)** — adaptador executa o plano → MP4, extraindo frames para
   validação humana (não há áudio audível no ambiente — usuário valida a locução).

## Schema do plano (`EditPlan`, pydantic, serializável em JSON)

```jsonc
{
  "version": "1.0",
  "meta": { "title": "string", "language": "pt-BR" },
  "source": {
    "kind": "video|page|topic",
    "ref": "url ou texto",
    "media": { "path": "?", "duration": 0, "fps": 0, "resolution": "WxH" } // se video
  },
  "intent": {
    "goal": "highlights|supercut|promo|explainer|sales|viral",
    "best_action_rationale": "por que esse modo foi escolhido"
  },
  "style": {
    "preset": "acao|suave|promo|vendas|viral",
    "pacing": { "avg_cut_seconds": 0, "energy": 0.0 },        // energy 0-1
    "transitions": ["cut","crossfade","whip","zoom"],
    "music": { "energy": 0.0 },
    "captions": { "enabled": true, "style": "karaoke|block|minimal", "position": "?" },
    "color": { "look": "neutral|punchy|cinematic" }
  },
  "output": {
    "aspect": "16:9|9:16|1:1",
    "duration_target_seconds": 0,
    "platform": "youtube|tiktok|reels|generic"
  },
  "timeline": [
    {
      "id": "string",
      "role": "hook|intro|point|broll|cta",
      "source_in": 0.0, "source_out": 0.0,                    // corte de footage real
      "content": { "headline": "?", "narration": "?", "broll_query": "?" }, // cena gerada
      "captions": [{ "t_in": 0.0, "t_out": 0.0, "text": "string" }],
      "overlays": [],
      "transition_out": "cut|crossfade|whip|zoom"
    }
  ],
  "render": { "engine_hint": "auto|ffmpeg|hyperframes" }
}
```

Validação: `EditPlan` em pydantic 2, com guardrails reaproveitados do mcp-video (bounds de
filtro, compatibilidade de merge, timing/overflow de texto, opacidade de overlay) rodando
em **preflight** — antes de qualquer chamada FFmpeg no passo de render.

## Presets (perfis de parâmetro sobre o mesmo schema)

| Preset | corte médio | transições | trilha (energy) | legenda | aspect default | uso |
|---|---|---|---|---|---|---|
| **acao**   | 1–2s        | whip/zoom/cut | alta        | karaoke punchy | 9:16        | dinâmico |
| **suave**  | 4–6s        | crossfade     | baixa-média | block minimal  | 16:9        | institucional/calmo |
| **promo**  | 2–3s        | cut+zoom      | média-alta  | block          | 16:9 / 1:1  | clipe promocional |
| **vendas** | 2–4s c/ganchos | cut        | média       | block + CTA    | 16:9 / 9:16 | VSL/oferta |
| **viral**  | 0.8–1.5s    | jump cut/zoom | alta        | karaoke        | 9:16        | TikTok/Instagram |

## Componentes (unidades isoladas)

| Unidade | Faz | Depende de |
|---|---|---|
| `detect` | classifica input (topic/page/video) | stdlib, yt-dlp probe |
| `ingest/video` | download + ffprobe + transcribe + scene/silence | yt-dlp, ffmpeg, auto-editor, transcrição |
| `ingest/page` | extrai texto/imagens da página | fetch/parser |
| `ingest/topic` | normaliza assunto em briefing | — |
| `analyze` | decide best action + monta `intent` | os ingests |
| `presets` | perfis de estilo (dataclasses) | — |
| `plan` | schema `EditPlan` + montagem + validação/guardrails | pydantic, guardrails (mcp-video) |
| `render/ffmpeg` | executa plano via FFmpeg (concat/trim/overlay/transições) | ffmpeg, ffmpeg_helpers |
| `render/autoeditor` | corte de silêncio/highlights + export EDL | auto-editor |
| `render/hyperframes` | cenas geradas (motion graphics/narração/CTA) | hyperframes, kokoro tts |
| `SKILL.md` | orquestra o fluxo; PT-BR; padrões INEMA | — |

## Reuso do fork mcp-video

Copiar/portar apenas o reaproveitável (sem o server MCP): `validation.py`, `errors.py`,
`*_guardrails.py`, `ffmpeg_helpers.py`, `models.py` (`EditResult`/`VideoInfo`).

## Identidade (default configurável)

PT-BR; dark premium âmbar e CTA INEMA.CLUB disponíveis como default opcional no preset de
vídeo gerado (consistente com as skills `video-explicativo` / `videos-cursos-inema`).
Desligável via parâmetro.

## Roadmap

- **v2 — Abordagem B:** render nativo Remotion (plano → Tracks/Items), alinhado à
  reactvideoeditor.com.
- **v3 — Abordagem C:** export pipeline mcp-video + OTIO `.otio` para NLEs (interchange
  com Premiere/Resolve/Final Cut via Auto-Editor `--export`).

## Critérios de sucesso

- Dado qualquer input (assunto/página/vídeo), a skill emite um `plano-edicao.json` válido
  (passa no schema + guardrails) e um `RESUMO.md` legível, escolhendo e justificando a
  melhor ação.
- O plano é independente de ferramenta (pode ser consumido por outro sistema).
- Com `--render`, o plano vira MP4 no aspecto/preset corretos, com frames de validação.
- Trocar o preset muda ritmo/transições/trilha/legenda/aspect sem reescrever o plano base.

## Fora de escopo (v1)

- Render Remotion/OTIO (v2/v3).
- Edição interativa via timeline UI.
- Cloud/Lambda render.
