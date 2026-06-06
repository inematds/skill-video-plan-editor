# Skill `video-plan-editor` — Pesquisa profunda + proposta de design

> Objetivo: uma skill que, a partir de **prompt do usuário + contexto**, gere um
> **plano de edição de vídeo** (dados estruturados) e o execute via **FFmpeg /
> HyperFrames / Remotion** e outras ferramentas CLI — automação de vídeo inteligente.
> Referência citada: https://demo.reactvideoeditor.com/ (web editor React + Remotion).

Pesquisa: 6 ângulos · 27 fontes · 135 claims → **25 verificados (voto 3-0) · 0 refutados**.

---

## 1. Mapa de ferramentas (o que faz o quê)

| Camada | Ferramenta | Papel | Modelo de "plano" | Status local |
|---|---|---|---|---|
| **Corte por análise** | **Auto-Editor** (CLI) | Corta silêncio/movimento automaticamente; `--edit audio:-19dB`, composição booleana `(or audio motion)` | **Exporta EDL/XML** p/ Premiere, Resolve, Final Cut, ShotCut, Kdenlive (`--export ...`) — não só renderiza | instalar (`pip`) |
| **Edição programática** | **MoviePy** (Python, FFmpeg) | Load→modify→compose→write; frames como Numpy; cortes, títulos, legendas, efeitos custom | API imperativa Python | instalar (`pip`) |
| **Render declarativo** | **Remotion** (React/TS) | Edit plan = **array de Tracks com Items tipados** `{from,durationInFrames,id}`; mesmo dado serve preview (`<Player>`) e render (`renderMedia`/CLI/Lambda). Aceita `--props` JSON | **Plano = JSON de Tracks/Items** | opcional |
| **Render canvas** | **Motion Canvas** | API imperativa, 1 `<canvas>`, render no browser | timeline procedural | opcional |
| **Schema de timeline** | **OpenTimelineIO (OTIO)** | Formato JSON **vendor-neutral** `.otio`: `Timeline > Stack > Track > Clip/Gap/Transition`; tempo rate-aware `RationalTime(value,rate)` | **Interchange JSON canônico** | opcional |
| **HTML→MP4** | **HyperFrames** v0.6.79 (já instalado) | Chrome headless + FFmpeg; `capture`, `transcribe` (timestamps/palavra), `tts` Kokoro, `remove-background`, `render`, `cloud`/`lambda` | composições HTML+GSAP | **já em uso** |
| **Orquestração IA** | **mcp-video** (KyaniteLabs, Apache-2.0, push 2026-06-04) | MCP server + lib Python + CLI envolvendo **FFmpeg + HyperFrames 0.5**; **119 tools**; **preflight guardrails** antes de qualquer FFmpeg; **edit-plan/pipeline ordenado** (`trim→add_text→normalize_audio→resize→export`) | **pipeline ordenado de ops** | avaliar/clonar |

### Arquitetura prompt→plano (referência acadêmica)
**LAVE** (ACM IUI 2024, arXiv:2402.10294): padrão canônico = (1) auto-legendar footage
em descrições em linguagem natural → (2) **agente LLM plan-and-execute** interpreta o
objetivo livre e planeja+executa ações (geração de ideia, sumarização, retrieval
semântico, storyboard/sequenciamento, trim). *Caveat: protótipo de pesquisa, n=8.*

---

## 2. Decisão de arquitetura (recomendação)

A pesquisa converge numa receita clara:

1. **Representar o plano como dado tipado e serializável em JSON** (estilo Remotion
   Tracks/Items **ou** OTIO) — nunca o LLM cuspindo comando FFmpeg cru.
2. **Gerar o plano a partir do prompt** via agente LLM plan-and-execute (LAVE).
3. **Preflight/guardrails ANTES de executar FFmpeg** (limites de filtro,
   compatibilidade de merge, mix de áudio, opacidade de overlay/chroma, timing/overflow
   de texto animado) — exatamente o que o mcp-video faz.
4. **Executar**: render direto (HyperFrames/Remotion/MoviePy) **ou** exportar EDL/OTIO
   p/ um NLE.

### Por que isso encaixa no teu setup
- HyperFrames já é teu render engine de fato; **mcp-video já o envolve** + FFmpeg +
  guardrails → forte candidato a base (clonar/estudar em vez de reinventar 119 tools).
- Auto-Editor cobre o caso "corta o silêncio/partes mortas do footage real" que tuas
  skills atuais (geram do zero) não cobrem.
- Remotion/OTIO dão o **schema do plano**; reactvideoeditor.com (a referência) é
  React + Remotion → o modelo Tracks/Items é o mais alinhado à referência.

---

## 3. Esboço da skill `video-plan-editor`

**Entrada:** prompt em linguagem natural + contexto (footage existente? assets? objetivo
— corte de silêncio / legendar / montar a partir de clipes / motion graphics do zero?).

**Saída:** `edit-plan.json` (schema tipado) + execução opcional.

Fluxo proposto:
1. **Inspect/Index** — `ffprobe` + (se houver footage) `hyperframes transcribe` p/
   timestamps; opcional auto-caption (estilo LAVE) p/ retrieval semântico.
2. **Plan** — LLM emite `edit-plan.json` (Tracks/Items + ops ordenadas). Schema fixo.
3. **Preflight** — validador determinístico (bounds, compat, timing) → falha cedo, sem
   FFmpeg.
4. **Execute** — roteia cada op p/ a ferramenta certa: Auto-Editor (corte), FFmpeg
   (concat/trim/overlay), HyperFrames (HTML/motion/CTA), MoviePy (efeito custom),
   Remotion (timeline data-driven).
5. **Verify** — extrai frames/ffprobe, mostra ao usuário (padrão das tuas skills).

---

## 4. Perguntas em aberto (decisões antes de construir)

- **Caso de uso primário** da skill: cortar/montar **footage real existente** (corte de
  silêncio, highlights, supercuts) **ou** orquestrar geração+edição (motion graphics +
  clipes) **ou** os dois?
- **Schema do plano**: Tracks/Items estilo Remotion (alinhado à referência), OTIO
  (`.otio` interoperável com NLEs), ou pipeline ordenado estilo mcp-video?
- **Base**: partir do **mcp-video** (clonar/estudar — já tem FFmpeg+HyperFrames+119 tools
  +guardrails) ou skill enxuta nova só com FFmpeg+Auto-Editor+HyperFrames?
- **Render engine alvo**: manter HyperFrames como principal (teu padrão) e usar
  Remotion/MoviePy só quando o plano pedir?
- **Idioma/identidade**: manter PT-BR + dark premium âmbar + CTA INEMA.CLUB como nas
  outras skills?

## 5. Caveats da pesquisa
- HyperFrames como ferramenta standalone e os internos do demo.reactvideoeditor.com **não
  foram verificados** por fonte web (HyperFrames só aparece como backend do mcp-video e
  nas tuas próprias skills). Conhecimento de HyperFrames aqui vem do setup local.
- mcp-video é repo pequeno (~33 stars), README auto-descritivo; contagem "119 tools" é do
  próprio maintainer; nem todos os 6 guardrails foram confirmados no código.
- Contagens/versões/Lambda são sensíveis ao tempo — reconferir antes de depender.
