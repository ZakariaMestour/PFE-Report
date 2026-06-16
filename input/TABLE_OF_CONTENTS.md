# TABLE OF CONTENTS
# End-of-Studies Project Report
# Supply Chain Finance & Trade Finance Platform
# Adria Business & Technology

---

*Estimated total body pages: 75–80 pages*
*Structure: 5 chapters + General Introduction + General Conclusion*

---

## FRONT MATTER

- Dedication .............................................................. i
- Acknowledgements ................................................... ii
- Abstract (English) ................................................... iii
- Résumé (Français) ................................................... iv
- ملخص (Arabe) ........................................................ v
- Table of Contents .................................................... vi
- List of Figures ........................................................ ix
- List of Tables .......................................................... xi
- List of Acronyms ..................................................... xii

---

## GENERAL INTRODUCTION ......................................... 1
*(~2–3 pages)*

---

## CHAPTER I. PROJECT CONTEXT AND BACKGROUND .............. 4
*(~14 pages)*

**I.1. Introduction** ................................................... 4

**I.2. Host Organization: Adria Business & Technology** .............. 4

- I.2.1. Company Overview and Positioning ............................. 4
- I.2.2. Vision, Mission, and Core Values .............................. 5
- I.2.3. Areas of Expertise ............................................ 5
- I.2.4. Information Sheet ............................................. 6
- I.2.5. Products and Services Portfolio ............................... 6
- I.2.6. Organizational Chart .......................................... 7
- I.2.7. Strategic Partnerships and Clientele .......................... 7

**I.3. General Context of the Project** .................................. 8

- I.3.1. Supply Chain Finance: Domain Overview ......................... 8
    - I.3.1.1. Definition and Business Purpose ......................... 8
    - I.3.1.2. Key SCF Products: Reverse Factoring, Dynamic Discounting, Receivables Finance .... 8
    - I.3.1.3. Actors in the SCF Ecosystem: Anchor, Counterparty, Bank .... 9
- I.3.2. Trade Finance: Complementary Domain .......................... 9
- I.3.3. Problem Statement: Why Digitizing SCF and Trade Finance ....... 10
- I.3.4. Proposed Solution and Platform Ambition ....................... 10
- I.3.5. Multi-Bank and Multi-Tenant Deployment Strategy ............... 11

**I.4. Project Methodology and Management** ............................. 11

- I.4.1. Agile Framework: Scrum at Adria .............................. 11
- I.4.2. Sprint Structure and Jira-based Ticket Management ............. 12
- I.4.3. Developer Role and Contribution Scope (Full Stack) ............ 12
- I.4.4. Tools and Work Environment ................................... 13
    - I.4.4.1. Version Control: Git and Branching Strategy ............. 13
    - I.4.4.2. Project Tracking: Jira ................................ 13
    - I.4.4.3. Collaboration: Confluence, Slack ....................... 13
    - I.4.4.4. Development: IntelliJ IDEA, VS Code .................... 13
- I.4.5. Timeline and Internship Planning (Gantt Diagram) .............. 14

**I.5. Conclusion** ..................................................... 14

---

## CHAPTER II. SYSTEM ARCHITECTURE AND TECHNICAL STACK ..... 15
*(~16 pages)*

**II.1. Introduction** .................................................. 15

**II.2. Overall Architecture: Microservices on Adria Standard** ........ 15

- II.2.1. The Adria Standard: Pre-configured Spring Cloud Services ..... 15
- II.2.2. Microservices Architecture Overview ......................... 16
- II.2.3. Monorepo Organization: Back-end and Front-end Structure ....... 16
- II.2.4. Service Communication and Inter-service Protocols ............ 17

**II.3. Backend Services Deep Dive** .................................... 17

- II.3.1. adria-scf-service: Core Business Logic ...................... 17
    - II.3.1.1. Internal Architecture: Domain-Driven Layered Design .... 17
    - II.3.1.2. Domain Packages: counterparty, product, program ........ 18
    - II.3.1.3. Key Technical Choices: Spring Boot, JPA, MapStruct, Lombok .. 18
- II.3.2. adria-scf-entities: Shared JPA Entity Library ............... 18
- II.3.3. adria-gateway2-service: API Gateway ......................... 19
    - II.3.3.1. Role and Responsibilities ............................. 19
    - II.3.3.2. Routing Configuration: /scf/, /fdl/, /properties/ ..... 19
    - II.3.3.3. Filters Pipeline and Cross-cutting Concerns ............ 19
    - II.3.3.4. Resilience: Circuit Breaker with Resilience4j ......... 20
    - II.3.3.5. Security: Antivirus Scanning, Brute-force Protection, Maintenance Mode .. 20
- II.3.4. foundation-data-library-service: Reference Data ............. 21
- II.3.5. adria-properties-service: Runtime Configuration ............. 21
- II.3.6. adria-registry-service: Service Discovery with Eureka ........ 21
- II.3.7. adria-config-service: Centralized Configuration ............. 22
- II.3.8. adria-audit-api: Compliance and Traceability ................ 22
    - II.3.8.1. AOP-based Event Capture .............................. 22
    - II.3.8.2. Dual Persistence Strategy: RabbitMQ vs Direct ......... 22
    - II.3.8.3. Hash-chain Integrity Verification ..................... 23
    - II.3.8.4. Multi-tenant Data Routing ............................ 23

**II.4. Frontend Architecture** ......................................... 23

- II.4.1. Technology Stack: React 18, Vite, TypeScript ................ 23
- II.4.2. UI Component Library: shadcn/ui and Radix UI ................ 24
- II.4.3. State Management: React Query, Context API, Custom Hooks ..... 24
- II.4.4. Routing Strategy: React Router v6 and AuthGuard ............. 24
- II.4.5. Role-based UI Adaptation: businessViewFromRoles .............. 24

**II.5. Security Architecture** ......................................... 25

- II.5.1. Identity and Access Management with Keycloak ................ 25
- II.5.2. PKCE-based OIDC Authentication Flow ......................... 25
- II.5.3. JWT Validation in the Backend: OAuth2 Resource Server ........ 25
- II.5.4. Role Extraction: KeycloakJwtAuthenticationConverter .......... 26
- II.5.5. Maker/Checker Governance: GovernanceSpecifications ........... 26

**II.6. Data Storage Architecture** ..................................... 26

- II.6.1. PostgreSQL: Schema-per-Service Pattern ...................... 26
- II.6.2. Database Migration with Flyway .............................. 27
- II.6.3. MinIO for Object Storage: Documents and Invoices ............. 27
    - II.6.3.1. Port/Adapter Pattern: ObjectStoragePort and MinioObjectStorageAdapter .... 27
    - II.6.3.2. Document Lifecycle: Upload, Metadata, Presigned URL .... 27
- II.6.4. Document Conversion with Gotenberg .......................... 27

**II.7. Infrastructure and Deployment** ................................. 28

- II.7.1. Containerization with Docker and Docker Compose .............. 28
- II.7.2. Full Docker Compose Stack: Services and Ports ................ 28
- II.7.3. Multi-Bank Deployment Strategy .............................. 28
- II.7.4. Environment-specific Configuration Management ................ 29

**II.8. Conclusion** .................................................... 29

---

## CHAPTER III. SCF DOMAIN: DESIGN AND IMPLEMENTATION ........ 30
*(~18 pages)*

**III.1. Introduction** ................................................. 30

**III.2. SCF Data Model: Entities and Relationships** ................... 30

- III.2.1. BaseEntity: Shared Auditing and Governance Fields ........... 30
- III.2.2. Core Business Entities .................................... 31
    - III.2.2.1. ScfCounterParty and ScfBankAccount ................... 31
    - III.2.2.2. ScfAnchor and ScfProgramAnchor ....................... 31
    - III.2.2.3. ScfProductDefinition ................................ 31
    - III.2.2.4. ScfProgramConfiguration ............................. 32
    - III.2.2.5. ScfProgramCounterParty .............................. 32
    - III.2.2.6. ScfProgramFeeCatalogue, ProgramFeeItem, FlatFeeConfig .. 32
    - III.2.2.7. ScfProgramCashflow .................................. 33
    - III.2.2.8. ScfCounterPartyDocument ............................. 33
- III.2.3. Business Enumerations and Their Significance ............... 33
    - III.2.3.1. CounterPartyStatus and ApprovalStatus Lifecycle ....... 33
    - III.2.3.2. PendingAction: Tracking Maker Intent ................. 34
    - III.2.3.3. ProgramStatus Lifecycle ............................. 34
    - III.2.3.4. ProductType and UnderlyingInstrument ................. 34
    - III.2.3.5. Currency and Other Reference Enums ................... 34
- III.2.4. Entity-Relationship Diagram ................................ 35

**III.3. Maker/Checker Governance Pattern** ............................. 35

- III.3.1. Business Rationale: The Four-Eyes Principle in Banking ...... 35
- III.3.2. Technical Implementation: GovernanceSpecifications .......... 35
- III.3.3. OriginalDataRestorer: Snapshot and Rollback Mechanism ....... 36
- III.3.4. State Machine Diagram: From DRAFT to APPROVED/REJECTED ...... 36

**III.4. Counterparty Module** .......................................... 37

- III.4.1. Business Purpose ........................................... 37
- III.4.2. Counterparty Onboarding Workflow ........................... 37
    - III.4.2.1. Sequence Diagram: Maker Creates, Checker Approves ..... 37
    - III.4.2.2. Bulk Onboarding via CSV Upload ....................... 38
    - III.4.2.3. CSV Export of Counterparty Data ...................... 38
- III.4.3. Document Management for Counterparties ..................... 38
    - III.4.3.1. File Upload Flow: Frontend → Gateway → MinIO .......... 38
    - III.4.3.2. Document Viewing via Presigned URLs ................... 39
    - III.4.3.3. Antivirus Scanning: ClamAV Integration at Gateway Level ... 39
- III.4.4. API Endpoints: CounterPartyController and CounterPartyDocumentController ..... 39

**III.5. Product Definition Module** .................................... 40

- III.5.1. Product vs Program: Key Distinction ....................... 40
- III.5.2. Product Definition Lifecycle .............................. 40
- III.5.3. SCF Product Types Supported ............................... 40

**III.6. Program Configuration Module** ................................. 41

- III.6.1. What a Program Represents ................................. 41
- III.6.2. Program Creation Wizard: Three-Step Frontend Flow ........... 41
    - III.6.2.1. Step 1 – General Party Pane: Program Info and Anchor Selection .. 41
    - III.6.2.2. Step 2 – Fee Catalogue Pane: Dynamic Fee Configuration . 42
    - III.6.2.3. Step 3 – Disbursement and Repayment Rules ............. 42
- III.6.3. Fee Catalogue Structure: FeeItems and FlatFeeConfig ......... 43
- III.6.4. Program Copy Feature: ProgramSnapshotService ............... 43
- III.6.5. Program Lifecycle and Maker/Checker Flow ................... 43
- III.6.6. API Endpoints: ProgramConfigurationController, CashflowUpdateController, FeeCatalogueUpdateController .... 44

**III.7. Invoice Upload and Cashflow Management** ....................... 44

- III.7.1. Excel Invoice Upload: ExcelInvoiceUploader ................. 44
- III.7.2. Scanned Invoice Upload and OCR ............................ 45
- III.7.3. Server-side Validation Rules: CashflowUpdateService ........ 45
- III.7.4. Validation Results Display: InvoiceUploadTable and ValidationSummaryCard .. 45
- III.7.5. Rejection Report Download ................................. 46

**III.8. Transaction Inquiry Module** ................................... 46

- III.8.1. Filtering and Searching Transactions ....................... 46
- III.8.2. Invoice View Modal ........................................ 46
- III.8.3. Finance Disbursement View Modal ........................... 46

**III.9. Conclusion** ................................................... 47

---

## CHAPTER IV. FRONTEND IMPLEMENTATION AND USER FLOWS ........ 48
*(~14 pages)*

**IV.1. Introduction** .................................................. 48

**IV.2. Application Architecture and Navigation** ....................... 48

- IV.2.1. Application Entry Point and Route Structure ................. 48
- IV.2.2. Authentication Flow: From URL to Dashboard .................. 48
    - IV.2.2.1. Sequence Diagram: PKCE OIDC from Browser to Keycloak ... 49
    - IV.2.2.2. Token Storage and Axios Interceptor ................... 49
- IV.2.3. Role-based Sidebar and View Adaptation ...................... 49
- IV.2.4. AppSidebar: Navigation and Module Selection ................. 50

**IV.3. Master Setup Module** ........................................... 50

- IV.3.1. Tab Structure and Role-gated Access ........................ 50
- IV.3.2. Product Suite Management ................................... 51
- IV.3.3. Program Configuration UI .................................. 51
- IV.3.4. Counterparty Onboarding UI ................................. 51
- IV.3.5. Foundational Data Management: Country, City, Currency, State . 52
- IV.3.6. Control Centre: Field Definition and Layout Management ....... 52
    - IV.3.6.1. FieldDefinition: Custom Field CRUD .................... 52
    - IV.3.6.2. FieldActionsTab: Field-level Action Rules .............. 52
    - IV.3.6.3. ManagePanesAndSections: Drag-and-drop Layout ........... 53
    - IV.3.6.4. ProductEventMapping: Event-to-Product Rules ............ 53

**IV.4. Invoice Management Flows** ...................................... 53

- IV.4.1. Invoice Upload Flow: Excel and Scanned ..................... 53
    - IV.4.1.1. Component Interaction Diagram ......................... 53
    - IV.4.1.2. InvoiceUploadForm and its Sub-components ............... 54
- IV.4.2. Manual Invoice Form ........................................ 54
    - IV.4.2.1. useInvoiceForm Hook: State and Validation Logic ........ 54
    - IV.4.2.2. Multi-pane Form: General Details, Line Items, Summary .. 55

**IV.5. Finance and Early Payment Flows** ............................... 55

- IV.5.1. Early Payment Request Flow ................................. 55
    - IV.5.1.1. EarlyPaymentRequestForm: Discount Calculation .......... 55
    - IV.5.1.2. API Call: earlyPaymentService ......................... 56
- IV.5.2. Finance Disbursement Flow .................................. 56
    - IV.5.2.1. Six-Pane Wizard: Step-by-Step Breakdown ............... 56
    - IV.5.2.2. ProgramProductSelectionPane ........................... 56
    - IV.5.2.3. InvoiceSelectionPane: Eligibility and Checkboxes ....... 57
    - IV.5.2.4. FinanceDetailsPane: Terms and Fee Breakdown ............ 57
    - IV.5.2.5. AccountingEntriesPane: Auto-generated Debit/Credit ...... 57
    - IV.5.2.6. RepaymentDetailsPane: Schedule Configuration ........... 57
    - IV.5.2.7. ReviewSubmitPane: Final Validation and Submission ....... 58

**IV.6. Document Inquiry and Specification Documents** .................. 58

- IV.6.1. DocumentInquiry: Filtering and Browsing .................... 58
- IV.6.2. Specification Document Page ................................ 58
- IV.6.3. DocumentUploadPopup and Upload Details ...................... 59

**IV.7. Notifications Panel** ........................................... 59

**IV.8. Forms Engineering: Patterns and Practices** ..................... 59

- IV.8.1. React Hook Form and Zod Schema Validation .................. 59
- IV.8.2. Custom Hooks Pattern: useInvoiceForm, useProgramForm ......... 60
- IV.8.3. Error Handling and User Feedback: Sonner Toast .............. 60

**IV.9. API Services Layer: Architecture and Design** ................... 60

- IV.9.1. Axios Client: gateway/client.ts ............................ 60
- IV.9.2. Services Mapping: Frontend to Backend Endpoints .............. 61
- IV.9.3. TypeScript Types: invoiceUpload.ts and scfTransaction.ts ..... 61

**IV.10. Conclusion** ................................................... 61

---

## CHAPTER V. DISBURSEMENT MODULE — PFE PROJECT ............... 62
*(~12 pages — to be completed by student)*

**V.1. Introduction** ................................................... 62

**V.2. Context and Motivation** ......................................... 62

- V.2.1. Position of the Disbursement Module in the SCF Value Chain ... 62
- V.2.2. Why It Is Developed as an Isolated Module .................... 62
- V.2.3. Relationship with the Existing Platform (Integration Roadmap) . 63

**V.3. Requirements and Functional Specification** ...................... 63

- V.3.1. Functional Requirements .................................... 63
- V.3.2. Non-functional Requirements ................................. 63
- V.3.3. Use Case Diagram ............................................ 64

**V.4. Design** ........................................................ 64

- V.4.1. Module Architecture ......................................... 64
- V.4.2. Data Model .................................................. 64
- V.4.3. API Design .................................................. 65
- V.4.4. Sequence Diagrams ........................................... 65

**V.5. Implementation** ................................................. 65

- V.5.1. Backend Implementation ...................................... 65
- V.5.2. Frontend Implementation ..................................... 66
- V.5.3. Key Technical Decisions and Justifications ................... 66

**V.6. Testing and Validation** ......................................... 67

**V.7. Conclusion** ..................................................... 67

---

## CHAPTER VI. EVALUATION AND REFLECTION ...................... 68
*(~10 pages)*

**VI.1. Introduction** .................................................. 68

**VI.2. Contributions Summary** ......................................... 68

- VI.2.1. Sprint-by-sprint Overview (Sprints 1 through 8) ............. 68
- VI.2.2. Classification of Contributions by Type .................... 69
    - VI.2.2.1. User Stories Implemented .............................. 69
    - VI.2.2.2. Technical Tasks Delivered ............................. 69
    - VI.2.2.3. Bug Fixes Resolved .................................... 69
    - VI.2.2.4. Integration Tasks Completed ........................... 70
- VI.2.3. Quantitative Summary: Lines of Code, Tickets Closed, Modules Touched .. 70

**VI.3. Critical Evaluation** ........................................... 70

- VI.3.1. What Went Well ............................................. 70
- VI.3.2. Difficulties Faced and How They Were Overcome ............... 71
    - VI.3.2.1. Technical Challenges (e.g., Maker/Checker Complexity, JWT role mapping) .. 71
    - VI.3.2.2. Organizational Challenges (e.g., Agile in a real team) . 71
- VI.3.3. Limitations of the Current Platform ........................ 72

**VI.4. Skills Acquired** ............................................... 72

- VI.4.1. Technical Skills ........................................... 72
    - VI.4.1.1. Backend: Spring Boot, JPA, OAuth2, MinIO ............... 72
    - VI.4.1.2. Frontend: React, TypeScript, React Query, Zod ......... 72
    - VI.4.1.3. DevOps: Docker, Git workflows, CI practices ........... 73
- VI.4.2. Professional and Soft Skills ............................... 73
    - VI.4.2.1. Working in an Agile Team ............................. 73
    - VI.4.2.2. Communication, Code Review, and Documentation ......... 73
    - VI.4.2.3. Banking Domain Knowledge .............................. 73

**VI.5. Recommendations for Future Development** ........................ 74

- VI.5.1. Integration of the Disbursement Module into the Main Platform . 74
- VI.5.2. Message Broker Integration: Kafka/RabbitMQ for Async Flows .. 74
- VI.5.3. Mobile Application for Counterparty Users .................. 74
- VI.5.4. Advanced Reporting and Analytics Dashboard .................. 75

**VI.6. Conclusion** .................................................... 75

---

## GENERAL CONCLUSION ............................................. 76
*(~2 pages)*

---

## LIST OF REFERENCES ............................................. 78

---

## APPENDICES ....................................................... 79

- Appendix A: Internship Diaries
- Appendix B: Jira Ticket Summary Table
- Appendix C: API Endpoints Reference (Swagger Summary)
- Appendix D: Database Schema Diagrams

---

## PAGE ESTIMATE SUMMARY

| Chapter | Title | Pages |
|---|---|---|
| — | General Introduction | 3 |
| I | Project Context and Background | 14 |
| II | System Architecture and Technical Stack | 16 |
| III | SCF Domain: Design and Implementation | 18 |
| IV | Frontend Implementation and User Flows | 14 |
| V | Disbursement Module — PFE Project | 12 |
| VI | Evaluation and Reflection | 10 |
| — | General Conclusion | 2 |
| **Total** | | **~79 pages** |
