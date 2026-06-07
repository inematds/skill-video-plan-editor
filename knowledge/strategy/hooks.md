# Strategy — Ganchos e retenção

## A regra dos 3 segundos
Nenhum vídeo de sucesso começa devagar. Nos primeiros frames: **movimento**, **pergunta
provocativa** ou **imagem inesperada/chocante**. O gancho deve fazer uma de três coisas:
- ser **visualmente inesperado** (quebra de padrão visual);
- fazer uma **pergunta provocativa**;
- prometer uma **recompensa clara**.

Fórmula matadora: **"Como [resultado desejado] sem [dor principal]"**.

## 3 tipos de gancho (gerar sempre as 3 opções)
A skill propõe 3 variações de gancho para os primeiros 3s:
1. **Curiosidade** — abre um loop ("O segredo que ninguém te conta sobre X…").
2. **Contraste / choque** — quebra expectativa ("Você está fazendo X totalmente errado").
3. **Benefício direto** — promessa clara ("Como dobrar Y em Z dias").

## Pattern Interrupt (quebra de padrão)
Mudar **cenário, ângulo de câmera ou elemento na tela a cada 3–5s** para manter o cérebro
engajado e evitar monotonia. Em motion graphics isso = trocar archetype/câmera/cor a cada
beat (ver `camera/vocabulary.md`).

## Loops narrativos
Abrir uma curiosidade no início que só é respondida no fim ("no final eu te mostro o
erro nº1"). Mantém o espectador até o fim. Pode haver micro-loops a cada seção.

## Compartilhamento (por que as pessoas compartilham)
- **Sinalização de identidade** — compartilham o que reflete quem elas são.
- **Emoção de alta excitação** — humor, admiração, raiva, inspiração. (Emoções de baixa
  excitação, como tristeza calma, compartilham menos.)

## Como vira plano
`EditPlan.intent.hook_variants[]` recebe as 3 opções. O beat de abertura usa a escolhida.
`pacing` define a cadência de pattern interrupt (ver `pacing.md`). Loops viram anotações
nos beats (`open_loop` / `close_loop`).
