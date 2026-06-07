# Prompting — clipe generativo (prompt final + negativo)

Para beats `render_kind: generated_clip` (Seedance/Kling/Veo/Runway/Luma) ou
`generated_still` (flux2-klein). Absorvido do MDD. Use junto de `storyboard.md` (a
direção) e `camera/vocabulary.md` (o movimento).

## Prompt final (master) — parágrafo corrido
Descreve a cena inteira como um plano contínuo, interpolando movimento natural entre os
beats do storyboard. Regras:
- Use o storyboard como guia de planos (ordem, câmera, ação, continuidade, estilo).
- **Não** peça texto/legenda/bordas/layout renderizados (IA erra texto; a CTA entra na edição).
- Mantenha personagens, objetos e ambiente **consistentes**; **termine no estado final** (freeze/reveal).
- Não invente novos elementos.

Esqueleto (preencher): `[tom/estilo cinematográfico + lentes + grade de cor] → [estado
inicial] → [beats com câmera+ação+continuidade] → [virada] → [estado final/freeze]. Same
character, same wardrobe, same light direction and color grade in every shot; natural
interpolated movement; no on-screen text, no logos, no extra speaking characters.`

Exemplo (autoridade/negócios, 16:9) — ver o pacote real em `examples/` quando existir:
> Cinematic premium short film, 35–85mm, shallow DoF, film grain, warm halation,
> navy-amber-teal grade. Slow push-in on a man in a dark suit hunched over a glowing
> laptop in a cramped dark office (cold light)… [beats]… ending on a slow push-in onto his
> upright silhouette watching the city skyline at dawn, freeze. Same actor/wardrobe/left
> dawn light/grade throughout; no text, no logos, no extra speaking characters.

## Prompt negativo — sempre incluir
> text, captions, subtitles, watermark, logos, brand marks, UI overlays, holograms,
> extra speaking people, changing outfits, changing face, inconsistent lighting, jump cuts
> without continuity, warped hands, extra fingers, anatomy errors, oversaturated colors,
> cheap CGI, shaky nervous camera, lens flare overload, cartoonish look, low resolution.

## Para flux2-klein (still)
Descreva uma IMAGEM (sem verbos de movimento): composição, luz, DOF, acabamento (grão/LUT).
O movimento (push-in/parallax) é aplicado depois pelas recipes de `motion/` sobre a still.
Mantenha o mesmo prompt negativo. Aspecto 16:9 (1536×1024) ou 9:16 no playground inemaimg.

## Onde isso entra no EditPlan
`timeline[i].gen_prompt` = prompt final do beat; a continuidade vai anotada; o negativo é
global do plano. Para um pacote de direção completo (storyboard + prompt + negativo), use
a skill `mestre-direcao-dinamica`.
