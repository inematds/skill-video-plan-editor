# Motion — Texturas cinematográficas (SVG, sem assets)

Grão de filme, halação, color-grade e warp **sintetizados no browser** com SVG
`feTurbulence` (Perlin noise). Zero imagens. Determinístico no render. Fonte: W3C/MDN +
CSS-Tricks + Codrops.

## Grão de filme (film grain)
```html
<svg width="0" height="0"><filter id="grain">
  <feTurbulence type="fractalNoise" baseFrequency="0.65" numOctaves="3" stitchTiles="stitch"/>
</filter></svg>
```
```css
.grain-layer{ position:absolute; inset:0; pointer-events:none; opacity:.08;
  filter:url(#grain); mix-blend-mode:overlay; }
```
- `type="fractalNoise"` = textura nuvem/gás suave; `type="turbulence"` = líquido/ondulado.
- `baseFrequency` = grossura (maior = mais fino); `numOctaves` = detalhe.
- Grão animado (cintila): trocar `seed` por frame, ou animar `baseFrequency` levemente.

## Gradiente granulado + color grade (halação)
Noise EMBAIXO do gradiente + filtro de contraste empurra mid-tones para extremos.
```css
.graded{ background: linear-gradient(120deg, #FFC30033, transparent), url(#grainURL);
  filter: contrast(170%) brightness(1.05) saturate(1.1); }
```
Para halação quente: camada radial âmbar com `mix-blend-mode:screen` + `blur`.

## Warp / distorção líquida
```html
<filter id="warp">
  <feTurbulence type="turbulence" baseFrequency="0.01 0.4" numOctaves="2" result="t"/>
  <feDisplacementMap in="SourceGraphic" in2="t" scale="50" xChannelSelector="R" yChannelSelector="G"/>
</filter>
```
- `baseFrequency` com dois valores (`x y`) assimétricos → distorção direcional/horizontal.
- Animar `scale` do `feDisplacementMap` de 0→N dá efeito de "derreter"/heat-haze.

## Vinheta / luz volumétrica (fake, CSS)
- Vinheta: `radial-gradient` escuro nas bordas + `mix-blend-mode:multiply`.
- "God rays" simples: gradiente cônico/linear claro com `blur` forte e `opacity` baixa,
  animar leve rotação/translate. (Volumetria real = WebGL, fase 2.)

## Uso
Aplicar `grain` + `graded` como camadas globais (`data-layout-ignore` no HyperFrames para
não acusar overflow). Mantêm o look "filme" uniforme sobre stills do flux2-klein e sobre
cenas de motion graphics.
