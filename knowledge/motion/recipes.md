# Motion — Recipes (GSAP/CSS, time-driven, determinístico)

Receitas nomeadas. Todas dirigidas por **tempo** (timeline GSAP), não scroll. Verificadas
contra docs GSAP e tutoriais Codrops. Prioridade SVG/CSS/GSAP (determinístico no render);
WebGL é fase 2.

## push-in (câmera virtual / dolly in)
Dirige UMA var `--progress` e aplica em `scale` — sincroniza imagem + texto.
```js
const o = { p: 0 };
gsap.to(o, { p: 1, duration: sceneDur, ease: "cinematicSmooth",
  onUpdate: () => el.style.setProperty("--progress", o.p) });
```
```css
.media { transform: scale(calc(1 + 0.12 * var(--progress))); transform-origin: 50% 45%; }
```

## parallax (profundidade em camadas)
Camadas movem em velocidades diferentes; bg também borra (DOF).
```js
gsap.to(".layer-bg",  { yPercent: -6,  ease: "none", duration: d });
gsap.to(".layer-mid", { yPercent: -12, ease: "none", duration: d });
gsap.to(".layer-fg",  { yPercent: -20, ease: "none", duration: d });
```
```css
.layer-bg { filter: blur(6px); }   /* DOF: fundo em bokeh */
```

## dof (profundidade de campo)
Sujeito nítido, fundo `filter:blur()`; opcional animar foco (rack focus): `blur` do bg
de 0→8px enquanto o fg vai 8px→0.

## mask-reveal (título linha-a-linha, cinematográfico)
GSAP SplitText com máscara de clip (free no GSAP 3.13).
```js
const split = SplitText.create(".title", { type: "lines", mask: "lines" });
gsap.from(split.lines, { yPercent: 100, duration: 0.8, ease: "cinematicFlow", stagger: 0.12 });
```
Sem SplitText: envolver cada linha em `.mask{overflow:hidden}` e animar filho `y:100%→0`.

## char-stagger (tipografia cinética, palavra/char)
```js
const s = SplitText.create(".kinetic", { type: "chars" });
gsap.from(s.chars, { yPercent: 100, opacity: 0, duration: 0.5,
  ease: "power3.out", stagger: 0.02 });
```
Container precisa de `overflow:hidden` por linha. Para "word cascade" use `type:"words"`.

## pop (slam-in de número/ícone/keyword)
```js
gsap.from("#num", { scale: 1.6, opacity: 0, duration: 0.5, ease: "back.out(2.2)" });
```

## count-up (número contando)
```js
const n = { v: 0 };
gsap.to(n, { v: 340, duration: 1.2, ease: "power2.out", snap: { v: 1 },
  onUpdate: () => el.textContent = Math.round(n.v) });
```

## bar-grow (barra/gráfico crescendo)
```css
.bar { transform: scaleX(var(--p, 0)); transform-origin: left center; }
```
```js
gsap.fromTo(barObj, { p: 0 }, { p: 1, duration: 0.8, ease: "cinematicSmooth",
  onUpdate: () => bar.style.setProperty("--p", barObj.p) });
```

## wipe-underline (sublinhado âmbar que varre)
```js
gsap.from(".underline", { scaleX: 0, transformOrigin: "left", duration: 0.5, ease: "power3.out" });
```

## whip-pan (transição com motion blur)
```js
const tl = gsap.timeline();
tl.to(sceneA, { xPercent: -30, filter: "blur(14px)", opacity: 0, duration: 0.18, ease: "expo.in" })
  .fromTo(sceneB, { xPercent: 30, filter: "blur(14px)", opacity: 0 },
                  { xPercent: 0, filter: "blur(0px)", opacity: 1, duration: 0.22, ease: "expo.out" });
```

## knockout-text (texto como máscara revelando imagem/padrão)
SVG `clip-path` com `<text>`; anima o fundo atrás ou o bloco de texto.
```html
<svg viewBox="0 0 1080 1920"><defs><clipPath id="ko"><text x="50%" y="50%"
  font-size="220" font-weight="900" text-anchor="middle">INEMA</text></clipPath></defs>
  <image href="bg.jpg" width="1080" height="1920" clip-path="url(#ko)"/></svg>
```

## distortion (warp líquido, SVG)
`feTurbulence` → `feDisplacementMap` (ver `textures.md`); animar `scale` do displacement.

## Regra de aplicação
Cada beat escolhe 1–3 recipes coerentes com a `camera` e a `emotion`. Não empilhar tudo —
movimento com propósito (ver `camera/vocabulary.md`).
