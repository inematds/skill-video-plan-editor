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
