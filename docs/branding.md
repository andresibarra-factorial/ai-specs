# Branding — client-facing deliverables

Every document that leaves FDE (feasibility assessment, solution design, SOW, field mapping, presentation) carries the Factorial brand. Source of truth: the **Factorial Brand Book Lite** (brand team, January 2025) and the FDE templates maintained by the Knowledge Base manager (`FDE/Templates`). This page records the subset the harness applies, so generated documents match the hand-made ones.

## 1. Colour

| Name | Hex | Use in documents |
|---|---|---|
| **Radical Red** | `#FF355E` | Main brand colour: table header rows (white text), header band, footer text, callout rule, section labels. Never under large blocks of body text; never associated with negative data. |
| **Midnight** | `#25253D` | Titles and body copy (the Brand Book swatch reads `#1A1A31`; the FDE templates use `#25253D` — keep the template value for consistency). Table borders. |
| Chill Frost | `#FFFFFF` | Main page background. |
| Ice | `#F9F9F9` | Alternative background (social) — not used in documents. |
| Glacier | `#ECECF1` | Complementary background; callout fill is the near variant `#F0F4F9` used by the FDE docx template. |
| Grey text | `#666666` / `#434343` | Secondary text, Heading 3 / 4 per the template; grey italic = author guidance in templates. |
| Product verticals | Radical Red (Talent) · Viridian `#07A2AD` (Finance) · Sunbeam `#FFC155` (Time) · Tangerine `#FF9153` (Core) | Charts and diagrams when a vertical is meant; tints `#E51943 / #FFAEBF / #FFEBEF` (red), `#06838C / #6AC7CE / #CDECEF` (viridian), `#EFA02A / #F9D69B / #FFEBC8` (sunbeam), `#F56819 / #FFBD98 / #FFD7C1` (tangerine). |

Legibility rules from the Brand Book: Midnight only over Chill Frost (never over Radical Red); on Radical Red use white; one-colour logo = light on dark or dark on light, never black elsewhere; no drop shadows on the logo; no logo over photographs unless on a plain white or black area.

## 2. Typography

- **DM Sans** for all print and digital communications. Weights: 400 Regular body copy; 500 Medium third-level titles; 600 Semibold second-level titles; 700 Bold first-level titles and highlighted body copy; 200/300/800/900 display only. Italics only for quotations and foreign words — emphasis is bold.
- **Roboto Mono** for code, paths, identifiers and API resources in documents (the FDE docx template embeds it).
- **Inter** is reserved for the Factorial product UI — never in documents.

## 3. Document conventions (FDE templates)

- **Naming:** `YYYYMMDD_FDE-<DocType>-<IntegrationName>_<ClientName>_Factorial.<ext>` (e.g. `20261006_FDE-Feasibility-Assessment-gsBase_ClientName_Factorial.docx`). ES twin: same name with the Spanish doc type (`documentation-standards.md` §5).
- **Cover:** Factorial logo (first-page header), Title style in Midnight (`<Doc type>: <External System> & Factorial`), one-line subtitle, `Prepared for: <Client>`, then the control table — *Project Objective* / *Technical Context* (Source of Truth · Consumer: Factorial <modules> · Orchestration) / *Document Control* (Version · Status · Date · Confidentiality · Assessed or Designed by · Pinned API version).
- **Running pages:** Radical Red header band with the white logo; footer `Factorial x <External System>` · `Internal/Client Restricted` · `Page n of N` in Radical Red.
- **Body:** A4, numbered Heading 1 / Heading 2 (`1.`, `1.1`), tables with a Radical Red header row and Midnight hairline borders, callout boxes with a Radical Red left rule on a Glacier fill, lists with the template's bullet. Executive summary first; evidence in appendices.
- **Status vocabulary** on covers: `Draft for review` → `In review` → `Approved`; confidentiality `Client Restricted` unless stated otherwise.

## 4. Rendering generated documents

`scripts/render_fde_docx.py <content.md> <out.docx>` renders a harness Markdown file into a Factorial-branded .docx. Its brand source is, by default, the committed **Feasibility Assessment template** `templates/docx/2026MMDD_FDE-Feasibility-Assessment-IntegrationName_ClientName_Factorial.docx` — a complete, Word-usable document rendered from `templates/feasibility-assessment.md`, carrying the FDE styles, embedded DM Sans / Roboto Mono fonts, cover layout, red header band and footer. The renderer keeps only that shell (styles, fonts, numbering, section layout, header, footer) and discards the base's body, so nothing of the base's text leaks into the output; `--base` accepts any other FDE-branded .docx (e.g. the KB manager's Solution Design template) when a different shell is wanted. Rendering is idempotent: re-rendering the template's Markdown on top of the template reproduces it byte for byte, which is how the committed docx is kept in sync with its Markdown (`python3 scripts/render_fde_docx.py templates/feasibility-assessment.md templates/docx/<same name>.docx`). Supported Markdown subset:

| Markdown | Renders as |
|---|---|
| front matter `title`, `subtitle`, `prepared_for`, `external_system`, `confidentiality`, `cover: Label :: line \|\| line` | Cover page (running header/footer placeholders filled from `external_system` / `confidentiality`) |
| `<!-- toc -->` | Table of contents (static entries; refresh with F9 in Word) |
| `# Title`, `## Title`, `### Title` | Numbered Heading 1 / 2, bold run-in Heading 3 |
| `#! Title`, `##! Title` | Unnumbered Heading 1 / 2 (appendices) |
| paragraph with `**bold**`, `_italic_`, `` `mono` `` | Body text |
| `_whole line in italics_` | Author guidance (grey italic — delete before sending) |
| `> **Title.** body` | Callout box |
| `- item`, `1. item` | Bullet / numbered list |
| `\| a \| b \|` + `\|---\|---\|` | Table, first row = header. Optional directive on the line before: `<!-- widths: 500,1500,… size: 16 -->` (DXA widths summing to 8730; body font size in half-points, default 18) |
| `---` | Page break |

Always render, convert to PDF and look at every page before sending; fix wrapping with the widths directive, never by editing the docx by hand (the Markdown is the source — the ES twin and every revision are re-rendered from it).
