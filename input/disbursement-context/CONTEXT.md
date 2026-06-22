# Disbursement Module — Chapter Generation Context

## Purpose of This File
This README is the single source of truth for generating the Disbursement module chapter of the SCF platform internship report. It documents every domain decision, every resolved ambiguity, and every confirmed fact established through iterative Product Owner sessions. **Do not speculate on anything not listed here. If something is marked as OPEN QUESTION, acknowledge it as unresolved — do not invent an answer.**

---

## 1. Platform Overview (Minimum Context)

The platform is a **Supply Chain Finance (SCF)** system. It enables three parties — supplier (seller), buyer, and bank — to manage invoice financing. The supplier delivers goods and issues an invoice. Instead of waiting for the buyer to pay at maturity (30–120 days), the bank pays the supplier early at a discount, and the buyer repays the bank at the original due date.

**Two program types are supported:**
- **Buyer-Anchored (Reverse Factoring):** The buyer's credit rating determines the rate. Bank holds buyer default risk. Supplier is always protected.
- **Supplier-Anchored (Factoring):** Supplier's credit + buyer payment history determines rate. Two sub-types: Recourse (bank recovers from supplier on default) and Non-recourse (bank absorbs loss entirely, charges higher fee).

**The three request types available on a lodged invoice:**

| Request Type | Parties | Bank Involved | Invoice Final State |
|---|---|---|---|
| Early Payment | Buyer ↔ Supplier only | No | MANUALLY_PAID |
| Request Finance | Supplier + Bank | Yes | FINANCED |
| Request Payment | Buyer pays manually | No | MANUALLY_PAID |

**Access symmetry — confirmed by PO:** Both buyer AND seller can initiate all three request types. In Buyer-Anchored programs, the supplier may not be a bank client (no platform access), so the buyer acts on the supplier's behalf. In Supplier-Anchored programs, the seller can initiate Request Payment, receive a Payment ID, and communicate it to the buyer out-of-band.

---

## 2. System Architecture (Relevant Context)

The platform is a **single deployable service** (`scf-service`) organized into bounded internal modules. It is NOT a microservices system today. Spring Cloud infrastructure (gateway, config server, service registry) is in place because **other services will join the platform in the future** — the infrastructure prevents costly restructuring later. Any new service registers with `adria-registry`, retrieves config from `adria-config`, and is routed through `adria-gateway` without touching existing code.

**Components:**
- `adria-gateway` — Spring Cloud Gateway. Single entry point. JWT validation (Keycloak). Request routing. Rate limiting. **Also receives Payment Gateway webhook callbacks**, validates HMAC signature, publishes to Kafka.
- `adria-config` — Spring Cloud Config Server. Centralized configuration.
- `adria-registry` — Eureka Server. Service discovery.
- `scf-service` — Core modular monolith. All business logic.
- `scf-entities` — Shared JAR. All JPA entities, enums, DTOs.

**Modules inside scf-service:**
- Program Module
- Invoice Module
- **Disbursement Module ← Author's module**
- Finance Module
- Repayment Module ← Other intern's module
- Counterparty Module

**Module boundary rule:** Modules never call each other's repositories directly. All cross-module communication is through service interfaces.

**Tech stack:** Java / Spring Boot / Spring Data JPA / PostgreSQL / Apache Kafka / Keycloak (OIDC, OAuth2, JWT) / MinIO (object storage for invoice PDFs) / React SPA (frontend — **IS in scope**) / Docker / Flyway / Maven.

**Frontend IS in scope.** The React SPA includes a **Transaction Inquiry** page — described in detail in Section 6 below.

---

## 3. The Five Business-Layer Domain Entities

These five entities are distinct. Confusing them leads to incorrect models. Their exact roles were clarified through multiple PO sessions.

### 3.1 Program
The central configuration object. Governs how all invoices under it are financed.

**Key attributes:**
```
type                    : BUYER_ANCHORED | SUPPLIER_ANCHORED
financePercent          : decimal (e.g. 0.80 = bank finances 80% of invoice amount)
maxDisbursement         : integer — PROGRAM-LEVEL cap on total disbursements (NOT per invoice)
maxTenorDays            : integer — max invoice tenor the bank will accept
autoDisbursement        : boolean — if true, triggers automatic disbursement on invoice upload
supportsEarlyPayment    : boolean
defaultDiscount         : decimal — rate for fixed early payment discount
supportsDynamicDiscount : boolean
dynamicDiscountRatePerDay : decimal
```

### 3.2 Invoice
The **commercial document**: "I delivered goods, you owe me money." Exists before any financing.

**Key attributes:**
```
status              : DRAFT | SUBMITTED | APPROVED_ACKNOWLEDGED | LODGED | FINANCED | MANUALLY_PAID
invoice_amount_state: PENDING | SETTLED  (separate field — see Section 4.1)
eligibleForFinance  : boolean
amount, issueDate, dueDate, tenorDays
```

### 3.3 Disbursement
The **payment execution record**: the act of the bank wiring money to the supplier. Created when a user (or the system automatically) requests financing and eligibility checks pass.

**Key attributes:**
```
mode        : INDIVIDUAL | CLUBBED
source      : MANUAL | AUTO
state       : INITIATED | PENDING_CONFIRMATION | SUCCESS | FAILED
amount
paymentRef  : reference returned by Payment Gateway on 202 Accepted, used to match async callback
failureReason
```

**Important: FinanceRequest was removed from the domain model.** An earlier design had a separate FinanceRequest entity. This was dropped. The Disbursement entity itself carries `mode` (INDIVIDUAL/CLUBBED) and `source` (MANUAL/AUTO), which is sufficient at the business layer. There is no FinanceRequest table or entity in the current model.

### 3.4 FinanceRecord
The **bank's repayment tracker**: "I paid the supplier, the buyer owes me this amount back by maturity date." Created ONLY when a Disbursement reaches SUCCESS state.

**Also called "Finance Repayment Record" — these are the same thing.** Two names are used interchangeably in product discussions. In the data model, there is one entity: FinanceRecord.

**Key attributes:**
```
status          : CREATED | OVERDUE | REPAID | NPA
scope           : INDIVIDUAL | CLUBBED
principalAmount
maturityDate    : = invoice.dueDate
interestAmount, penaltyAmount, totalDue
retryCount
crystallizedAt  : timestamp recorded on OVERDUE→NPA transition (regulatory requirement)
```

### 3.5 Transaction
A **business ledger entry** for any money movement. This is NOT a database transaction (commit/rollback). It is a business record that users see on the dashboard.

**Three confirmed transaction types relevant to this module:**
```
INVOICE              : created when invoice is uploaded/processed
FINANCE_DISBURSEMENT : created when a Disbursement reaches SUCCESS
FINANCE_REPAYMENT    : created when a FinanceRecord is REPAID
EARLY_PAYMENT        : created when buyer-seller early payment completes
```

**The Transaction Inquiry page** (frontend) shows all invoices in all programs, with their associated FINANCE_DISBURSEMENT transaction if the invoice was financed, and the FINANCE_REPAYMENT transaction if a repayment occurred. Finance Records themselves are not shown separately — they surface through their Transaction records. The three-dot action menu on each invoice row is the entry point for all three request types.

---

## 4. State Machines

### 4.1 Invoice Lifecycle State Machine

**Confirmed by PO: one `status` field, not two.**

An earlier proposal had separate `state` and `status` fields. PO decision: use one field. A separate `invoice_amount_state` attribute decouples financial settlement status.

```
States and transitions:
DRAFT → SUBMITTED → APPROVED_ACKNOWLEDGED → LODGED
LODGED → FINANCED          (when Disbursement succeeds)
LODGED → MANUALLY_PAID     (when early payment or direct payment completes)
```

**Deleted states — do not mention them as existing:**
- `PARTIALLY_FINANCED` — deleted
- `FULLY_FINANCED` — deleted
- `PAID_THROUGH_FINANCE` — renamed to `FINANCED`

**invoice_amount_state (separate field, only relevant when status = FINANCED):**
- `PENDING` — Disbursement succeeded, Finance Record is active, buyer has not yet repaid the bank
- `SETTLED` — Finance Record is REPAID, bank has received its money back

**UI behavior:**
- Three-dot action menu (Early Payment / Request Finance / Request Payment) is **active** at LODGED state
- Three-dot menu is **blocked** at FINANCED state — no further actions possible on a financed invoice
- Three-dot menu is **blocked** at MANUALLY_PAID state

**APPROVED_ACKNOWLEDGED note:** In Buyer-Anchored programs, the buyer acknowledges the invoice. In Supplier-Anchored programs, the bank approves it. Both cases produce the same state stored as the single value `APPROVED_ACKNOWLEDGED` — same logical stage, different word used in product discussions.

### 4.2 Disbursement State Machine

```
● (initial) → INITIATED → PENDING_CONFIRMATION → SUCCESS
                         ↘                      ↘
                         FAILED (422 immediate)  FAILED (async callback)
```

**State definitions:**
- `INITIATED` — Disbursement record created. HTTP POST submitted to Payment Gateway. If gateway returns 422 immediately (invalid account, insufficient funds), transitions directly to FAILED.
- `PENDING_CONFIRMATION` — Gateway returned 202 Accepted. `paymentRef` stored for callback matching. Waiting for async webhook.
- `SUCCESS` — Async callback confirmed payment executed. Six consequences fire (see Section 7, Event Chain).
- `FAILED` — Either 422 sync rejection or async callback returned FAILED. Invoice remains LODGED, available for retry.

### 4.3 Finance Record State Machine

```
CREATED → REPAID                    (direct repayment at maturity)
CREATED → OVERDUE → REPAID          (retry success)
CREATED → OVERDUE → NPA             (all retries exhausted = CRYSTALLIZATION)
```

**OVERDUE progressive penalties:**
- Days 1–7: base penalty rate
- Days 8–30: base rate × 1.5
- Days 31+: base rate × 2.0
- Exponential backoff retries run throughout the grace period

**NPA and Crystallization:**
Crystallization is the formal term for the OVERDUE→NPA transition. It comes from secured finance law: a floating charge that hovered over a pool of assets "crystallizes" — attaches to specific assets and becomes a fixed legal claim. In the platform:
- `crystallizedAt` timestamp is recorded (required for regulatory reporting)
- Bank's accounting team must provision for the loss on its balance sheet
- Legal escalation is triggered
- **Recourse program:** bank pursues the supplier for recovery
- **Non-recourse program:** bank absorbs the loss entirely

**Loan Transfer (special case):** Before defaulting, a buyer can take a bank loan to cover the Finance Record. On loan approval, the Finance Record transitions directly to REPAID. A Transaction of type `LOAN_TRANSFER` is created for audit. The loan itself is managed outside the SCF system.

---

## 5. Class Diagram — Confirmed Relationships

```
Program  1 ────────────────── 1..* Invoice
Program  1 ────────────────── 0..* Disbursement
Disbursement 1 ──── covers ── 1..* Invoice      (INDIVIDUAL: 1→1, CLUBBED: 1→N)
Disbursement 1 ──── creates (if SUCCESS) ── 0..1 FinanceRecord

Invoice      ──── generates ──▶ Transaction (type=INVOICE)
Disbursement ──── generates ──▶ Transaction (type=FINANCE_DISBURSEMENT)
FinanceRecord ─── generates ──▶ Transaction (type=FINANCE_REPAYMENT)
```

**The diamond (rhombus) is intentional and valid:** Program→Invoice and Program→Disbursement, combined with Disbursement→Invoice, form a rhombus. This is not a cycle. It expresses that a disbursement can only cover invoices belonging to the same program it is associated with.

**INDIVIDUAL vs CLUBBED modes:**
- `INDIVIDUAL` — User selects N invoices and chooses INDIVIDUAL. System creates N independent Disbursements (one per invoice), each with its own Finance Record on success. Failure of one has no impact on the others.
- `CLUBBED` — User selects N invoices and chooses CLUBBED. System creates ONE Disbursement for the combined amount, ONE Finance Record linked to all N invoices via a `finance_record_invoices` junction table.

**Removed entity: FinanceRequest.** Do not include this in the class diagram or any entity descriptions. It was removed from the model.

---

## 6. Eligibility Engine

Before any Disbursement is created, four checks run in sequence. All must pass.

### Variable Definitions
```
financed_amount_total      = SUM(disbursements WHERE invoiceId = X AND state = SUCCESS)
max_financeable_amount     = invoice.amount × program.financePercent
remaining_eligible_amount  = max_financeable_amount − financed_amount_total
invoice_tenor              = invoice.dueDate − invoice.issueDate  (calendar days)
program_disbursement_count = COUNT(disbursements WHERE programId = P AND state = SUCCESS)
```

### The Four Checks

**C1:** `remaining_eligible_amount > 0`
- Rejection code: `ELIGIBILITY_QUOTA_EXHAUSTED`
- The invoice has not already been fully financed.

**C2:** `program_disbursement_count < program.maxDisbursement`
- Rejection code: `PROGRAM_CAP_REACHED`
- **This is a PROGRAM-LEVEL counter, not per-invoice.** When the cap is reached, ALL invoices in the program are blocked — confirmed by PO after an initial incorrect assumption of per-invoice scope.

**C3:** `requestedAmount ≤ remaining_eligible_amount`
- Rejection code: `ELIGIBILITY_AMOUNT_EXCEEDED`
- On rejection, system returns the actual `remaining_eligible_amount` to the UI.

**C4:** `invoice_tenor ≤ program.maxTenorDays`
- Rejection code: `TENOR_EXCEEDED`
- Limits the bank's capital exposure duration.

---

## 7. Manual vs Automatic Disbursement

### Manual Flow
User logs in, navigates to invoice list, selects one or more invoices via the three-dot menu, chooses INDIVIDUAL or CLUBBED, sets the requested amount. Eligibility checks C1→C4 run. If all pass, Disbursement created (INITIATED), HTTP POST to gateway, 202 received → PENDING_CONFIRMATION, waiting for async callback.

### Automatic Flow
When `program.autoDisbursement = true`, the flow starts automatically on invoice upload with no user interaction.
- This flag is set at program creation for suppliers with a standing financing agreement — it is a **business pre-approval**, not a system scheduler.
- When an invoice reaches LODGED state, `InvoiceService` publishes `invoice.lodged` to Kafka.
- `EligibilityBatchJob` (Quartz) consumes the event, runs C1→C4.
- If eligible: Disbursement created (source=AUTO, mode=INDIVIDUAL).
- Auto mode always takes **100% of `remaining_eligible_amount`** — no partial selection.
- Auto mode is always INDIVIDUAL — CLUBBED is not available in automatic mode.

---

## 8. Payment Gateway Integration — Two-Phase Pattern

The external Payment Gateway returns HTTP 202 immediately on submission and sends the actual result (SUCCESS or FAILED) via webhook minutes or hours later. This asynchronous gap is absorbed by Apache Kafka.

### Phase 1 — Synchronous Submission
```
DisbursementService → HTTP POST /payments → Payment Gateway
                    ← 202 Accepted + paymentRef
Disbursement state: INITIATED → PENDING_CONFIRMATION
paymentRef stored for later callback matching
```
If gateway returns 422 immediately: Disbursement → FAILED.

### Phase 2 — Asynchronous Confirmation
```
Payment Gateway → POST /callbacks/payment → adria-gateway
adria-gateway: HMAC signature validated
adria-gateway → HTTP 200 OK (fast ack — returned immediately, before any processing)
adria-gateway → publishes event to Kafka topic: payment.callback
DisbursementEventConsumer → consumes event → looks up Disbursement by paymentRef
```

**On SUCCESS callback:**
1. Disbursement → SUCCESS
2. Finance Record CREATED (status=CREATED)
3. Transaction(type=FINANCE_DISBURSEMENT) created
4. Kafka event `disbursement.success` published
5. Invoice status → FINANCED
6. `invoice_amount_state` → PENDING
7. Repayment engine starts monitoring maturity date

**On FAILED callback:**
1. Disbursement → FAILED
2. Failure reason stored
3. Invoice remains LODGED (available for retry)

**Why Kafka between gateway and consumer:**
The gateway returns 200 to the Payment Gateway immediately to prevent timeout-triggered webhook retries. Business logic executes asynchronously in the consumer. Kafka guarantees at-least-once delivery — if the consumer crashes, events wait and are replayed from last committed offset.

**HMAC validation:** Every inbound callback is signed by the Payment Gateway. The hash is verified before Kafka publication. Any callback failing validation is dropped — no fraudulent event enters the system.

---

## 9. Kafka Topics

| Topic | Producer | Consumer | Purpose |
|---|---|---|---|
| `invoice.lodged` | InvoiceService | EligibilityBatchJob | Trigger eligibility check; start auto-disbursement flow |
| `invoice.eligible` | EligibilityBatchJob | DisbursementService | Submit payment to gateway |
| `payment.callback` | adria-gateway (webhook) | DisbursementEventConsumer | Process gateway result |
| `disbursement.success` | DisbursementEventConsumer | InvoiceService | Update invoice → FINANCED |
| `finance.maturity` | MaturityScheduler (cron) | RepaymentService | Trigger repayment at maturity date |

---

## 10. Full Event Trigger Chain

```
EVENT 1: Invoice reaches LODGED state
  → InvoiceService publishes invoice.lodged
  → Transaction(type=INVOICE) created
  → Three-dot menu on invoice becomes active

EVENT 2: Finance requested (Manual: user clicks) OR Auto (EligibilityBatchJob fires)
  → Eligibility checks C1→C4
  → If pass: Disbursement CREATED (INITIATED)
  → HTTP POST to Payment Gateway
  → 202 received → Disbursement = PENDING_CONFIRMATION

EVENT 3: payment.callback consumed — SUCCESS
  → Disbursement = SUCCESS
  → Finance Record CREATED
  → Transaction(FINANCE_DISBURSEMENT) created
  → Kafka: disbursement.success published
  → Invoice = FINANCED, invoice_amount_state = PENDING
  → Three-dot menu blocked

EVENT 4: finance.maturity (cron) fires at invoice due date
  → RepaymentService (other intern) submits repayment to gateway
  → If SUCCESS: Finance Record = REPAID, invoice_amount_state = SETTLED
  → Transaction(FINANCE_REPAYMENT) created

EVENT 5: Repayment FAILED → Finance Record = OVERDUE
  → Progressive penalties applied
  → Exponential backoff retries

EVENT 6: All retries exhausted → CRYSTALLIZATION
  → Finance Record = NPA
  → crystallizedAt timestamp recorded
  → Legal escalation, balance sheet provisioning
```

**Module scope boundary:**
- Disbursement module owns Events 1–3 (up to and including Finance Record creation)
- Repayment module (other intern) owns Events 4–6
- The Finance Record is the handoff artifact

---

## 11. Confirmed PO Decisions (Things That Changed From Initial Assumptions)

| Topic | Initial Wrong Assumption | Confirmed Reality |
|---|---|---|
| Invoice status fields | Two fields: state + status | One `status` field + separate `invoice_amount_state` |
| PARTIALLY_FINANCED | This state exists | Deleted — replaced by `invoice_amount_state = PENDING` |
| FULLY_FINANCED | This state exists | Deleted |
| PAID_THROUGH_FINANCE | Final invoice state | Renamed to FINANCED |
| maxDisbursement scope | Per-invoice limit | Per-PROGRAM — portfolio-level risk control |
| FinanceRequest entity | Separate entity needed | Removed — absorbed into Disbursement (mode + source fields) |
| Who initiates requests | Supplier only | Both buyer AND supplier — access symmetry |
| Auto disbursement trigger | System scheduler on approval | Program flag + EligibilityBatchJob on invoice.lodged Kafka event |
| Multi-invoice disbursement | Always 1 Finance Record per invoice | User chooses INDIVIDUAL or CLUBBED |
| FinanceRecord vs Finance Repayment Record | Two different things | Same entity, two names used in different contexts |
| Frontend scope | Out of scope | **IN SCOPE** — React SPA with Transaction Inquiry |

---

## 12. Open Questions — Do Not Resolve, Acknowledge As Open

**Q1 — CLUBBED partial repayment (HIGH IMPACT):**
One Finance Record covers 5 invoices. If the buyer can only repay 3 of the 5, does the entire Finance Record go OVERDUE? Or can individual invoice allocations in the `finance_record_invoices` junction table be partially settled independently? This determines whether the junction table needs its own state field. **Not resolved by PO.**

**Q2 — Exact trigger for FINANCED:**
Is `invoice.status = FINANCED` set when `Disbursement = SUCCESS`, or when the Finance Record is created? Currently modeled as (b) — Finance Record creation. The two should be atomic, but the ordering matters for failure recovery. **Not explicitly confirmed.**

**Q3 — Portfolio cap UX:**
When `program_disbursement_count ≥ maxDisbursement`, all LODGED invoices in the program become silently ineligible indefinitely. No queuing mechanism or back-office notification is specified. An invoice can remain blocked with no visible reason for the user. **No UX or business rule defined yet.**

---

## 13. What Is In Scope vs Out of Scope

| Feature | Scope |
|---|---|
| Invoice lifecycle management | In scope |
| Buyer-Anchored and Supplier-Anchored programs | In scope |
| Early payment (fixed and dynamic discount) | In scope |
| Request Finance — manual and auto disbursement | In scope — Author's module |
| Payment Gateway integration (sync + async) | In scope — Author's module |
| Finance Record creation | In scope — Author's module (creation only) |
| Repayment engine, penalties, NPA escalation | In scope — Other intern |
| Transaction ledger | In scope |
| Role-based access control (Keycloak) | In scope |
| Document storage (MinIO) | In scope |
| Frontend — React SPA, Transaction Inquiry | In scope |
| Buyer's bank loan management after loan transfer | Out of scope |
| General ledger / core banking integration | Out of scope |
| Currency conversion | Out of scope |
| KYC / AML compliance processes | Out of scope |

---

## 14. Early Payment Detail

**Fixed discount formula:**
```
discount = invoiceAmount × r_annual × (daysEarly / 365)
Example: $100,000 × 8% × (90/365) = $1,973
Buyer pays: $98,027
```

**Dynamic discount formula:**
```
discount = invoiceAmount × r_daily × daysEarly
Example: $100,000 × 0.03% × 30 = $900
Buyer pays: $99,100
```

In early payment, **the buyer earns the discount** as a return for paying early.
In bank financing, **the bank earns the equivalent amount** as interest on capital deployed.
Same arithmetic, completely different parties and legal structures.

No Finance Record is created in early payment. No Disbursement is created. Invoice → MANUALLY_PAID. Transaction(EARLY_PAYMENT) created.