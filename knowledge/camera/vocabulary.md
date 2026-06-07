# Camera — Vocabulário de movimento (a PONTE)

A mesma linguagem de câmera serve aos dois caminhos: vira **prompt** para gerar imagem/
vídeo (flux2-klein / Sora-Veo) **e** vira **parâmetro de motion graphics** (GSAP/CSS).
Todo beat do `EditPlan` recebe um campo `camera` escolhido daqui.

## Movimentos básicos
| Movimento | Efeito emocional | Uso | Frase p/ prompt | Motion graphics (GSAP/CSS) |
|---|---|---|---|---|
| **Push-in** (dolly in) | tensão, aproximação, intimidade | revelar detalhe, hook | "slow push in, 2s, ending close-up" | `scale`/`translateZ` crescendo, ease `cinematicSmooth` |
| **Pull-back** | revelação, contexto | mostrar o todo | "slow pull back revealing the room" | `scale` 1→0.8 + reveal de camadas |
| **Orbit** | poder, admiração | apresentar produto/herói | "360° orbit around subject" | `rotateY` em `transform-style:preserve-3d` |
| **Crane up** | grandiosidade, esperança | finais épicos | "crane up, arc rising" | `translateY` + `rotateX` leve |
| **Dolly lateral** | fluidez, transição | seguir ação | "lateral dolly tracking" | `translateX` constante (linear/`sine`) |
| **Whip-pan** | choque, transição | corte dinâmico entre cenas | "fast whip pan to next scene" | `x` rápido + `filter:blur` momentâneo (motion blur) |
| **Tracking shot** | imersão, ação | seguir personagem | "tracking shot following subject" | sujeito fixo + fundo em parallax |
| **Zoom in** (lente) | foco, isolamento | destacar detalhe | "punch zoom on detail" | `scale` rápido com `back.out` (punch) |
| **Dutch angle** | desconforto, tensão | drama/ação | "dutch angle, tilted frame" | `rotate` 3–8° |
| **Handheld** | urgência, realismo | caos/documentário | "controlled handheld shake" | micro `x/y/rotate` random suave (idle) |

## Combinações avançadas
- **Compression zoom (dolly zoom / Hitchcock):** afasta a câmera enquanto a lente faz zoom — sujeito mantém tamanho, fundo distorce. Prompt: "dolly zoom, vertigo effect". MG: sujeito `scale` constante + fundo `scale`/`perspective` em sentido oposto.
- **Accelerating orbit:** órbita lenta→rápida, fundo borra, sujeito nítido. MG: `rotateY` com ease `power3.in` + `filter:blur` no fundo.
- **Floating descent:** descida lentíssima, onírica, sem tremor. MG: `translateY` longo com `cinematicSilk`, sem idle shake.

## Profundidade (sempre que possível)
Compor em **3 planos**: foreground / midground / background, com **DOF raso** (sujeito
nítido, fundo em bokeh). Prompt: "shallow depth of field, f/2.8, background bokeh". MG:
camadas separadas + `filter:blur()` no bg + parallax (cada plano move em velocidade
diferente). Ver `motion/recipes.md` → *parallax* e *dof*.

## Regra de ouro
Cada movimento tem uma **razão emocional** — nunca mexer a câmera por mexer. Sincronizar o
movimento com a batida/locução (ver `pacing.md`). Pattern interrupt = trocar de câmera a
cada 3–5s.
