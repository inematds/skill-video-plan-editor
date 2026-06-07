# Motion — Easing (a alavanca #1)

A doc do GSAP chama easing de "possivelmente a parte mais importante do motion design".
Trocar só o ease muda toda a personalidade. **Regra base: `power1.out`/`power2.out` para
entradas de UI/texto** (rápido no início = responsivo; desacelera no fim = atrito natural).

## Eases nativos do GSAP
`none power1 power2 power3 power4 back bounce circ elastic expo sine steps` — cada um em
`.in` / `.out` / `.inOut`. Uso: `ease: "power2.out"`, `ease: "back.out(2)"`.
- **back** = overshoot (pop). Ex.: `back.out(1.7)` número/badge surgindo.
- **elastic** = mola. Energia/brincalhão. `elastic.out(1, 0.4)`.
- **bounce** = quica. Lúdico.
- **expo.out** = entrada muito rápida que freia forte (premium/snappy).

## Eases cinematográficos (CustomEase) — registrar uma vez
```js
gsap.registerPlugin(CustomEase);
CustomEase.create("cinematicSilk",   "0.45,0.05,0.55,0.95"); // suave, equilibrado
CustomEase.create("cinematicSmooth", "0.25,0.1,0.25,1");     // entrada/saída clássica
CustomEase.create("cinematicFlow",   "0.33,0,0.2,1");        // flui, desacelera elegante
CustomEase.create("cinematicLinear", "0.4,0,0.6,1");         // quase linear, controlado
```
Pequenas variações de aceleração mudam dramaticamente o ritmo visual. Use estes para
push-in lento, parallax e reveals premium.

## Mapa rápido (ease por intenção)
| Intenção | Ease |
|---|---|
| Entrada de texto/UI | `power2.out` |
| Pop de número/ícone (punch) | `back.out(2)` |
| Push-in / câmera lenta | `cinematicSmooth` / `power1.inOut` |
| Parallax / drift | `cinematicSilk` / `sine.inOut` |
| Whip-pan / impacto | `expo.in` (saída) + `expo.out` (entrada) |
| Energia/viral | `back.out(2.5)` ou `elastic.out` |
| Saída/fade cinematográfico | `power2.in` |

## Tempo (time-driven, não scroll)
Nosso render é por tempo. Onde a pesquisa usa `ScrollTrigger.onUpdate`, nós dirigimos o
mesmo valor 0→1 pela **timeline GSAP** no tempo do beat. Padrão: uma var `--progress`
movida por `gsap.to(obj,{p:1, ease:"cinematicSmooth"})` e aplicada a `scale/translate`
(ver `recipes.md`).
