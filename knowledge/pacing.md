# Pacing — Ritmo e sincronização

Define a energia temporal por preset/formato. O ritmo é o que separa "slideshow" de
"dinâmico".

## Word-by-word (legendas / kinetic type)
- **1–3 palavras na tela por vez**, sincronizadas à fala.
- **~200–500ms por palavra** (cadência que cria a "puxada rítmica").
- Em vídeo narrado: derivar do áudio (timestamps de `hyperframes transcribe`); fora disso,
  estimar pela contagem de palavras × ~280ms.

## Pattern interrupt
Trocar algo visível (corte, câmera, cor, archetype) **a cada 3–5s**. Em motion graphics =
mudar archetype/câmera entre beats; dentro de um beat longo, um sub-evento (pop/zoom) a
cada ~3s.

## Energia por preset
| Preset | corte médio | câmera | trilha | legenda | aspect |
|---|---|---|---|---|---|
| **viral** | 0.8–1.5s | whip/punch-zoom | alta | karaoke ALL-CAPS | 9:16 |
| **acao** | 1–2s | tracking/whip | alta | karaoke | 9:16 |
| **promo** | 2–3s | orbit/push | média-alta | block | 16:9 / 1:1 |
| **vendas** | 2–4s | push lento + b-roll | média (cresce) | block + CTA | 16:9 / 9:16 |
| **suave** | 4–6s | push-in lento, floating | baixa | minimal | 16:9 |

> Cena narrada ≠ corte de 1s: quando há narração, a **duração da cena segue o áudio**.
> "Viral" então aplica o *look* punchy (vertical, karaoke, câmera enérgica, pattern
> interrupt interno) — não corta a fala no meio. Para ritmo real de jump-cut de 1s, o
> roteiro precisa de narração curta/staccato.

## Sincronização com áudio (regra de ouro)
**Timing é fonte única:** medir durações reais com `ffprobe` e tirar `data-start/duration`
E os tempos dos tweens do MESMO array `AUDIO[]`. Assim áudio e animação nunca desencaixam.
Sincronizar hits visuais (pop, whip, count-up termina) com sílabas tônicas / batidas.

## Curva de energia (arco do vídeo)
- **Hook (0–3s):** energia alta imediata (não começar devagar).
- **Valor (miolo):** ritmo sustentado com pattern interrupt; variar para não cansar.
- **Pico antes do CTA:** acelerar/pausar dramaticamente (contraste).
- **CTA:** claro, respiro mínimo, gesto final + glow.
