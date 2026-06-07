# Archetype: cinematic-hero

Cena de abertura/hook premium: still de fundo (flux2-klein) com **push-in lento**,
**grão de filme + color grade**, e **título revelado linha-a-linha por máscara**.
Sensação de "filme", não de slide.

## Parâmetros (do beat)
- `headline` — frase do gancho (1–6 palavras, impactante).
- `kicker` — rótulo curto opcional (ex.: "INEMA · NEGÓCIOS").
- `bg` — caminho da still gerada (flux2-klein) OU gradiente se ausente.
- `duration` — duração da cena (s), do `AUDIO[]`.

## Camera + recipes
`camera: slow push-in` · recipes: `push-in`, `mask-reveal`, `grain`, `graded` (ver
`motion/`). Ease: `cinematicSmooth` (push) + `cinematicFlow` (título).

## HTML (dentro de `.scene-inner`)
```html
<section class="scene clip" data-track-index="1">
  <div class="scene-inner hero" style="opacity:0">
    <div class="hero-media"><img src="${bg}" alt=""></div>
    <div class="hero-grade" data-layout-ignore></div>
    <div class="hero-grain" data-layout-ignore></div>
    <div class="hero-text">
      <span class="hero-kicker">${kicker}</span>
      <h1 class="hero-title">${headline}</h1>
      <span class="hero-rule"></span>
    </div>
  </div>
</section>
```

## CSS
```css
.hero{ position:relative; width:100%; height:100%; overflow:hidden; }
.hero-media{ position:absolute; inset:0; }
.hero-media img{ width:100%; height:100%; object-fit:cover;
  transform: scale(calc(1.05 + 0.12*var(--p,0))); transform-origin:50% 45%; }
.hero-grade{ position:absolute; inset:0;
  background:linear-gradient(180deg, rgba(13,19,33,.1), rgba(13,19,33,.85));
  mix-blend-mode:multiply; }
.hero-grain{ position:absolute; inset:0; opacity:.08; filter:url(#grain);
  mix-blend-mode:overlay; pointer-events:none; }
.hero-text{ position:absolute; left:8%; bottom:14%; right:8%; }
.hero-kicker{ font-family:'JetBrains Mono',monospace; font-size:20px; letter-spacing:3px;
  color:var(--accent); text-transform:uppercase; }
.hero-title{ font-family:'Anton',sans-serif; font-size:96px; line-height:.98;
  color:var(--fg); text-transform:uppercase; margin-top:12px; }
.hero-title .line-mask{ overflow:hidden; display:block; }
.hero-rule{ display:block; height:5px; width:0; margin-top:18px;
  background:linear-gradient(90deg,var(--accent),var(--accent2)); }
```

## GSAP (time-driven)
```js
const o = { p: 0 };
const tl = gsap.timeline();
tl.fromTo(".hero", { opacity:0 }, { opacity:1, duration:0.4, ease:"power2.out" }, 0);
// push-in pela duração toda
tl.to(o, { p:1, duration: duration, ease:"cinematicSmooth",
  onUpdate:()=>hero.style.setProperty("--p", o.p) }, 0);
// título por máscara linha-a-linha
const split = SplitText.create(".hero-title", { type:"lines", mask:"lines" });
tl.from(split.lines, { yPercent:100, duration:0.8, ease:"cinematicFlow", stagger:0.12 }, 0.35);
tl.from(".hero-kicker", { y:14, opacity:0, duration:0.5, ease:"power2.out" }, 0.3);
tl.to(".hero-rule", { width:180, duration:0.6, ease:"power3.out" }, 0.9);
```

## Notas
- `grain`/`grade` com `data-layout-ignore` (HyperFrames não acusa overflow).
- Anima `.scene-inner`/filhos, nunca o `.clip`.
- Sem `bg`: trocar `.hero-media img` por um gradiente `graded` (ver `motion/textures.md`).
- Fonte `Anton` precisa estar em `assets/fonts` (ver `tokens.md`).
