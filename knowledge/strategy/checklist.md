# Strategy — Checklist de produção

Rodar antes de finalizar o plano (e antes de publicar o vídeo).

## Antes de aprovar o plano
- [ ] O gancho prende nos primeiros **3 segundos**?
- [ ] Há **3 variantes de gancho** (curiosidade / contraste / benefício)?
- [ ] O vídeo resolve uma **dor** ou entrega um **desejo** claro?
- [ ] A emoção dominante está definida (Facts / Feelings / Fun)?
- [ ] ~**70%** é valor puro, sem enrolação?
- [ ] Há **quebra de padrão a cada 3–5s** (corte, zoom, texto, troca de câmera)?
- [ ] Existe ao menos um **loop narrativo** aberto cedo e fechado no fim?
- [ ] A **CTA é única e inconfundível**?
- [ ] O **ritmo** está acelerado, sem "respiros" desnecessários?
- [ ] Cada beat tem **camera + archetype + (prompt|motion recipe)** definidos?

## Antes de renderizar
- [ ] Áudio (narração) claro; durações medidas com `ffprobe` (timing = fonte única).
- [ ] Legendas dinâmicas: 1–3 palavras por vez, sincronizadas (ver `pacing.md`).
- [ ] Composição com profundidade (foreground/mid/background) quando aplicável.
- [ ] Efeitos têm **propósito narrativo** (não decorativos).
- [ ] Identidade consistente (`tokens.md`): paleta, fontes, accent.
- [ ] `vpe validate` sem `[error]`.

## Antes de publicar
- [ ] Frames conferidos pelo usuário (não há áudio audível no ambiente — validar locução).
- [ ] Aspect correto para a plataforma (9:16 Reels/TikTok, 16:9 YouTube).
- [ ] CTA final presente (INEMA.CLUB quando aplicável).
