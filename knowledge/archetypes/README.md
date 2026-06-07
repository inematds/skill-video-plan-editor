# Archetypes — Catálogo de cenas

Blocos de cena reutilizáveis (HTML+CSS+GSAP) que a composição combina. Cada archetype é
parametrizado (recebe conteúdo do beat) e usa recipes de `motion/` + linguagem de
`camera/`. A skill escolhe um archetype por beat conforme papel narrativo e emoção.

| Archetype | Quando usar | Camera default | Recipes principais |
|---|---|---|---|
| **cinematic-hero** | hook/abertura premium, capa | slow push-in | grain, push-in, mask-reveal, graded |
| **big-stat** | número/estatística de impacto | punch zoom | count-up, pop, bar-grow |
| **big-type-3d** | frase-bomba editorial | dolly + perspective | char-stagger, 3D tilt |
| **vs / comparação** | antes/depois, X vs Y | dolly lateral | mask-reveal, slide |
| **steps / lista** | passos, lições, processo | pull-back | char-stagger, pop por item |
| **editorial-grid** | grade de itens/imagens | orbit/preserve-3d | parallax, stagger 3D |
| **quote** | citação/declaração | push-in lento | mask-reveal, grain |
| **diagram** | explicar mecanismo | pull-back | bar-grow, draw, stagger |
| **knockout-reveal** | logo/marca revelando imagem | push-in | knockout-text, graded |
| **cta** | fechamento INEMA.CLUB | push-in + glow | pop, wipe-underline |

## Estrutura de um archetype
Cada arquivo `*.md` traz: propósito, parâmetros que recebe do beat, marcação HTML, CSS e o
trecho GSAP (time-driven). Ver `cinematic-hero.md` como referência de implementação.

## Identidade
Todos herdam `tokens.md` (paleta, fontes, accent âmbar) e respeitam os gotchas do
HyperFrames (animar `.scene-inner`, fontes locais, decorativos `data-layout-ignore`).

## Roadmap de archetypes
Implementado como exemplo: **cinematic-hero**. Os demais seguem o mesmo molde — adicionar
conforme os primeiros vídeos exigirem (começar enxuto, expandir).
