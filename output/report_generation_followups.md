# Report Generation Follow-ups

This file tracks items to revisit before the final report polish. It is intentionally kept outside the chapter files so we can continue writing without losing corrections, screenshot needs, or diagram-quality notes.

## Standing Instructions

- When a real platform screenshot is needed, insert a visible placeholder using the format `[Insert ...]`.
- Generated diagrams can support explanation, but they should not replace real screenshots when the report needs to show the actual platform UI, Swagger screen, code execution, dashboard, wizard, or validation output.
- The generated diagrams were redesigned in a professional pass. Keep later diagram changes precise: formal UML when the caption says UML, clean relationship routing, no text overflow, and no arrows passing through entity compartments.
- UML diagrams must follow formal UML expectations when the diagram is intended as UML:
  - class diagrams must show class names, attributes, methods where relevant, visibility when useful, associations, multiplicities, inheritance, and composition/aggregation when applicable;
  - sequence diagrams must show actors/participants, lifelines, activation bars when useful, synchronous/asynchronous messages, returns, and conditional fragments where needed;
  - activity diagrams must show initial/final nodes, actions, decisions, guards, forks/joins when relevant, and clear flow direction;
  - state-machine diagrams must show initial/final states, named states, transition labels, guards/actions where relevant, and valid branching.

## Screenshot Placeholders To Add

These are candidates for real platform screenshots to insert later.

- Chapter IV: `[Insert screenshot of Counterparty Onboarding table and actions]`
- Chapter IV: `[Insert screenshot of Transaction Inquiry filters and results]`
- Chapter V: `[Insert screenshot of Disbursement API Swagger endpoints]`
- Chapter V: `[Insert backend controller, service, mapper, repository, and migration details once finalized]`
- Chapter V: `[Insert screenshot or export of Jira sprint/ticket summary if available]`
- Chapter V: `[Insert bug-fix examples and Product Owner refinement-session count if available]`

## Diagram Status

The current generated diagrams were rebuilt from `output/images/generate_professional_diagrams.py`. The pass replaced the earlier repetitive card-style diagrams with varied academic diagrams: UML use case diagrams, formal class diagrams with multiplicities, state machines, sequence diagrams, activity diagrams, architecture views, and workflow diagrams.

- Latest UML audit: corrected the Chapter III core data model so `ScfProgramCashflow` is modeled as program-level cashflow configuration, not invoice-level data.
- Latest UML audit: corrected the Chapter V Disbursement use case so the actor initiates `Request finance` only; `Choose mode` is now reached only through `<<include>>`.
- Latest UML audit: rebuilt the Chapter V Disbursement class diagram layout with formal multiplicities and cleaner ledger-dependency routing.
- Latest UML audit: rebuilt the Chapter V Disbursement sequence image with a real `alt` combined fragment and an explicit rejection message for failed eligibility checks.
- Chapter III `ch3_core_data_model` is now a formal class diagram with multiplicities.
- Chapter III `ch3_maker_checker_state` is now a UML state-machine diagram.
- Chapter III `ch3_program_configuration_flow` is now a UML activity diagram.
- Chapter IV includes back-office, middle-office, and front-office use case diagrams.
- Chapter IV `ch4_finance_disbursement_wizard` now matches the actual wizard order: Program/Product, Invoice Selection, Finance Details, Repayment Details, Accounting Entries, Review/Submit.
- Chapter V now includes formal UML diagrams for the Disbursement use case, class model, state machine, and manual sequence with Payment Gateway, HMAC validation, Kafka, and `DisbursementEventConsumer`.

## Completed Diagram Additions

- Use case diagram 1: back office bank-side use cases, including maker/checker creation, approval, rejection, and administration operations.
- Use case diagram 2: middle office use cases, showing monitoring, transaction inquiry, validation, and follow-up responsibilities.
- Use case diagram 3: front office use cases, showing buyer and supplier actions, including invoice actions and request types.
- Use case diagram 4: Disbursement Module use case with buyer/supplier initiation, manual request finance, automatic disbursement, eligibility, payment instruction, and Payment Gateway callback.
- Class diagram 1: main SCF classes with UML multiplicities, including program configuration, product definition, counterparty, bank account, country, city, anchor, program counterparty, and cashflow.
- Class diagram 2: Disbursement domain classes from `input/disbursement-context/CONTEXT.md`, including Program, Invoice, Disbursement, FinanceRecord, FinanceRecordInvoice, and Transaction, with no separate finance-request class.
- State machine diagram: Disbursement lifecycle with initial node, `INITIATED`, `PENDING_CONFIRMATION`, `SUCCESS`, `FAILED`, sync 422 failure, async failed callback, and success callback.
- Sequence diagram: corrected manual disbursement sequence based on the provided context, including frontend, Disbursement service, Payment Gateway, adria-gateway callback endpoint, HMAC validation, Kafka topic `payment.callback`, `DisbursementEventConsumer`, FinanceRecord creation, transaction creation, and invoice update.

## Chapter V Data Gaps

The Disbursement Module chapter now uses `input/disbursement-context/CONTEXT.md` as the main source. Remaining gaps are mostly evidence and final API/code artifacts.

- `[Insert screenshot of Disbursement API Swagger endpoints]`
- `[Insert backend controller, service, mapper, repository, and migration details once finalized]`
- `[Insert testing evidence or validation screenshots]`

## Final Polish Tasks

- Replace all `[Insert ...]` placeholders with screenshots, figures, or validated project details.
- Verify Chapter V quantitative evidence in Jira and Bitbucket using the final calculated totals, not formula fragments or unverified raw counts.
- If time allows, add one extra sequence diagram for an implemented platform flow, preferably Program Configuration maker/checker approval or Invoice Upload validation. The mandatory UML set exists, but an extra implemented-flow sequence would strengthen the conception chapter.
- Review the rebuilt diagrams after supervisor feedback and keep the SVG originals synchronized with PNG outputs.
- Re-run LaTeX compilation after the final screenshot/page-de-garde insertion.
- Check figure numbering, table numbering, and cross-references after the final compilation.
- Review all chapters for institution-specific formatting requirements before final export.
