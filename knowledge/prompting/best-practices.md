# Prompting — Boas práticas, checklist e erros

## Técnicas avançadas
1. **Timing exato** — não "câmera rápida"; sim "push-in em 2s, de 3m até close-up".
2. **Movimento + ação juntos** — não "pessoa correndo"; sim "pessoa correndo enquanto tracking lateral a mantém em frame, movimento sincronizado".
3. **Referência cinematográfica** — "estilo câmera anos 80, handheld controlado, cortes secos".
4. **Profundidade de campo** — "DOF raso (f/2.8), sujeito nítido, fundo em bokeh".
5. **Sincronizar com áudio** — "push-in sincronizado com a batida, acelerando conforme o som cresce".

## Checklist antes de gerar
- [ ] Movimento de câmera é específico?
- [ ] Timing definido em segundos?
- [ ] Transições descritas?
- [ ] Iluminação cinematográfica?
- [ ] Áudio sincronizado?
- [ ] Múltiplos planos (fg/mid/bg)?
- [ ] Efeitos têm propósito narrativo?
- [ ] Ritmo acelerado (sem "respiros")?
- [ ] Composição profissional (DOF, ângulos)?
- [ ] Resultado claro (não estático)?

## Erros comuns
| ❌ Vago | ✅ Específico |
|---|---|
| "vídeo cinematográfico com câmera dinâmica" | "slow push-in seguido de orbit 360°" |
| "pessoa dança com música" | "dança sincronizada com a batida, handheld segue o movimento" |
| "pessoa em frente a parede" | "close (fg), parede desfocada (bg), push-in revela detalhe" |
| "corta pra próxima cena" | "whip-pan rápido, sincronizado com a batida" |
| "vídeo rápido" | "5 cortes em 3s, cada corte 0.6s" |

## Nota para flux2-klein (still)
flux2-klein gera **imagem**, não vídeo. Então: descreva a composição, luz, DOF e
acabamento (grão/LUT) — **omita verbos de movimento**. O push-in/parallax/whip são
aplicados depois sobre a still pelas recipes de `motion/`.
