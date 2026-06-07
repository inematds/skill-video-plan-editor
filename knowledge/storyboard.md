# Storyboard — direção de cena dinâmica (absorvido do MDD)

Disciplina de direção para qualquer beat que vire **footage/clipe generativo**
(`render_kind: generated_clip` / `generated_still`) ou para dar arco a uma sequência.
Absorvido da skill **mestre-direcao-dinamica (MDD)**. Não é descrever "alguém usando X";
é dirigir uma **cena com movimento, intenção e continuidade**.

## A fórmula central
Antes de gerar qualquer plano, ache o **conflito visual** — sem conflito o vídeo fica
parado:

> **Assunto → conflito visual → progressão → virada → impacto suspenso.**

Conflito por domínio (escolha o motor da cena):
- Produto: problema vs solução · Imóvel: espaço comum vs experiência desejada
- Evento: expectativa vs ápice · IA/tech: tela vazia vs revelação
- Educação: dúvida vs clareza · Marca: invisibilidade vs autoridade
- Esporte: pressão vs superação · Institucional: problema vs visão de futuro

Transforme em beats: **estado inicial (lado fraco) → progressão → virada → estado final
(lado forte) → impacto suspenso (freeze)**.

## Regra de ouro de cada tomada
> **Câmera + ação + continuidade + emoção + efeito permitido.**

Tomada vaga ("mostre alguém usando IA") é fraca. Tomada dirigida ("push-in lento sobre o
monitor, 50mm, a interface ganha camadas, mesma luz lateral, sensação de descoberta")
carrega o vídeo. Casar movimento com a **função** do beat (ver `camera/vocabulary.md`):
- Abertura/estabelecer → top shot, dolly lateral, push-in lento
- Tensão/expectativa → push-in lento, rack focus
- Revelação/virada → crash zoom, orbit, rack focus
- Detalhe de valor → macro close-up · Imersão → POV
- Fechamento → **freeze impact**, push-in final, orbit terminando no objeto

## Princípios não-negociáveis
1. **Continuidade é sagrada** — mesma roupa, mesma luz, mesmo ambiente entre planos, salvo
   quando a virada exige mudança. Liste o que NÃO muda.
2. **Cada tomada tem função** — se um plano não move a história, corte ou troque.
3. **Câmera muda com intenção** — não repetir o mesmo movimento em planos vizinhos sem motivo.
4. **Efeito precisa de motivo** físico ou narrativo — sem holograma/UI falsa gratuita.
5. **Termine com imagem forte** (freeze/reveal/push-in final) — não dissolvendo a ação.
6. **A chamada/CTA não vai no prompt de vídeo** — IA escrevendo texto sai errado; a CTA
   (INEMA.CLUB) entra na edição, fora da geração.

## Estrutura do beat dirigido (campos)
Cada beat generativo carrega: `camera` (movimento+lente), `action` (o que progride),
`continuity` (o que se mantém), `effect` (permitido), `emotion` (intenção). No `EditPlan`,
isso vira `camera` + `gen_prompt` (expandido via `prompting/`), com a continuidade anotada.

## Sequências de planos prontas (8 painéis — esqueletos, adapte)
- **IA/tech:** monitor vazio → mão digita prompt → dados entrando → imagem gerada →
  timeline → câmera virtual → laurels → reveal final.
- **Produto:** problema → produto na sombra → close de textura → uso em ação →
  antes/depois → detalhe técnico → pessoa satisfeita → fechamento.
- **História/autoridade:** close no rosto → símbolo → ambiente → memória/tensão → virada →
  resolução no rosto → plano aberto de fechamento (freeze).

Para conteúdo listável (ex.: "12 lições"), use UM personagem e um arco
**invisibilidade→autoridade**; cada lição = um beat-metáfora físico, não um card de texto.

## Checklist (rodar antes de gerar clipes)
- [ ] Tem começo, meio e fim claros?  - [ ] Cada tomada tem função?
- [ ] A câmera muda com intenção (sem repetir à toa)?  - [ ] Personagem/produto consistente?
- [ ] Ambiente legível?  - [ ] Efeitos têm motivo?  - [ ] Fecha com imagem forte?
- [ ] Prompt negativo bloqueia invenções?  - [ ] CTA ficou FORA do prompt de vídeo?

> Para o pacote completo de direção (storyboard painel-a-painel + prompt final + negativo),
> a skill `mestre-direcao-dinamica` é o motor de referência — `video-plan-editor` a delega
> nos beats `generated_clip`/`generated_still`.
