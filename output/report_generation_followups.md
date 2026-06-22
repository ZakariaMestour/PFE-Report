# Report Generation Follow-ups

This file tracks items to revisit before the final report polish. It is intentionally kept outside the chapter files so we can continue writing without losing corrections, screenshot needs, or diagram-quality notes.

## Standing Instructions

- When a real platform screenshot is needed, insert a visible placeholder using the format `[Insert ...]`.
- Generated diagrams can support explanation, but they should not replace real screenshots when the report needs to show the actual platform UI, Swagger screen, code execution, dashboard, wizard, or validation output.
- The existing generated diagrams should be redesigned later. Current feedback: they look too similar, use the same font and card-like visual idea, and many read like class diagrams without UML multiplicities or proper domain-specific conception.
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
- Chapter VI: `[Insert screenshot or export of Jira sprint/ticket summary if available]`
- Chapter VI: `[Insert bug-fix examples and Product Owner refinement-session count if available]`

## Diagram Review Queue

These diagrams already exist and should be reviewed before final submission.

- Chapter I diagrams are conceptual workflow diagrams, not UML. No formal UML correction required unless the supervisor asks for UML-only visuals.
- Chapter II diagrams are architecture and flow diagrams, not UML. They are acceptable as technical structural diagrams.
- Chapter III `ch3_core_data_model` should be upgraded or supplemented with a formal UML class diagram if the final chapter requires an entity/class diagram.
- Chapter III `ch3_maker_checker_state` should be upgraded to a formal UML state-machine diagram with initial/final nodes and transition labels if presented explicitly as UML.
- Chapter III `ch3_program_configuration_flow` should be upgraded to a UML activity diagram if the final report labels it as an activity diagram.
- Chapter IV diagrams are UI/component flow diagrams. They should be complemented with real screenshots, especially for user-facing modules.
- Chapter IV `ch4_finance_disbursement_wizard` must be corrected to match the actual wizard order: Program/Product, Invoice Selection, Finance Details, Repayment Details, Accounting Entries, Review/Submit.
- Chapter V generated diagrams should be replaced with formal UML diagrams based on `input/disbursement-context/CONTEXT.md`, especially because the previous target sequence does not include Payment Gateway 202, webhook callback, HMAC validation, Kafka, or `DisbursementEventConsumer`.

## Required New Diagrams

- Use case diagram 1: back office bank-side use cases, including maker/checker creation, approval, rejection, and administration operations.
- Use case diagram 2: middle office use cases, showing monitoring, transaction inquiry, validation, and follow-up responsibilities.
- Use case diagram 3: front office use cases, showing buyer and supplier actions, including invoice actions and request types.
- Use case diagram 4: Disbursement Module use case with buyer/supplier initiation, bank-side processing, manual request finance, automatic disbursement, individual mode, clubbed mode, and Payment Gateway interaction.
- Class diagram 1: main SCF classes with UML multiplicities, including Program, Product/Program, Counterparty, Country, City, and related associations.
- Class diagram 2: Disbursement domain classes from `input/disbursement-context/CONTEXT.md`, including Program, Invoice, Disbursement, FinanceRecord, Transaction, any required junction table for clubbed finance records, and no `FinanceRequest`.
- State machine diagram: Disbursement lifecycle with initial node, `INITIATED`, `PENDING_CONFIRMATION`, `SUCCESS`, `FAILED`, sync 422 failure, async failed callback, and success callback.
- Sequence diagram: corrected manual disbursement sequence based on the provided context, including frontend, DisbursementService, Payment Gateway, adria-gateway callback endpoint, HMAC validation, Kafka topic `payment.callback`, `DisbursementEventConsumer`, FinanceRecord creation, transaction creation, and invoice update.

## Chapter V Data Gaps

The Disbursement Module chapter now uses `input/disbursement-context/CONTEXT.md` as the main source. Remaining gaps are mostly evidence and final API/code artifacts.

- `[Insert formal UML use case diagram for the Disbursement Module]`
- `[Insert formal UML class diagram for Disbursement domain with Program, Invoice, Disbursement, FinanceRecord, Transaction, associations, and multiplicities]`
- `[Insert formal UML state machine diagram for Disbursement lifecycle: initial, INITIATED, PENDING_CONFIRMATION, SUCCESS, FAILED, and transition labels]`
- `[Insert corrected UML sequence diagram for manual disbursement with Payment Gateway, 202 Accepted, webhook callback, HMAC validation, Kafka topic payment.callback, and DisbursementEventConsumer]`
- `[Insert screenshot of Disbursement API Swagger endpoints]`
- `[Insert backend controller, service, mapper, repository, and migration details once finalized]`
- `[Insert testing evidence or validation screenshots]`

## Final Polish Tasks

- Replace all `[Insert ...]` placeholders with screenshots, figures, or validated project details.
- Verify Chapter VI quantitative evidence in Jira and Bitbucket: 12 SCF-service tickets, 8 FDL tickets, backend plus front-end parts, and reported pull request count `19 + 12 + 8 + 1 = 40`.
- Decide which generated diagrams remain conceptual and which must be formal UML.
- Re-run LaTeX compilation once a TeX engine is installed or available in PATH.
- Check figure numbering, table numbering, and cross-references after compilation.
- Review all chapters for institution-specific formatting requirements before final export.
