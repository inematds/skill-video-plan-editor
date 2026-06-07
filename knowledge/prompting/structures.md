# Prompting — Estruturas de prompt (=KairoBoost)

Expandir um beat curto num prompt cinematográfico rico. Serve para **flux2-klein**
(b-roll/still hoje) e para modelos de vídeo (Sora/Veo/Kling) na fase 2.

Princípio (KairoBoost): de "pessoa correndo" → "pessoa em roupas de corrida profissional,
correndo num parque ao amanhecer com luz dourada, movimento dinâmico, câmera lateral,
expressão de determinação, fundo desfocado, atmosfera motivacional, qualidade
cinematográfica 4K".

## Método 1 — Production Brief (cenas atmosféricas)
Para uma imagem/cena rica e emocionalmente ressonante.
```
[FORMATO E TOM]     gênero + tom. Ex: "anúncio cinematográfico de luxo, nostálgico, íntimo"
[SUJEITO]           personagens/elementos. Ex: "mulher 30s, expressão contemplativa"
[VESTUÁRIO/PROPS]   roupas e objetos. Ex: "suéter bege, relógio de ouro, café fumegante"
[ENQUADRAMENTO]     plano + ângulo. Ex: "close médio, câmera acima da linha dos olhos, 3/4"
[ILUMINAÇÃO/PALETA] luz + cores. Ex: "luz dourada do amanhecer, âmbar/bege/ouro, sombras suaves"
[BEATS DE CÂMERA]   momentos c/ movimento (ver camera/vocabulary.md):
                    0-3s push lento · 3-6s orbit sutil · 6-9s pull back
[MONTAGEM]          cortes/transições. Ex: "match-cut, transição via reflexo no vidro"
[SOM/FOLEY]         sons. Ex: "respiração, xícara, pássaros, piano"
[ACABAMENTO]        look final. Ex: "film grain leve, halação quente, LUT vintage"
```

## Método 2 — Time-Coded Shotlist (sequências rápidas / virais)
Para anúncios, trailers, Reels com sincronização precisa.
```
[CABEÇALHO] Vídeo de [DURAÇÃO]s, [FORMATO], com [TRANSIÇÕES] e [ESTILO DE CÂMERA].
[0-2s] ABERTURA      [plano] em [sujeito] fazendo [ação] + [câmera] + [transição] + [áudio]
[2-4s] DESENVOLVIMENTO [ação] + [câmera] + [transição] + [áudio]
[4-6s] IMPACTO       [ação/VFX] + [câmera] + [transição] + [áudio]
[6-8s] FINALIZAÇÃO   [gesto final] + [câmera fixa] + [imagem final]
```

## Quando usar qual
- **Production Brief** → b-roll atmosférico, VSL, autoridade, abertura premium.
- **Shotlist** → Reels/TikTok, anúncios, qualquer coisa rápida e batida.

## Saída no plano
O prompt expandido vai em `EditPlan.timeline[i].gen_prompt`. Para `render_kind:
generated_still` (flux2-klein) descreva uma IMAGEM (sem movimento) — o movimento vem das
recipes de motion (push-in/parallax aplicados sobre a still).
