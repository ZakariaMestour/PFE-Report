# Eraser AI Diagram Descriptions

Use these prompts to recreate the existing report diagrams in Eraser AI. For all diagrams, use a clean academic enterprise style: white background, Inter or Roboto font, high contrast neutral lines, subtle blue-gray accents, orthogonal connectors where possible, consistent spacing, and no decorative gradients. Keep every label, actor, component, field, state, relationship, and cardinality exactly as described.

## 1. ch1_scf_ecosystem

Create a conceptual flowchart titled `Supply Chain Finance Ecosystem`.

Use a top-to-bottom layout with two grouped sections. The upper group is named `Governance and Financing` and contains two boxes: `Bank` with the details `program governance` and `financing control`, and `SCF Program` with the details `product rules`, `eligibility`, and `finance limits`. The lower group is named `Commercial Relationship` and contains three boxes: `Anchor` with the details `large buyer or seller` and `risk reference`, `Counterparty` with the details `supplier / buyer` and `SME participant`, and `Invoice Pool` with the details `cashflows` and `trade documents`.

Connect `Bank` to `SCF Program` with the label `governance`. Connect `Anchor` to `SCF Program` with the label `program relationship`. Connect `SCF Program` to `Counterparty` with the label `eligible operations`. Connect `Invoice Pool` to `SCF Program` with the label `invoice evidence`. Connect `Counterparty` to `Anchor` with the label `goods, services, invoice exchange`. The diagram must communicate that the bank governs the program, the anchor participates through a program relationship, invoices provide evidence, and the counterparty operates under eligible SCF operations.

## 2. ch1_internship_workflow

Create a left-to-right workflow diagram titled `Daily Development and Validation Workflow`.

Divide the diagram into three swimlane-style groups. The first group is `Developer Lane` and contains `Jira Ticket`, `Implementation` with the details `Backend + Frontend`, and `Push Branch` with the detail `Bitbucket`. The second group is `Tech Lead Lane` and contains `Pull Request Review` and `Merge`. The third group is `Tester Lane` and contains `Verification`.

Connect the main path as `Jira Ticket -> Implementation -> Push Branch -> Pull Request Review`. From `Pull Request Review`, draw an approved path to `Merge`, then to `Verification`. Add a dashed feedback path from `Pull Request Review` back to `Implementation` labeled `changes requested`. Add another dashed feedback path from `Verification` back to `Implementation` labeled `defect feedback`. The diagram should make the delivery loop clear: implement, review, merge, verify, then return to implementation if review or testing finds issues.

## 3. ch1_internship_timeline

Create a horizontal timeline titled `Internship Timeline`.

Use five milestone boxes from left to right. The first is `February 2026` with the details `Remote training`, `Business logic`, and `Java / Spring Boot`. The second is `Week 3` with the details `On-site work`, `Team integration`, and `SCF codebase`. The third is `Sprints 2 to 8` with the details `Jira tickets` and `PR + testing`. The fourth is `Mondays` with the details `PO refinement`, `Module rules`, and `Diagram reviews`. The final milestone is `July 1st 2026` with the details `Report closure` and `Final synthesis`.

Connect the milestones linearly: `February 2026 -> Week 3 -> Sprints 2 to 8 -> Mondays -> July 1st 2026`. The timeline should read as a chronological progression from training, to team integration, to sprint delivery, to repeated PO refinement sessions, then report closure.

## 4. ch2_global_architecture

Create a layered architecture diagram titled `Global Architecture of the SCF Platform`.

Use a top-to-bottom layered structure with three groups. The first group is `Channel Layer` and contains `React SPA` with the detail `role views`, and `Axios Client` with the detail `gateway paths`. The second group is `Business and Edge Layer` and contains `adria-gateway` with the details `JWT, filters, routing`, `scf-service` with the details `modular monolith` and `SCF modules`, and `FDL / Properties` with the details `reference data` and `runtime values`. The third group is `Infrastructure Layer` and contains `Keycloak` with the detail `OIDC`, `PostgreSQL` with the detail `business data`, `MinIO` with the detail `documents`, and `Kafka` with the detail `events`.

Connect `React SPA -> Axios Client -> adria-gateway`. From `adria-gateway`, connect to `scf-service` and to `FDL / Properties`. Add a dashed dependency from `adria-gateway` to `Keycloak`. From `scf-service`, connect to `PostgreSQL`, `MinIO`, and `Kafka`. Make the gateway the central entry point between the frontend and backend services, and show infrastructure dependencies below the services.

## 5. ch2_gateway_filter_chain

Create a left-to-right flow diagram titled `Gateway Routing and Filter Chain`.

Use two grouped sections. The main group is `Gateway Layer` and contains the boxes `Request` with `browser/API`, `Auth` with `JWT / public paths`, `Security` with `ClamAV, limits`, `Routing` with `/scf /fdl /properties`, `Discovery` with `lb:// service`, and `Fallback` with `resilience`. The secondary group is `Callback Security` and contains `HMAC` with `webhooks`, and `Logging` with `correlation`.

Connect the main chain as `Request -> Auth -> Security -> Routing -> Discovery -> Fallback`. Add dashed support connectors from `HMAC` to `Routing` and from `Logging` to `Routing`. The drawing should show that normal browser or API requests pass through authentication, scanning and limits, routing, service discovery, and fallback handling, while webhook HMAC validation and correlation logging support the routing layer.

## 6. ch2_auth_role_flow

Create a UML sequence diagram titled `Authentication and Role Resolution`.

Use numbered messages and lifeline activation bars. The actor is `Browser`. The participants, from left to right, are `Keycloak`, `React Auth`, `Business View`, and `Backend`.

Sequence:
1. `Browser` sends `authorize + PKCE` to `Keycloak`; activate `Keycloak`.
2. `Keycloak` returns `authorization code` to `Browser`; deactivate `Keycloak`.
3. `Browser` sends `token exchange` to `Keycloak`; activate `Keycloak`.
4. `Keycloak` returns `access + refresh token` to `React Auth`; deactivate `Keycloak`.
5. Activate `React Auth`.
6. `React Auth` sends `decode roles` to `Business View`; activate `Business View`.
7. `Business View` returns `BANK / ANCHOR / COUNTERPARTY` to `React Auth`; deactivate `Business View`.
8. `React Auth` sends `Bearer API call` to `Backend`; activate `Backend`.
9. `Backend` returns `authorized response` to `React Auth`; deactivate `Backend`.
10. Deactivate `React Auth`.

The diagram should emphasize PKCE login, token exchange, role decoding in the frontend, and the final authorized backend API call.

## 7. ch2_storage_document_flow

Create a left-to-right architecture flow titled `Document Storage and Conversion Flow`.

Use four grouped sections. The first group is `Frontend` and contains `Upload UI` with the detail `multipart file`. The second group is `Gateway` and contains `Gateway` with the detail `ClamAV scan`. The third group is `Business Service` and contains `SCF Service` with the details `metadata + storage ports`. The fourth group is `Storage and Conversion` and contains database/storage nodes: `MinIO` with `object bytes`, `PostgreSQL` with `document row`, and `Gotenberg` with `PDF conversion`.

Connect `Upload UI -> Gateway -> SCF Service`. From `SCF Service`, connect separately to `MinIO`, `PostgreSQL`, and `Gotenberg`. The diagram should show that uploaded files are scanned at the gateway, then the SCF service stores binary bytes in MinIO, metadata in PostgreSQL, and uses Gotenberg for PDF conversion.

## 8. ch3_core_data_model

Create a UML class diagram titled `Core SCF Data Model`.

Use class boxes with attributes. Include these classes and fields exactly:

`ScfProductDefinition`: `+String code`, `+ProductType type`, `+Instrument instrument`, `+ApprovalStatus status`.

`ScfProgramConfiguration`: `+UUID id`, `+String reference`, `+Currency currency`, `+BigDecimal financePercent`, `+ProgramStatus status`.

`ScfAnchor`: `+String anchorCode`, `+String name`, `+AnchorRole role`.

`ScfCounterParty`: `+String legalName`, `+CounterpartyRole role`, `+CounterPartyStatus status`, `+String taxIdentifier`.

`ScfProgramCounterParty`: `+String roleInProgram`, `+BigDecimal limitAmount`, `+Boolean active`.

`ScfBankAccount`: `+String iban`, `+String swiftCode`, `+Currency currency`, `+Boolean primaryAccount`.

`ScfProgramCashflow`: `+String invoiceNumber`, `+BigDecimal amount`, `+LocalDate dueDate`, `+String validationStatus`.

`Country`: `+String code`, `+String name`.

`City`: `+String code`, `+String name`, `+String postalCode`.

Relationships and cardinalities: `ScfProductDefinition "1" -> "0..*" ScfProgramConfiguration` labeled `defines`; `ScfProgramConfiguration "1" -> "1..*" ScfAnchor` labeled `assigns`; `ScfProgramConfiguration "1" -> "0..*" ScfProgramCounterParty` labeled `configures`; `ScfCounterParty "1" -> "0..*" ScfProgramCounterParty` labeled `joins`; `ScfCounterParty "1" -> "0..*" ScfBankAccount` labeled `owns`; `ScfProgramConfiguration "1" -> "0..*" ScfProgramCashflow` labeled `contains`; `Country "1" -> "0..*" City` labeled `contains`; and `ScfCounterParty -> Country` labeled `country`.

Layout suggestion: place `ScfProductDefinition` above `ScfProgramConfiguration`; place program-related classes around the program configuration; place geographic classes on the right with `Country` above `City`; keep cardinality labels close to connector endpoints.

## 9. ch3_maker_checker_state

Create a UML state machine diagram titled `Maker/Checker Governance State Machine`.

States are `DRAFT`, `PENDING_APPROVAL`, `APPROVED`, and `REJECTED`. Start from an initial black dot and transition to `DRAFT`. From `DRAFT`, transition to `PENDING_APPROVAL` with the label `submit()`. From `PENDING_APPROVAL`, branch to `APPROVED` with the label `checker approves`, and to `REJECTED` with the label `checker rejects(comment)`. From `REJECTED`, transition back to `DRAFT` with the label `restore originalData on update rejection`. From `APPROVED`, transition to the final state.

The visual should make the maker/checker governance loop obvious: a maker submits a draft, a checker approves or rejects it, and rejected work returns to draft with restored original data.

## 10. ch3_program_configuration_flow

Create a UML activity diagram titled `Program Configuration Activity`.

Use a top-to-bottom flow. Start with a start node, then show the following activity boxes in order: `Select product definition`, `Enter general program data`, `Assign anchor and counterparties`, `Configure fees and flat charges`, and `Configure cashflow and disbursement rules`. After these steps, add a decision diamond labeled `Complete?`.

From `Complete?`, draw a solid path labeled `yes: submit for approval` to the end node. Draw a dashed loop labeled `no` back to `Enter general program data`. The diagram should communicate that program configuration is iterative until the configuration is complete enough to submit for approval.

## 11. ch4_navigation_role_flow

Create a left-to-right frontend architecture flow titled `Frontend Routing and Role-Based Navigation`.

Use two grouped sections. The first group is `Application Shell` and contains `App.tsx` with the details `providers + routes`, `KeycloakAuth` with `PKCE callback + tokens`, `AuthGuard` with `protected route + redirect`, and `Index.tsx` with `sidebar + selectedModule`. The second group is `Role Adaptation` and contains `Business View` with `BANK / ANCHOR / COUNTERPARTY`, and `Feature Modules` with `dashboard + SCF flows`.

Connect `App.tsx -> KeycloakAuth`. Also connect `App.tsx -> AuthGuard`. Connect `AuthGuard -> Index.tsx`. From `Index.tsx`, connect to both `Business View` and `Feature Modules`. The diagram should show that the application shell initializes authentication and route protection before adapting navigation and modules according to user roles.

## 12. ch4_use_case_back_office

Create a UML use case diagram titled `SCF Back Office`.

Use an actors area on the left and a system boundary named `SCF Back Office Boundary` on the right. Actors are `Bank Maker` and `Bank Checker`. Inside the boundary, include these use cases: `Create / edit product`, `Configure program`, `Onboard counterparty`, `Submit pending change`, `Review pending operation`, and `Approve or reject`.

Associations: `Bank Maker` connects to `Create / edit product`, `Configure program`, `Onboard counterparty`, and `Submit pending change`. `Bank Checker` connects to `Review pending operation` and `Approve or reject`. Add an include relationship from `Onboard counterparty` to `Submit pending change` labeled `<<include>>`. Add another include relationship from `Review pending operation` to `Approve or reject` labeled `<<include>>`.

The diagram should highlight maker/checker separation: the maker creates and submits changes, while the checker reviews and approves or rejects pending operations.

## 13. ch4_use_case_middle_office

Create a UML use case diagram titled `SCF Middle Office`.

Use an actors area on the left and a system boundary named `SCF Middle Office Boundary` on the right. Actors are `Middle Office Analyst` and `Compliance / Audit`. Inside the boundary, include these use cases: `Monitor transactions`, `Filter inquiry results`, `Follow failed payments`, `Export operational report`, `Consult audit trail`, and `Analyze portfolio exposure`.

Associations: `Middle Office Analyst` connects to `Monitor transactions`, `Filter inquiry results`, `Follow failed payments`, `Export operational report`, and `Analyze portfolio exposure`. `Compliance / Audit` connects only to `Consult audit trail`. Add an include relationship from `Monitor transactions` to `Filter inquiry results` labeled `<<include>>`.

The diagram should communicate that middle office work focuses on monitoring, analysis, failed payment follow-up, exports, and audit visibility.

## 14. ch4_use_case_front_office

Create a UML use case diagram titled `SCF Front Office`.

Use external actors only. Place the primary actors `Buyer` and `Supplier` on the left side of the system boundary. Place the secondary/supporting actor `Bank` on the right side of the system boundary. Do not place any actor inside the system boundary. The system boundary is named `SCF Front Office Boundary`. Inside the boundary, include these use cases: `Upload or create invoice`, `Track invoice status`, `Request finance`, `Request early payment`, `Request payment`, and `Consult transactions`.

Associations: connect `Buyer` to `Track invoice status`, `Request payment`, and `Consult transactions`. Connect `Supplier` to `Upload or create invoice`, `Request finance`, and `Request early payment`. Connect the secondary actor `Bank` to `Request finance`, `Request early payment`, and `Request payment`.

The diagram should respect UML use-case rules: primary actors on the left, the secondary/supporting actor on the right, actors outside the boundary, use cases inside the boundary, and simple association lines without arrowheads.

## 15. ch4_invoice_upload_flow

Create a left-to-right component interaction diagram titled `Invoice Upload Component Interaction`.

Use a single grouped component boundary named `InvoiceUploadForm`. Inside it, include six components: `State owner` with `program context`, `ExcelUploader` with `spreadsheet rows`, `ScannedUploader` with `PDF / image path`, `UploadTable` with `row validation` and `issue details`, `Summary` with `counts`, and `Reports` with `rejection file`.

Connect the spreadsheet path as `State owner -> ExcelUploader -> UploadTable -> Summary`. Connect the scanned document path as `State owner -> ScannedUploader -> UploadTable -> Reports`. The diagram should show that one form owns the program context, then either Excel rows or scanned files feed the upload table, which leads to summary counts or rejection reports.

## 16. ch4_finance_disbursement_wizard

Create a simple horizontal wizard flow titled `Finance Disbursement Wizard - Corrected Step Order`.

Use six equally spaced step boxes from left to right: `1. Program / Product`, `2. Invoice Selection`, `3. Finance Details`, `4. Repayment Details`, `5. Accounting Entries`, and `6. Review / Submit`.

Connect the boxes in order with straight arrows: `1. Program / Product -> 2. Invoice Selection -> 3. Finance Details -> 4. Repayment Details -> 5. Accounting Entries -> 6. Review / Submit`. The visual should look like a clean stepper that makes the corrected finance disbursement order explicit.

## 17. ch4_services_layer

Create a left-to-right frontend services layer diagram titled `Frontend Services Layer`.

Use two grouped sections. The first group is `UI Layer` and contains `Components` with the details `forms, tables, wizards`, and `Hooks` with the details `useProgramForm` and `useInvoiceForm`. The second group is `Access Layer` and contains `Feature Services` with the details `typed functions` and `endpoint mapping`, `Axios Client` with `Bearer token`, and `Types` with `DTO models`.

Connect `Components -> Hooks -> Feature Services`. From `Feature Services`, connect to `Axios Client` and to `Types`. The diagram should show how UI components use hooks, hooks call typed feature services, and feature services rely on Axios for authenticated calls and Types for DTO contracts.

## 18. ch5_disbursement_use_case

Create a UML use case diagram titled `Disbursement Module`.

Use one primary actor only: `Buyer or Supplier`, placed outside the system boundary on the left. Do not show `Payment Gateway` or `System Scheduler` as actors in this use-case diagram. The system boundary is named `Disbursement Module Boundary`. Inside the boundary, include these use cases: `Request finance`, `Choose mode INDIVIDUAL/CLUBBED`, `Automatic disbursement`, `Run eligibility checks`, `Submit payment instruction`, and `Process async callback`.

Associations: `Buyer or Supplier` connects to `Request finance` and `Choose mode INDIVIDUAL/CLUBBED`.

Include relationships: `Request finance` includes `Choose mode INDIVIDUAL/CLUBBED`; `Choose mode INDIVIDUAL/CLUBBED` includes `Run eligibility checks`; `Automatic disbursement` includes `Run eligibility checks`; `Run eligibility checks` includes `Submit payment instruction`; `Submit payment instruction` includes `Process async callback`. Label all include relationships as `<<include>>`.

The diagram should keep external technical collaborators out of the actor set. It should distinguish manual finance requests from automatic disbursement while showing that both paths converge on eligibility checks, payment instruction, and callback processing.

## 19. ch5_disbursement_class_diagram

Create a UML class diagram titled `Disbursement Domain Class Diagram`.

Include these classes and fields exactly:

`Program`: `+ProgramType type`, `+Decimal financePercent`, `+int maxDisbursement`, `+int maxTenorDays`, `+bool autoDisbursement`.

`Invoice`: `+InvoiceStatus status`, `+AmountState amountState`, `+Decimal amount`, `+Date issueDate`, `+Date dueDate`, `+int tenorDays`.

`Disbursement`: `+DisbursementMode mode`, `+DisbursementSource source`, `+DisbursementState state`, `+Decimal amount`, `+String paymentRef`, `+String failureReason`.

`FinanceRecord`: `+FinanceStatus status`, `+FinanceScope scope`, `+Decimal principalAmount`, `+Date maturityDate`, `+Decimal totalDue`.

`FinanceRecordInvoice`: `+Decimal allocatedAmount`, `+Decimal settledAmount`, `+String allocationState`.

`Transaction`: `+TransactionType type`, `+Decimal amount`, `+String reference`, `+Instant createdAt`.

Relationships and cardinalities: `Program "1" -> "1..*" Invoice` labeled `contains`; `Program "1" -> "0..*" Disbursement` labeled `authorizes`; `Disbursement "1" -> "1..*" Invoice` labeled `covers`; `Disbursement "1" -> "0..1" FinanceRecord` labeled `creates if SUCCESS`; `FinanceRecord "1" -> "1..*" FinanceRecordInvoice` labeled `allocates`; `FinanceRecordInvoice "1..*" -> "1" Invoice` labeled `references`. Add dashed dependency relationships from `Invoice` to `Transaction` labeled `INVOICE`, from `Disbursement` to `Transaction` labeled `FINANCE_DISBURSEMENT`, and from `FinanceRecord` to `Transaction` labeled `FINANCE_REPAYMENT`.

Layout suggestion: place `Program` on the left, `Invoice` near it, `Disbursement` in the center, `FinanceRecord` to the right, `FinanceRecordInvoice` between finance record and invoice, and `Transaction` below as the accounting/event representation. Keep cardinalities visible and close to connectors.

## 20. ch5_disbursement_state_machine

Create a UML state machine diagram titled `Disbursement Lifecycle State Machine`.

States are `INITIATED`, `PENDING_CONFIRMATION`, `SUCCESS`, and `FAILED`. Start from an initial state and transition to `INITIATED`. From `INITIATED`, branch to `PENDING_CONFIRMATION` with the label `POST /payments / 202 Accepted + paymentRef`, and branch to `FAILED` with the label `sync 422 rejection`. From `PENDING_CONFIRMATION`, branch to `SUCCESS` with the label `async callback SUCCESS`, and branch to `FAILED` with the label `async callback FAILED`. Both `SUCCESS` and `FAILED` transition to final states.

Add a note next to `SUCCESS` containing these four lines: `Create FinanceRecord`, `Create FINANCE_DISBURSEMENT transaction`, `Publish disbursement.success`, and `Set invoice FINANCED`.

The diagram should make the asynchronous payment confirmation path clear: a request begins as initiated, may fail synchronously, may wait for callback confirmation, then ends as success or failure.

## 21. ch5_disbursement_sequence_uml

Create a UML sequence diagram titled `Manual Disbursement with Async Payment Callback`.

Use numbered messages and activation bars. The actor is `Buyer/Supplier`. Participants, from left to right, are `React Wizard`, `Disbursement Service`, `Program/Invoice Services`, `Payment Gateway`, `adria-gateway`, `Kafka payment.callback`, and `DisbursementEventConsumer`.

Sequence:
1. `Buyer/Supplier` sends `select lodged invoices + mode` to `React Wizard`; activate `React Wizard`.
2. `React Wizard` sends `requestFinance(payload)` to `Disbursement Service`; activate `Disbursement Service`.
3. `Disbursement Service` sends `load program rules + invoice state` to `Program/Invoice Services`; activate `Program/Invoice Services`.
4. `Program/Invoice Services` returns `rules, tenor, remaining amount` to `Disbursement Service`; deactivate `Program/Invoice Services`.
5. `Disbursement Service` performs a self-call labeled `run C1-C4 eligibility checks`.
6. Add an `alt` fragment. In the first branch, labeled `any eligibility check fails`, `Disbursement Service` returns `reject with business code` to `React Wizard`.
7. In the second branch, labeled `eligible`, `Disbursement Service` sends `POST /payments` to `Payment Gateway`; activate `Payment Gateway`.
8. `Payment Gateway` returns `202 Accepted + paymentRef` to `Disbursement Service`; deactivate `Payment Gateway`.
9. `Disbursement Service` returns `state=PENDING_CONFIRMATION` to `React Wizard`.
10. After the alt fragment, `Payment Gateway` sends `POST /callbacks/payment` to `adria-gateway`; activate `adria-gateway`.
11. `adria-gateway` performs a self-call labeled `validate HMAC signature`.
12. `adria-gateway` returns `HTTP 200 fast ack` to `Payment Gateway`.
13. `adria-gateway` sends `publish payment.callback` to `Kafka payment.callback`; activate `Kafka payment.callback`; deactivate `adria-gateway`.
14. `Kafka payment.callback` sends `consume callback event` to `DisbursementEventConsumer`; deactivate `Kafka payment.callback`; activate `DisbursementEventConsumer`.
15. `DisbursementEventConsumer` sends `update disbursement SUCCESS/FAILED` to `Disbursement Service`.
16. `Disbursement Service` performs a self-call labeled `create FinanceRecord + Transaction and update Invoice`.
17. Deactivate `DisbursementEventConsumer`, `Disbursement Service`, and `React Wizard`.

The diagram should emphasize that the user request receives a pending response before the asynchronous callback completes the final disbursement state.

## 22. ch6_contribution_streams

Create a left-to-right flow diagram titled `Internship Contribution Streams`.

Use two grouped sections. The first group is `Platform Delivery` and contains `Jira` with `tickets`, `Bitbucket` with `PR review`, and `Tester` with `validation`. The second group is `PFE Module Preparation` and contains `PO Sessions` with `business rules`, `Diagrams` with `flow review`, and `Target Design` with `future merge`.

Connect `Jira -> Bitbucket -> Tester` in the platform delivery group. Connect `PO Sessions -> Diagrams -> Target Design` in the PFE preparation group. Add a dashed cross-group connector from `Tester` to `PO Sessions` labeled `delivery context feeds module analysis`. The diagram should show that implementation delivery and final-year project design preparation progressed in parallel and informed each other.

## 23. ch6_skills_map

Create a top-to-bottom skills map titled `Skills Acquired During the Internship`.

Use one central root box at the top labeled `Internship Growth`. Under it, place six skill area boxes: `Backend` with `Spring Boot` and `JPA/OAuth2`; `Frontend` with `React` and `TypeScript`; `DevOps` with `Docker` and `Git / PR`; `Banking` with `SCF domain` and `program logic`; `Collaboration` with `Scrum` and `PO refinement`; and `Quality` with `review` and `testing feedback`.

Connect `Internship Growth` to each skill area. The diagram should read as a compact capability map showing technical, domain, collaboration, and quality-related learning outcomes.

## 24. ch6_future_roadmap

Create a left-to-right roadmap diagram titled `Recommendations for Future Development`.

Use four main roadmap boxes in order: `Disbursement` with `native module`, `Async Flows` with `Kafka/RabbitMQ`, `Mobile` with `counterparty access`, and `Analytics` with `portfolio view`. Add one guiding principle box labeled `Common direction` with the details `Governed, traceable, configurable, useful for bank operations`.

Connect the roadmap linearly as `Disbursement -> Async Flows -> Mobile -> Analytics`. Add dashed influence connectors from `Common direction` to each of the four roadmap boxes. The diagram should communicate that all recommendations share the same product direction: governed, traceable, configurable, and useful for operational banking users.
