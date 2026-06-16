# PROJECT CONTEXT
This an Ai generated readme file, i will be correcting if there are some false information, you will find a paragraphe that begins with "Corrected:", the correct the previous concept above it.
## 1. Project Overview

The platform is a **Supply Chain Finance (SCF) and Trade Finance** system built for Moroccan and North African banks. It digitises the financing of trade receivables and payables between corporate anchors (large buyers or sellers) and their counterparties (suppliers, distributors, SMEs). Core use-cases include reverse factoring, dynamic discounting, receivables finance, payables finance, and distributor finance — all managed through configurable **programs** that bind an anchor, its counterparties, fee structures, and disbursement rules into a single operational unit.

### Actors and Roles (Keycloak realm `adria-scf`)

| Code name | View | Capabilities |
|---|---|---|
| `scf_bank_admin` | BANK | Full platform administration, product definition, program creation, master data, control centre |
| `scf_bank_officer` | BANK | Operational oversight, transaction inquiry, document inquiry |
| `scf_bank_maker` | BANK | Creates and modifies records (counterparties, programs, invoices, disbursements) — cannot approve own changes |
| `scf_bank_checker` | BANK | Approves or rejects records created by a maker — cannot approve own records |
| `scf_anchor_admin` | ANCHOR | Manages anchor-side operations, uploads invoices, views programs |
| `scf_anchor_user` | ANCHOR | Submits invoices, requests early payment, views transactions |
| `scf_counterparty_user` | COUNTERPARTY | Views own invoices, requests payment, tracks disbursements |

Role resolution is performed in the frontend by `businessViewFromRoles.ts`, which inspects the `realm_access.roles` array in the JWT and returns one of three business views: **BANK**, **ANCHOR**, or **COUNTERPARTY**. The sidebar, dashboard cards, and available actions adapt dynamically to this view.

### Development State

The project is in active development. SpringDoc OpenAPI auto-generates the Swagger specification at runtime from controller annotations (no static Swagger YAML). The docker-compose stack provisions all infrastructure services locally for development.
Corrected : in each spring there is a jira ticket to define clearly the endpoints that we will be working on, meaning, updating the swagger file or creating a new one. that swagger is shared with the team. In general our tech lead was doing this task.

### Multi-Tenant Ambition

The gateway's `environments` directory contains per-bank configuration profiles for **AWB** (Attijariwafa Bank), **BCP** (Banque Centrale Populaire), **BMCI**, **CAM** (Crédit Agricole du Maroc), **SGABS** (Société Générale), **UIB** (Union Internationale de Banques), and an **IBM** integration profile. Each profile overrides the Keycloak realm, database URL, MinIO bucket, and branding properties. The audit service's `TenantAwareRoutingSource` extends `AbstractRoutingDataSource`, routing database operations to a tenant-specific datasource resolved from the JWT `tenant_id` claim via `TenantResolver`.
Corrected: You only need to know these following information. When a team starts a new project or product we follow something called Adria standard. they are standard services that we work with, in general Spring cloud services that are pre configured, with many env. for the audit service, actually this a new and compilcated concept that another team is working on, of course this out of my scope, but as I said we are working with many tools and standards that are already there. and this audit service gonna become one of the standard that all adria's products gonna work with it.

---

## 2. Microservices Architecture

| Service | Role | Tech | Port |
|---|---|---|---|
| **adria-scf-service** | Core SCF business logic — counterparty onboarding, program configuration, product definitions, invoice/cashflow management, document storage | Spring Boot (blocking/servlet), JPA/Hibernate, PostgreSQL, MinIO client, Gotenberg client | 8082 |
| **adria-scf-entities** | Shared JPA entity library consumed by adria-scf-service | JPA annotations only, no runtime | — |
| **adria-gateway2-service** | API Gateway — routing, security, antivirus scanning, brute-force protection, maintenance mode, audit, circuit breaking | Spring Cloud Gateway (reactive/WebFlux), Resilience4j, Caffeine cache | 8085 |
| **adria-audit-api** | Cross-cutting audit module — event capture via AOP, dual persistence (RabbitMQ / direct), hash-chain integrity, multi-tenant data routing | Spring Boot, RabbitMQ, JPA, SHA-256 hashing | — |
| **foundation-data-library-service** | Reference/master data CRUD — countries, cities, states, currencies, bank directories, transaction reference generation | Spring Boot (blocking), JPA, PostgreSQL | 8083 |
| **foundation-data-library-entities** | Shared JPA entity library for FDL | JPA annotations only | — |
| **adria-properties-service** | Runtime property/feature-toggle management — stores key-value properties grouped by module, cached with TTL | Spring Boot, JPA, PostgreSQL | 8084 |
| **adria-registry-service** | Netflix Eureka Server for service discovery | Spring Cloud Netflix Eureka | 8761 |
| **adria-config-service** | Spring Cloud Config Server — centralised external configuration from Git or native filesystem | Spring Cloud Config | 8888 |
| **trade-ui-service** | React SPA — Vite, TypeScript, Shadcn UI, React Router v6, React Query, Axios | Vite + React 18 | 5173 |

### Gateway Routing

`AuthorizedPathsConfiguration` defines public paths (`/actuator/**`, `/eureka/**`, system status). All other requests are JWT-validated via `SecurityContextWebFlux` against the Keycloak JWKS endpoint. Routes configured in YAML:

- `/scf/**` → `lb://adria-scf-service` (StripPrefix=1)
- `/fdl/**` → `lb://foundation-data-library-service` (StripPrefix=1)
- `/properties/**` → `lb://adria-properties-service` (StripPrefix=1)

The `lb://` prefix triggers Eureka-based load-balanced routing. Each route has a circuit-breaker fallback handled by `FallBackController`, which returns a structured error when a downstream service is unavailable.

### Service Discovery

All services register with the Eureka server at `http://localhost:8761`. The registry runs with self-preservation disabled (`enableSelfPreservation: false`) for development.

### Centralised Configuration

Microservices fetch their configuration from the Config Server (`http://localhost:8888`) at startup via their `bootstrap.yml`. The Config Server reads configuration files from either a Git repository or a local native directory.

### Properties Service

`adria-properties-service` exposes REST endpoints (`GET/PUT /properties`, `GET /properties/group/{groupName}`) for managing runtime-configurable key-value properties. Example groups: `scf.fees`, `scf.validation`, `gateway.maintenance`, `audit.config`. Values are stored in PostgreSQL with caching. No maker/checker governance — direct updates.

---

## 3. SCF Domain — Entities and Data Model

All SCF entities extend `BaseEntity`, which provides via `@MappedSuperclass`: **id** (UUID, auto-generated), **createdBy**/**createdDate**/**lastModifiedBy**/**lastModifiedDate** (JPA auditing), **version** (optimistic locking via `@Version`), and the maker/checker governance fields: **approvalStatus** (`ApprovalStatus`), **pendingAction** (`PendingAction`), **makerUser**, **checkerUser**, **checkerComments**.

### Core Entities

**ScfCounterParty** — a corporate, individual, or SME entity participating in trade finance (supplier, buyer, or both). Key fields: `companyName`, `legalName`, `counterPartyType`, `counterPartyRole`, `counterPartyStatus`, `taxId`, `registrationNumber`, contact/address fields, `originalData` (JSON snapshot for rollback). One-to-many to `ScfBankAccount` (bank details with `bankName`, `accountNumber`, `iban`, `swiftCode`, `currency`, `isPrimary` flag) and `ScfCounterPartyDocument` (uploaded files with `documentName`, `documentType`, `filePath` in MinIO, `fileSize`, `contentType`, `bucketName`).

**ScfAnchor** — the large corporate (buyer or seller) that anchors a financing program. Fields: `anchorName`, `anchorCode`, `anchorRole`, `taxId`, contact/address fields. One-to-many to `ScfProgramAnchor`.

**ScfProductDefinition** — a reusable product template. Fields: `productName`, `productCode` (unique), `productType`, `underlyingInstrument`, `description`, `productDefinitionStatus`, `originalData`.

**ScfProgramConfiguration** — a concrete financing program. Fields: `programName`, `programReference` (unique), `programDescription`, `programStatus`, `productType`, `currency`, `startDate`/`endDate`, `maxFinanceAmount`, `maxFinancePercentage`, `disbursementMethod`, `repaymentMethod`, `autoApproveThreshold`, `gracePeriodDays`, `penaltyRate`, `earlyPaymentDiscountRate`, `originalData`. One-to-many to `ScfProgramAnchor`, `ScfProgramCounterParty`, `ScfProgramFeeCatalogue`, `ScfProgramCashflow`.

**ScfProgramAnchor** — junction linking a program to an anchor with a program-specific `anchorRole`.

**ScfProgramCounterParty** — junction linking a program to a counterparty with `counterPartyRole`, `creditLimit`, and `borrowerRole`.

**ScfProgramFeeCatalogue** — fee configuration for a program. `feeDescription` plus two JSON-serialized structures: `feeItems` (List of `ProgramFeeItem` via `FeeItemsJsonConverter` — each item has `feeType`, `calculationBasis`, `rate`, `flatAmount`, `currency`, `frequency`) and `flatFeeConfig` (`FlatFeeConfig` via `FlatFeeConfigJsonConverter` — `flatFeeAmount`, `flatFeeCurrency`, `flatFeeFrequency`, `flatFeeDescription`).

**ScfProgramCashflow** — an invoice/cashflow entry within a program. Fields: `invoiceNumber`, `supplierName`, `buyerName`, `invoiceAmount`, `currency`, `invoiceDate`, `dueDate`, `paymentTerms`, `description`, `validationStatus` (VALID/ERROR/WARNING), `validationErrors`/`validationWarnings` (JSON arrays), `originalData`.

### Enums

| Enum | Values |
|---|---|
| `AnchorRole` | BUYER, SELLER, DISTRIBUTOR |
| `BorrowerRole` | PRIMARY_BORROWER, CO_BORROWER, GUARANTOR |
| `CounterPartyRole` | BUYER, SELLER, BOTH |
| `CounterPartyType` | CORPORATE, INDIVIDUAL, SME |
| `CounterPartyStatus` | DRAFT, PENDING_APPROVAL, APPROVED, REJECTED, ACTIVE, SUSPENDED, CLOSED |
| `ApprovalStatus` | DRAFT, PENDING_APPROVAL, APPROVED, REJECTED |
| `PendingAction` | NONE, CREATE, UPDATE, DELETE |
| `ProgramStatus` | DRAFT, PENDING_APPROVAL, APPROVED, REJECTED, ACTIVE, SUSPENDED, CLOSED |
| `ProductType` | REVERSE_FACTORING, DYNAMIC_DISCOUNTING, RECEIVABLES_FINANCE, PAYABLES_FINANCE, DISTRIBUTOR_FINANCE |
| `ProductDefinitionStatus` | DRAFT, PENDING_APPROVAL, APPROVED, REJECTED, ACTIVE, DEPRECATED |
| `UnderlyingInstrument` | INVOICE, PURCHASE_ORDER, BILL_OF_EXCHANGE, PROMISSORY_NOTE, LETTER_OF_CREDIT |
| `Currency` | MAD, USD, EUR, GBP, CHF, SAR, AED, TND, EGP, XOF |

---

## 4. SCF Service — Backend Business Modules

### 4.1 Counterparty Module

**CounterPartyController** (`/scf/counterparties`) exposes: paginated list with filtering (GET), single fetch (GET `/{id}`), create (POST), update (PUT `/{id}`), delete (DELETE `/{id}`), submit for approval (PUT `/{id}/submit`), approve (PUT `/{id}/approve`), reject with reason (PUT `/{id}/reject` with `RejectCounterPartyRequest`), bulk create (POST `/bulk` with `ScfCounterPartyBulkCreateRequest`), and CSV export (GET `/export`). All endpoints secured with `@PreAuthorize` checking `scf_bank_admin`, `scf_bank_maker`, `scf_bank_checker`.

**Onboarding workflow**: A bank maker creates a counterparty in DRAFT status with company details, tax/registration IDs, contact info, address, and bank accounts. The maker submits for approval → status becomes PENDING_APPROVAL, `pendingAction` set to CREATE. A different bank checker reviews and either approves (status → APPROVED) or rejects with comments (status → REJECTED). `GovernanceSpecifications.excludeOwnPendingRecords(currentUser)` prevents a maker from seeing their own pending records in the checker's approval queue.

**CounterPartyDocumentController** (`/scf/counterparties/{counterPartyId}/documents`) handles: upload (POST, multipart — stores file in MinIO via `ObjectStoragePort`, saves `ScfCounterPartyDocument` metadata), list (GET), view with presigned URL (GET `/{docId}/view` → `DocumentViewResult`), download stream (GET `/{docId}/download`), and delete (DELETE `/{docId}`).

**Exceptions**: `CounterPartyAlreadyExistsException` (duplicate taxId/registrationNumber), `CounterPartyCsvExportException` (CSV generation failure), `CounterPartyDocumentNotFoundException`, `CounterPartyDocumentValidationException` (unsupported format or size limit).

### 4.2 Program Configuration Module

**ProgramConfigurationController** (`/scf/programs`) exposes: paginated list with filtering by status/productType/search (GET), single fetch (GET `/{id}`), create (POST with `ProgramGeneralRequest`), update (PUT `/{id}` with `ProgramGeneralUpdateRequest`), delete (DELETE `/{id}`), submit/approve/reject lifecycle endpoints, copy (POST `/{id}/copy` with `ProgramCopyRequest`), list anchors (GET `/anchors`), and add anchor/counterparty to program.

**Program creation flow**: The `ProgramGeneralRequest` carries general info (name, reference, dates, currency, finance limits), anchor assignment (`ScfProgramAnchorCreate` with anchorId and role), counterparty list (`ScfProgramCounterPartyCreate` with counterPartyId, role, creditLimit, borrowerRole), and fee catalogues. `ProgramConfigurationService.createProgram()` validates, maps via `ProgramConfigurationMapper`, persists with DRAFT status.

**Fee catalogue**: `ScfProgramFeeCatalogue` stores `feeItems` (List of `ProgramFeeItem` — each with feeType, calculationBasis, rate, flatAmount, currency, frequency) and `flatFeeConfig` as JSON columns via JPA converters. `FeeCatalogueUpdateController` (`/scf/programs/{programId}/fee-catalogue`) manages updates and retrieval through `FeeCatalogueUpdateService`.

**Cashflow/invoice submission**: `CashflowUpdateController` (`/scf/programs/{programId}/cashflow`) accepts `ProgramCashflowRequest` containing invoice details. `CashflowUpdateService` validates: duplicate invoice numbers, date range validity (invoiceDate ≤ dueDate), positive amounts. Each entry is stored as a `ScfProgramCashflow` entity with `validationStatus`, `validationErrors`, and `validationWarnings`.

**ProgramSnapshotService**: Deep-copies a program via `snapshotProgram(UUID, newName, newReference)` — duplicates the configuration and all sub-entities (anchors, counterparties, fee catalogues) but excludes cashflows. The copy starts in DRAFT status. Used by the copy feature (`ProgramCopyRequest` → `ProgramCopiedResponse`).

**Maker/Checker**: On update, `OriginalDataRestorer` serialises the current entity state to the `originalData` JSON field. On rejection, `OriginalDataRestorer` deserialises and restores the entity to its pre-modification state. `GovernanceSpecifications` enforces at the repository query level that a maker cannot approve their own pending changes.

### 4.3 Product Definition Module

`ScfProductDefinition` is a reusable template defining a financing product (e.g., "Reverse Factoring — Invoice"). It differs from `ScfProgramConfiguration` in that a product is a generic template while a program is a concrete operational instance bound to a specific anchor, counterparties, and fee structure. `ProductType` enumerates the five SCF product families. `UnderlyingInstrument` specifies the financial instrument backing the product (invoice, purchase order, bill of exchange, promissory note, letter of credit). `ScfProductDefinitionServiceImpl` handles CRUD with maker/checker lifecycle and validates `productCode` uniqueness.

### 4.4 Storage and Document Conversion

The **hexagonal architecture** (port/adapter) cleanly separates storage concerns. `ObjectStoragePort` defines six operations: `uploadFile`, `downloadFile`, `deleteFile`, `getPresignedUrl`, `bucketExists`, `createBucket`. `MinioObjectStorageAdapter` implements this port using the MinIO Java SDK (`MinioClient`). Configuration via `MinioStorageConfig` (`minio.endpoint`, `minio.accessKey`, `minio.secretKey`, `minio.bucketName`). `ObjectStorageType` enum anticipates future S3 support.

**Gotenberg** is an open-source document conversion service. `DocumentConverterPort` defines `convertToPdf` and `convertToImage`. `GotenbergDocumentConverterAdapter` POSTs documents to Gotenberg's LibreOffice conversion endpoint (`/forms/libreoffice/convert`) for DOCX/XLSX-to-PDF conversion. Configured via `gotenberg.url` in `DocumentConverterConfiguration`.

### 4.5 Security and Governance

`SecurityConfig` configures Spring Security as a stateless OAuth2 resource server. JWT validation uses the Keycloak JWKS endpoint (`spring.security.oauth2.resourceserver.jwt.issuer-uri`). CSRF is disabled; CORS allows the frontend origin. Public paths: `/actuator/**`, `/swagger-ui/**`, `/v3/api-docs/**`.

`KeycloakJwtAuthenticationConverter` extracts roles from `realm_access.roles` and `resource_access.<clientId>.roles` JWT claims, prefixes each with `ROLE_`, and wraps them as `SimpleGrantedAuthority` instances in a `JwtAuthenticationToken`.

`GovernanceSpecifications` provides static JPA Specification builders: `excludeOwnPendingRecords(currentUser)` ensures a maker's pending records are excluded from the checker's view; `filterByApprovalStatus` and `filterByPendingAction` enable dynamic query filtering.

`OriginalDataRestorer` serialises entity state to JSON before modification (stored in `originalData` column) and deserialises it back on rejection, enabling full rollback of maker changes.

---

## 5. Gateway — Cross-cutting Concerns

| Filter | Responsibility |
|---|---|
| **GatewayAntivirusFilter** | Intercepts `multipart/form-data` uploads, extracts file bytes, sends to ClamAV via TCP socket. If malware detected ("FOUND" response), returns HTTP 400. Configurable pass-through if ClamAV is unreachable. |
| **CacheBodyForBruteforceFilter** + **AttemptHandlerService** | Caches login request bodies. `BruteforceIdentifierResolver` identifies callers by IP + username. `AttemptHandlerService` tracks failed attempts in a Caffeine cache; if `maxAttempts` (default 5) exceeded within the window, returns HTTP 429 with `Retry-After` header. Resets on success. |
| **MaintenanceFilter** + **MaintenanceService** | If `gateway.maintenance.enabled = true`, blocks all requests except `allowedPaths` with HTTP 503 and a configurable message. Dynamically toggleable at runtime. |
| **RequestLoggingFilter** | Logs method, URI, sanitised headers, client IP, timestamp on request; status code and response time (ms) on response. Does not log bodies. |
| **TokenTppFilter** | Validates `X-TPP-Token` header against a TPP registry/whitelist for Open Banking third-party providers. Returns HTTP 403 if invalid. |
| **GatewaySeparatorFilter** | Adds `X-Request-Id` correlation header (UUID) if absent; propagates through the chain and into the response for distributed tracing. |
| **RequestRecordFilter** | Captures request metadata (timestamp, IP, URI, method, user agent, authenticated user) and forwards as headers to downstream services for audit integration. |
| **UnauthorizedPathsGatewayFilterFactory** | Factory-created filter that blocks access to configured internal-only path patterns with HTTP 403. |

---

## 6. Audit Service — Compliance and Traceability

**Event capture**: `@AuditEvent(value, module, level)` on methods triggers `AuditEventAspect` (`@Around`), which captures method name, parameters (those annotated with `@AuditPayload` are serialised via `AuditPayloadAspect`), user, IP, execution time, result or exception. Constructs `AuditEventPayload`.

**Dual persistence**: `AuditParametrage` per module configures `persistenceStrategy` — either `RabbitMQPersistenceStrategy` (publishes to `audit.exchange` with routing key `audit.{tenantId}`, consumed asynchronously) or `DirectPersistenceStrategy` (synchronous JPA save). The RabbitMQ path decouples audit capture from persistence and absorbs traffic spikes.

**Insertion strategies**: `SingleInsertionStrategy` persists each event individually. `BatchInsertionStrategy` buffers events and flushes on batch-size threshold or timeout, using an `@Async` thread pool from `AuditAsyncConfig`.

**Retention strategies**: `ArchiveDbRetentionStrategy` moves logs older than `retentionDays` to `audit_log_archive` table via scheduled job. `ArchiveFileRetentionStrategy` exports to file (CSV/JSONL) and deletes from the main table; files named `audit_archive_{tenantId}_{date}.{format}`.

**Export**: `CsvExportStrategy` and `JsonlExportStrategy` convert `List<AuditLogEntity>` to downloadable byte arrays.

**Multi-tenancy**: `TenantAwareRoutingSource` extends `AbstractRoutingDataSource`, resolving the current tenant via `TenantResolver` (extracts `tenant_id` from JWT or derives from realm). Each bank has its own datasource.

**Integrity verification**: `HashUtil.computeHash()` produces SHA-256 of eventName + module + userId + timestamp + payload. Each `AuditLogEntity` stores `hashValue` and `previousHash` (chain). `AuditVerificationService` recomputes hashes and validates the chain to detect tampering.

**AuditParametrage** configures per module: `moduleName`, `auditLevel` (minimum capture level), `retentionDays`, `retentionStrategy`, `insertionStrategy`, `persistenceStrategy`, `exportFormat`, `batchSize`, `isActive`.

**Entity-level tracking**: `AuditTrailEntityListener` intercepts `@PrePersist`/`@PreUpdate`/`@PreRemove` JPA callbacks, captures before/after field values, and delegates to `AuditTrailCollector`, which batches changes and sends to the audit service at transaction commit.

---

## 7. Foundation Data Library — Reference Data

**BankDirectory**: Represents financial institutions. `BankDirectoryController` (`/fdl/bank-directory`) provides full CRUD with maker/checker. Fields include `institutionName`, `swiftCode` (unique), `institutionType` (COMMERCIAL_BANK, INVESTMENT_BANK, CENTRAL_BANK, DEVELOPMENT_BANK, MICROFINANCE, CREDIT_UNION, OTHER), `operationalStatus` (ACTIVE, INACTIVE, MERGED, LIQUIDATED). `BankDirectoryBulkController` (`/fdl/bank-directory/bulk`) handles CSV/Excel bulk upload (`BulkUploadResultDto` returns success/failure counts with per-row errors) and template download.

**CityMaster**, **CountryMaster**, **StateMaster**, **CurrencyMaster**: Standard reference data tables with full CRUD and maker/checker governance. `CityMaster` links to `StateMaster` and `CountryMaster` via `@ManyToOne`. `CurrencyMaster` has a `CurrencyMasterStatus` enum (ACTIVE, INACTIVE, DEPRECATED).

**Transaction Reference Generation**: `TransactionReferenceConfigController` (`/fdl/transaction-reference/config`) manages reference format configurations — each config specifies `prefix`, `separator`, `sequenceLength`, `sequenceSeed`, `dateFormat`, `moduleCode`. `TmTransactionRefConfigDraft` holds pending changes; on approval, data copies to `TmTransactionRefConfigData`. `TransactionReferenceRuntimeController` (`/fdl/transaction-reference/runtime`) generates the next reference: `TransactionReferenceRuntimeService` reads the config for the given `moduleCode`, increments `TmTransactionRefSequence.currentSequence` atomically (`@Lock(PESSIMISTIC_WRITE)`), and formats: `{prefix}{separator}{date}{separator}{paddedSequence}` (e.g., `INV-20260612-00001`).

---

## 8. Frontend Architecture (React/Vite/TypeScript)

### 8.1 Application Structure and Routing

`App.tsx` uses React Router v6 with three routes: `/auth` → `Auth`, `/` → `Index` (wrapped in `AuthGuard`), `/specification-document` → `SpecificationDocument` (wrapped in `AuthGuard`). The app wraps in `KeycloakAuthProvider`, `QueryClientProvider` (React Query), `Toaster` (Sonner), and `TooltipProvider`.

`Index.tsx` renders `AppSidebar` plus a content area driven by `selectedModule` state: `"dashboard"` → `SCFDashboard`, `"master-setup"` → `SCFMasterSetup`, `"transaction-inquiry"` → `SCFTransactionInquiry`, `"document-inquiry"` → `DocumentInquiry`, `"invoice-upload"` → `InvoiceUploadForm`, `"invoice-form"` → `InvoiceForm`, `"finance-disbursement"` → `FinanceDisbursementModal`, `"early-payment"` → `EarlyPaymentRequestModal`, `"notifications"` → `NotificationsPanel`.

`AuthGuard` checks `useAuth().isAuthenticated`; if loading shows spinner, if unauthenticated redirects to `/auth`. `AppSidebar` menu items filter by `visibleTo` arrays tied to the `businessView` (BANK sees all; ANCHOR sees dashboard, transaction inquiry, invoice upload/form, early payment; COUNTERPARTY sees dashboard, transaction inquiry, early payment).

`useBusinessView` calls `useAuth()` for roles then `getBusinessViewFromRoles()`, returning `businessView`, `isBank`, `isAnchor`, `isCounterparty`.

### 8.2 Feature Modules

**SCF Dashboard** — Summary cards (programs, counterparties, invoices, finance stats), quick-action buttons, recent activity timeline. Data is currently hardcoded demo data.

**SCF Master Setup** — Tab container for Product Suite, Program Configuration, Counterparty Onboarding, Foundational Data, and Control Centre. Tabs visibility is role-gated.

**Product Suite** — Data table of product definitions with create/edit via `SCFProductDefinition` dialog (fields: productName, productCode, productType, underlyingInstrument, description). `ProductSolutionToggle` filters by product family.

**Program Configuration** — `SCFProgramConfiguration` lists programs with status-based actions. `ProgramFormDialog` is a three-step wizard: `GeneralPartyPane` (program details, anchor selection, counterparty linking via `CounterPartySearchDialog`) → `FeeCataloguePane` (dynamic fee item table) → `DisbursementRepaymentPane` (disbursement/repayment rules). State managed by `useProgramForm` hook.

**Counterparty Onboarding** — `SCFCounterPartyOnboarding` provides CRUD table, inline create/edit form (company details, bank accounts, documents via `DocumentUploadPopup`), maker/checker actions, bulk create, CSV export.

**Invoice Upload** — `InvoiceUploadForm` orchestrates `ExcelInvoiceUploader` (drag-drop .xlsx/.xls), `ScannedInvoiceUploader` (images/PDFs triggering OCR), `InvoiceUploadTable` (validation status per row), `ValidationSummaryCard` (aggregate stats), `DisbursementStatusCard` (eligibility summary), `RejectionReportDownloader`.

**Invoice Form** — Manual invoice entry via `InvoiceForm` with `InvoiceGeneralDetailsPane`, `InvoiceLineItemsPane` (dynamic line items with auto-calculation), `InvoiceSummaryPane`, `InvoiceFormActions`. State via `useInvoiceForm` hook.

**Early Payment** — `EarlyPaymentRequestModal` with `EarlyPaymentRequestForm` (requestedPaymentDate, discountAccepted, calculated discount and net amount).

**Finance & Disbursement** — `FinanceDisbursementModal` six-step wizard: `ProgramProductSelectionPane` → `InvoiceSelectionPane` (checkbox selection of eligible invoices) → `FinanceDetailsPane` (finance terms, fee breakdown) → `AccountingEntriesPane` (auto-generated debit/credit entries) → `RepaymentDetailsPane` (schedule) → `ReviewSubmitPane`.

**Transaction Inquiry** — `SCFTransactionInquiry` with filter panel and `SCFTransactionInquiryTable`. Row actions open `InvoiceViewModal` or `FinanceDisbursementViewModal`.

**Document Inquiry** — `DocumentInquiry` page with filters; `DocumentUploadPopup` for uploading; `DocumentUploadDetails` for viewing/downloading.

**Control Centre** — `FieldDefinition` (custom field CRUD), `FieldActionsTab` (field-level action rules), `ManagePanesAndSections` (drag-drop layout configuration), `ProductEventMapping` (event-to-product mapping rules).

**Foundational Data** — `CityMaster`, `CountryMaster`, `CurrencyMaster`, `StateMaster` CRUD tables with maker/checker actions.

### 8.3 Services Layer

Each service file creates typed functions over the shared `apiClient` (Axios instance from `gateway/client.ts`). Endpoint prefixes: `/scf/` for SCF backend, `/fdl/` for FDL backend. Key mappings: `scfCounterPartyService` → `/scf/counterparties`, `scfProgramConfigService` → `/scf/programs`, `scfProductService` → `/scf/products`, `invoiceUploadService` → `/scf/invoices/upload`, `financeDisbursementService` → `/scf/finance/disbursements`, `earlyPaymentService` → `/scf/early-payments`, `scfTransactionInquiryService` → `/scf/transactions/inquiry`, `documentInquiryService` → `/scf/documents`, `notificationService` → `/scf/notifications`, `cityMasterService` → `/fdl/cities`, `countryMasterService` → `/fdl/countries`, `currencyMasterService` → `/fdl/currencies`, `stateMasterService` → `/fdl/states`.

### 8.4 Keycloak Integration

Full PKCE-based OIDC flow: `oidcConfig.ts` reads `VITE_KEYCLOAK_URL`, `VITE_KEYCLOAK_REALM` (`adria-scf`), `VITE_KEYCLOAK_CLIENT_ID` (`scf-frontend`), `VITE_REDIRECT_URI`. `keycloakAuthBridge.login()` constructs the authorization URL with PKCE code_challenge and redirects. `Auth.tsx` handles the callback — exchanges the code for tokens via `keycloakAuthBridge.handleCallback()`, stores access/refresh tokens in `sessionStorage`. `KeycloakAuthProvider` decodes the JWT on mount, extracts user info via `keycloakUserBridge.getUserFromToken()` (sub, preferred_username, email, names, realm_access.roles). `gateway/client.ts` Axios request interceptor reads the token from sessionStorage and sets `Authorization: Bearer <token>`. On 401, the response interceptor attempts token refresh; on failure triggers logout.

### 8.5 TypeScript Types

**invoiceUpload.ts**: `InvoiceUploadFile` (id, fileName, fileSize, uploadDate, status), `InvoiceUploadRow` (rowNumber, invoiceNumber, supplier/buyer, amount, currency, dates, validationStatus with VALID/WARNING/ERROR, validationErrors/Warnings arrays), `InvoiceUploadResult` (fileId, totalRows, valid/warning/errorRows, rows), `DisbursementEligibility` (eligible/ineligible amounts and counts, reasons).

**scfTransaction.ts**: `SCFTransaction` (id, transactionReference, transactionType — INVOICE/FINANCE_DISBURSEMENT/REPAYMENT/EARLY_PAYMENT/FEE, program details, counterparty, amount, currency, status — DRAFT through SETTLED/CANCELLED, dates). `FinanceDisbursement` (program/product details, invoiceIds, finance terms, fees as `FeeBreakdown[]`, accountingEntries as `AccountingEntry[]` with DEBIT/CREDIT, repaymentSchedule as `RepaymentEntry[]`, approvalHistory as `ApprovalHistoryEntry[]`).

---

## 9. End-to-End Business Flows

### 9.1 Authentication Flow

User navigates to `/` → `AuthGuard` detects no token → redirects to `/auth` → `Auth.tsx` calls `keycloakAuthBridge.login()` → browser redirects to Keycloak authorization endpoint (PKCE) → user authenticates → Keycloak redirects to `/auth?code=…` → `Auth.tsx` calls `keycloakAuthBridge.handleCallback(code)` → POST to Keycloak token endpoint → receives access_token, refresh_token → stored in sessionStorage → `KeycloakAuthProvider` decodes JWT → `keycloakUserBridge.getUserFromToken()` extracts roles → `useBusinessView` calls `getBusinessViewFromRoles(roles)` → sidebar and dashboard adapt to BANK/ANCHOR/COUNTERPARTY view.

### 9.2 Counterparty Onboarding Flow

Bank maker opens `SCFCounterPartyOnboarding` → fills company details, bank accounts, uploads documents via `DocumentUploadPopup` → calls `scfCounterPartyService.createCounterParty()` → POST `/scf/counterparties` → gateway routes to `adria-scf-service` → `CounterPartyController.create()` → service validates, persists `ScfCounterParty` (DRAFT) → maker clicks Submit → `scfCounterPartyService.submitForApproval(id)` → PUT `/scf/counterparties/{id}/submit` → status → PENDING_APPROVAL → bank checker views pending list (filtered by `GovernanceSpecifications.excludeOwnPendingRecords`) → approves → PUT `/scf/counterparties/{id}/approve` → status → APPROVED → counterparty active.

### 9.3 Program Creation Flow

Bank maker opens `ProgramFormDialog` → `GeneralPartyPane`: sets program name/reference, selects productType, picks anchor via search, adds counterparties via `CounterPartySearchDialog`, sets finance limits and dates → `FeeCataloguePane`: adds fee items (type, rate, flat amount, frequency) → `DisbursementRepaymentPane`: configures disbursement/repayment methods, thresholds, rates → submit → `useProgramForm` constructs `ProgramGeneralRequest` → `scfProgramConfigService.createProgram()` → POST `/scf/programs` → `ProgramConfigurationController.create()` → `ProgramConfigurationService.createProgram()` → maps via `ProgramConfigurationMapper`, persists `ScfProgramConfiguration` with sub-entities → DRAFT status → submit/approve lifecycle.

### 9.4 Invoice Upload and Validation Flow

User opens `InvoiceUploadForm` → drags Excel file into `ExcelInvoiceUploader` → `invoiceUploadService.uploadExcelInvoices(programId, file)` → POST `/scf/invoices/upload/excel` (multipart) → gateway antivirus scan (ClamAV) → routes to `adria-scf-service` → `CashflowUpdateController` processes file → `CashflowUpdateService` parses rows, validates (duplicate invoice numbers, date ranges, positive amounts) → creates `ScfProgramCashflow` entries with `validationStatus` → response displayed in `InvoiceUploadTable` → `ValidationSummaryCard` shows totals → user submits valid invoices for approval → maker/checker flow via `invoiceValidationService`.

### 9.5 Finance Disbursement Flow

Bank officer opens `FinanceDisbursementModal` → `ProgramProductSelectionPane`: selects program and product (fetched via `scfProgramConfigService`) → `InvoiceSelectionPane`: loads eligible invoices via `invoiceDisbursementService.getInvoicesForDisbursement(programId)`, user selects invoices → `FinanceDetailsPane`: sets finance terms (amount, dates, rates), fee breakdown auto-populated from program's fee catalogue → `AccountingEntriesPane`: auto-generated debit/credit entries displayed read-only → `RepaymentDetailsPane`: configures repayment schedule → `ReviewSubmitPane`: final review → submit → `financeDisbursementService.createDisbursement()` → POST `/scf/finance/disbursements` → backend processes → DRAFT → submit/approve lifecycle.

### 9.6 Document Upload and Storage Flow

User opens `DocumentUploadPopup` → selects file and document type → `specificationDocumentService.uploadDocument()` or `scfCounterPartyService.uploadDocument()` → POST multipart → gateway `GatewayAntivirusFilter` scans via ClamAV → routes to `CounterPartyDocumentController.upload()` → service calls `ObjectStoragePort.uploadFile()` → `MinioObjectStorageAdapter` uses `minioClient.putObject()` to store in MinIO bucket → `ScfCounterPartyDocument` entity created with `filePath`, `bucketName`, `contentType` in PostgreSQL → document retrievable via presigned URL (`getPresignedUrl`) or direct stream (`downloadFile`).

---

## 10. Infrastructure and Deployment

### Docker Compose Services

| Service | Image | Port(s) |
|---|---|---|
| postgres | PostgreSQL 15 | 5432 |
| minio | MinIO | 9000 (API), 9001 (console) |
| keycloak | Keycloak 22 | 8080 |
| rabbitmq | RabbitMQ 3 management | 5672 (AMQP), 15672 (UI) |
| clamav | ClamAV | 3310 |
| gotenberg | Gotenberg | 3000 |
| eureka | adria-registry-service | 8761 |
| config-server | adria-config-service | 8888 |
| gateway | adria-gateway2-service | 8085 |
| scf-service | adria-scf-service | 8082 |
| fdl-service | foundation-data-library-service | 8083 |
| properties-service | adria-properties-service | 8084 |
| audit-service | adria-audit-api | — |

All services communicate over a `scf-network` Docker bridge network.

### Multi-Bank Deployment

The gateway's `environments` directory contains per-bank profiles (AWB, BCP, BMCI, CAM, IBM, SGABS, UIB). Each `application-{bank}.yml` overrides: Keycloak realm, database URL, MinIO bucket name, branding, and maintenance messages. Activated via `spring.profiles.active`. Combined with `TenantAwareRoutingSource` in the audit service (which routes to tenant-specific datasources resolved from JWT claims), the platform supports full multi-bank isolation — each institution operates on its own database schema with its own Keycloak realm, while sharing the same deployed codebase.

### Environment-Specific Configuration

Microservices load configuration in order: embedded `application.yml` → Config Server overrides (per-profile) → environment variables. The Config Server reads from a Git repository or native filesystem. Per-bank gateway profiles provide the final layer of bank-specific customisation.
