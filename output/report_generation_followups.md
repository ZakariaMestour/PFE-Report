# Report Generation Follow-ups

This file tracks items to revisit before the final report polish. It is intentionally kept outside the chapter files so we can continue writing without losing corrections, screenshot needs, or diagram-quality notes.

## Standing Instructions

- When a real platform screenshot is needed, insert a visible placeholder using the format `[Insert ...]`.
- Generated diagrams can support explanation, but they should not replace real screenshots when the report needs to show the actual platform UI, Swagger screen, code execution, dashboard, wizard, or validation output.
- UML diagrams must follow formal UML expectations when the diagram is intended as UML:
  - class diagrams must show class names, attributes, methods where relevant, visibility when useful, associations, multiplicities, inheritance, and composition/aggregation when applicable;
  - sequence diagrams must show actors/participants, lifelines, activation bars when useful, synchronous/asynchronous messages, returns, and conditional fragments where needed;
  - activity diagrams must show initial/final nodes, actions, decisions, guards, forks/joins when relevant, and clear flow direction;
  - state-machine diagrams must show initial/final states, named states, transition labels, guards/actions where relevant, and valid branching.

## Screenshot Placeholders To Add

These are candidates for real platform screenshots to insert later.

- Chapter IV: `[Insert screenshot of the SCF dashboard with role-based sidebar]`
- Chapter IV: `[Insert screenshot of the Master Setup tabs]`
- Chapter IV: `[Insert screenshot of the Program Configuration wizard]`
- Chapter IV: `[Insert screenshot of Counterparty Onboarding table and actions]`
- Chapter IV: `[Insert screenshot of Invoice Upload validation table]`
- Chapter IV: `[Insert screenshot of Finance Disbursement wizard]`
- Chapter IV: `[Insert screenshot of Transaction Inquiry filters and results]`
- Chapter V: `[Insert screenshot of the Disbursement Module prototype or implemented screen]`
- Chapter V: `[Insert screenshot of Disbursement API Swagger endpoints]`
- Chapter V: `[Insert backend controller, service, mapper, repository, and migration details once finalized]`
- Chapter VI: `[Insert screenshot or export of Jira sprint/ticket summary if available]`
- Chapter VI: `[Insert quantitative summary: number of Jira tickets, pull requests, bug fixes, modules touched, and lines of code if available]`

## Diagram Review Queue

These diagrams already exist and should be reviewed before final submission.

- Chapter I diagrams are conceptual workflow diagrams, not UML. No formal UML correction required unless the supervisor asks for UML-only visuals.
- Chapter II diagrams are architecture and flow diagrams, not UML. They are acceptable as technical structural diagrams.
- Chapter III `ch3_core_data_model` should be upgraded or supplemented with a formal UML class diagram if the final chapter requires an entity/class diagram.
- Chapter III `ch3_maker_checker_state` should be upgraded to a formal UML state-machine diagram with initial/final nodes and transition labels if presented explicitly as UML.
- Chapter III `ch3_program_configuration_flow` should be upgraded to a UML activity diagram if the final report labels it as an activity diagram.
- Chapter IV diagrams are UI/component flow diagrams. They should be complemented with real screenshots, especially for user-facing modules.

## Chapter V Data Gaps

The Disbursement Module chapter will likely need placeholders unless more implementation details are added.

- `[Insert functional requirements validated by the Product Owner]`
- `[Insert Disbursement Module data model once finalized]`
- `[Insert Disbursement API endpoints once finalized]`
- Generated a target UML sequence diagram for disbursement submission, but it must be checked against the final backend contract once the module is natively integrated.
- `[Insert testing evidence or validation screenshots]`

## Final Polish Tasks

- Replace all `[Insert ...]` placeholders with screenshots, figures, or validated project details.
- Verify Chapter VI quantitative evidence in Jira and Bitbucket: 12 SCF-service tickets, 8 FDL tickets, backend plus front-end parts, and reported pull request count `19 + 12 + 8 + 1 = 40`.
- Decide which generated diagrams remain conceptual and which must be formal UML.
- Re-run LaTeX compilation once a TeX engine is installed or available in PATH.
- Check figure numbering, table numbering, and cross-references after compilation.
- Review all chapters for institution-specific formatting requirements before final export.
