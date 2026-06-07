# Tokens — Identidade visual

Constrangimentos que mantêm consistência e "marca" (1–2 fontes, 2–3 pesos, paleta fixa).

## Paleta (dark premium âmbar — house style INEMA)
```css
:root{
  --bg:#0D1321; --bg2:#1D2D44; --bg3:#3E5C76;
  --fg:#F0EBD8; --fg2:#748CAB;
  --accent:#FFC300;  /* âmbar — keyword/destaque */
  --accent2:#FF6B35; /* laranja — gradiente/energia */
  --green:#2EC4B6;   /* sucesso/código */
  --red:#E63946;     /* alerta/dor */
}
```
Highlight de keyword (estilo legenda): fundo `--accent` ou `--green` atrás da palavra-chave.

## Tipografia (constraint: poucas famílias, pesos fortes)
| Papel | Fonte | Uso |
|---|---|---|
| **Display/impacto** | **Anton** (900, condensada) | títulos editoriais gigantes, hooks |
| Títulos limpos | **Sora** (700/800) | títulos de cena, números |
| Corpo/legenda | **Inter** (400/500/700) | subtítulos, legendas, texto |
| Mono/rótulo | **JetBrains Mono** (400/700) | kickers, URLs, código, timecodes |
| (Opcional premium) | **Fraunces** (serif display) | tom luxo/editorial elegante |

Escala tipográfica (9:16, ajustar p/ 16:9): hook 88–110px · título 48–72px · sub 28–36px ·
legenda karaoke 44–56px · kicker 18–22px.

## Fontes — instalação
Já em `assets/fonts`: Sora, Inter, JetBrains Mono. **Faltam (buscar quando for renderizar):
Anton** (obrigatória p/ editorial) e **Fraunces** (opcional premium). Subset latin .woff2
local via `@font-face` — **nunca** Google Fonts CDN (some no render do HyperFrames).

## Legenda dinâmica (karaoke) — estilo
- ALL-CAPS opcional, peso forte (Anton/Sora 800).
- Contorno preto fino (`-webkit-text-stroke: 2px #000`) para legibilidade sobre qualquer fundo.
- Keyword destacada em `--accent`/`--green`.
- 1–3 palavras por vez (ver `pacing.md`).

## Acabamento
Grão + color grade global (ver `motion/textures.md`) em todos os vídeos para coesão de
"filme". CTA final padrão INEMA.CLUB (âmbar com glow), desligável a pedido.
