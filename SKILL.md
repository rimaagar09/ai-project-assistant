---
name: capillary-brd
description: >
  Use this skill to create a Business Requirements Document (BRD) in Capillary Standard Format
  for any Capillary loyalty platform implementation. Trigger whenever the user mentions Capillary,
  Loyalty+, Campaign Manager, Rewards+, Engage+, CDP, or any Capillary module implementation.
  Also trigger when the user asks to create a BRD for loyalty programs, loyalty implementations,
  points programs, rewards catalogues, campaign management, CRM projects, mobile app loyalty,
  or POS integrations involving the Capillary platform. Trigger for phrases like "Capillary BRD",
  "loyalty BRD", "create BRD for Capillary project", "document Capillary requirements",
  "BRD for loyalty implementation", or "standard Capillary format". Always use this skill —
  not the generic brd-creator — when the project involves any Capillary module or loyalty
  platform implementation. Outputs a polished .docx and .pdf in Capillary Standard BRD Format,
  including a mandatory visual Member Journey Flow diagram after the Risk section.
---

# Capillary Standard BRD Creator

Produces a structured, implementation-ready Business Requirements Document in Capillary Standard
Format — suitable for Loyalty+, Campaign Manager, Rewards+, Engage+, CDP, API, and Mobile App
implementations.

**Every BRD includes TWO mandatory diagrams:**
1. **Loyalty Process Flow** (Mermaid → PNG, after Scope section) — enrollment, earning, validation, voucher, tier, failure states
2. **End-to-End Member Journey Flow** (PNG via Pillow, after Risk section) — 5-stage horizontal lifecycle

## Before You Start

Read the docx skill first: `/mnt/skills/public/docx/SKILL.md`

---

## Step 1 — Gather Project Information

| Field | Required? |
|-------|-----------|
| Client / Brand name | Yes |
| Project name | Yes |
| Capillary modules in scope | Yes — see `references/capillary-modules.md` |
| Business problem / opportunity | Yes |
| Business objectives (revenue, engagement, retention) | Yes |
| Current state / pain points | Yes |
| Key stakeholders (client + Capillary team) | Optional |
| Known integrations (POS, mobile, e-commerce, LINE, etc.) | Optional |
| Phased delivery? | Optional |
| Target go-live / timeline | Optional |
| Commercial / effort details | Optional |

---

## Step 2 — Identify Modules

Read `references/capillary-modules.md` for full module catalogue.

---

## Step 3 — Generate Diagram 1: Loyalty Process Flow (MANDATORY)

**Always generate BEFORE building the document.**
Draw the flowchart programmatically as a PNG using Python + Pillow.

The diagram MUST include all of:
- New member enrollment path vs existing member path
- Transaction processing
- Points eligibility decision (Yes → Credit / No → Skip)
- Tier upgrade eligibility check
- Voucher trigger check and issuance
- Notification step
- Final state (Process Complete)

**Shape conventions:**
- Pill/stadium `([...])` → Start / End states (navy fill)
- Diamond `{...}` → Decision nodes (light gray, dark border)
- Rectangle `[...]` → Process steps (light gray fill)
- Yes/No labels on decision arrows

**Mermaid source (always include in document as a code block too):**
```
graph TD
    Start([Customer Visit]) --> CheckMember{Member Exists?}
    CheckMember -- No --> Register[New Member Enrollment]
    CheckMember -- Yes --> Fetch[Fetch Member Profile]
    Register --> Fetch
    Fetch --> Transaction[Transaction Happens]
    Transaction --> Earning{Eligible for Points?}
    Earning -- Yes --> Credit[Credit Points]
    Earning -- No --> Skip[No Points Awarded]
    Credit --> TierCheck{Tier Upgrade Eligible?}
    TierCheck -- Yes --> UpgradeTier[Upgrade Member Tier]
    TierCheck -- No --> VoucherCheck{Voucher Trigger?}
    UpgradeTier --> VoucherCheck
    VoucherCheck -- Yes --> IssueVoucher[Issue Voucher via Engage+]
    VoucherCheck -- No --> End([Process Complete])
    IssueVoucher --> Notify[Send Notification]
    Notify --> End
    Skip --> End
```

See `references/gen_loyalty_flow_template.py` for the complete working Pillow script.
Read `references/capillary-brd-sections.md` Section 7 for node description table and full drawing guidance.

---

## Step 4 — Generate Diagram 2: Member Journey Flow (MANDATORY)

**5-stage horizontal PNG using Python + Pillow.**

Stages: ① ONBOARD `#2E5496` → ② EARN `#1F6B75` → ③ DISCOVER `#4A235A` → ④ REDEEM `#7B3F00` → ⑤ RETAIN `#1E6B3C`

See `references/gen_flow_diagram_template.py` for the complete generation script.
See `references/capillary-brd-sections.md` Section 14 for embedding instructions.

**Always verify both images render correctly** using the `view` tool before embedding.

---

## Step 5 — Build the BRD (20 Sections)

Read `references/capillary-brd-sections.md` for all section content guidance.
Read `references/capillary-fr-examples.md` for example requirements per module.

### Complete Section Order

```
1.  Document Control
2.  Executive Summary
3.  Business Objectives
4.  Current State Analysis (As-Is)
5.  Proposed Solution (To-Be)
6.  Scope Definition (In Scope / Out of Scope)
── [DIAGRAM 1 — always here] ────────────────────────────────────────────────
7.  Loyalty Process Flow Diagram  ← Mermaid flowchart rendered as PNG
─────────────────────────────────────────────────────────────────────────────
8.  Functional Requirements       ← 6-column table: Req ID|Module|Desc|Logic|Priority|Dependency
9.  Non-Functional Requirements
10. Data Requirements             ← Member fields, Transaction fields, API payloads, Reports
11. Integration Requirements      ← POS→Capillary, Capillary→CRM, →Martech, Webhooks, API endpoints
12. Dependencies
13. Risks & Mitigation
── [DIAGRAM 2 — always here] ────────────────────────────────────────────────
14. End-to-End Member Journey Flow  ← 5-stage PNG (Pillow)
─────────────────────────────────────────────────────────────────────────────
15. KPIs & Success Metrics
16. Assumptions
17. UAT & Sign-Off Criteria       ← UAT scenarios table, acceptance checklist, sign-off process
18. Commercial Considerations
19. Clarification Register
20. Appendix
```

---

## Step 6 — Document Format (Capillary Standard)

Read `references/capillary-brd-format.md` for full visual specification.

**Key rules:**
- Font: **Calibri** throughout
- Primary color: Navy `#1F3864`
- Section headings: Bold, navy, **underlined** — white background, no colored fills
- Section numbers: Plain integers `1`, `2`, `3`
- Table headers: Light gray `#F2F2F2`, navy bold text
- Bullets: `∙` dot inline character
- Requirements table: 6-column format
- Footer: `Capillary Technologies | [Client] | Confidential  Page N`
- End with `--- XXXX --- XXXX ---`

---

## Step 7 — Generate Output

```bash
node build_brd.js
python /mnt/skills/public/docx/scripts/office/validate.py output.docx
python /mnt/skills/public/docx/scripts/office/soffice.py --headless --convert-to pdf output.docx
cp output.docx /mnt/user-data/outputs/[Client]_[Project]_BRD.docx
cp output.pdf  /mnt/user-data/outputs/[Client]_[Project]_BRD.pdf
```

Use `present_files` to share both.

---

## Quality Checklist

- [ ] Loyalty Process Flow diagram (PNG) generated and verified — includes all 8 node types
- [ ] Member Journey Flow diagram (PNG) generated and verified — 5 stages visible
- [ ] Both diagrams embedded in correct sections (7 and 14)
- [ ] All 20 sections present
- [ ] FR table uses 6-column format with FR-xxx IDs
- [ ] Data Requirements has all 4 sub-sections (member fields, transaction fields, API payloads, reports)
- [ ] Integration section covers POS→Capillary, →CRM, →Martech, webhooks, API endpoints
- [ ] Dependencies table complete
- [ ] UAT scenarios table with ≥ 10 scenarios
- [ ] Assumptions list present
- [ ] Risk register complete
- [ ] File passes docx validation
- [ ] PDF generated

---

## Reference Files

| File | When to Read |
|------|-------------|
| `references/capillary-modules.md` | Module catalogue — read when identifying scope |
| `references/capillary-brd-sections.md` | Full content + diagram guidance for all 20 sections |
| `references/capillary-fr-examples.md` | Example requirements per Capillary module |
| `references/capillary-brd-format.md` | Visual/format spec and docx-js code patterns |
| `references/gen_loyalty_flow_template.py` | Pillow script for Loyalty Process Flow PNG (Diagram 1) |
| `references/gen_flow_diagram_template.py` | Pillow script for Member Journey Flow PNG (Diagram 2) |

Read relevant files **before writing any code**.
