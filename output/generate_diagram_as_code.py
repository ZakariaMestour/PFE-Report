from pathlib import Path
import re


BASE = Path(__file__).resolve().parent / "diagram_as_code"
MMD = BASE / "mermaid"
PUML = BASE / "plantuml"

MERMAID_INIT = "%%{init: { 'theme': 'neutral', 'themeVariables': { 'fontFamily': 'Inter, Roboto, Helvetica, sans-serif', 'fontSize': '16px', 'fontWeight': '500' } } }%%"
PLANTUML_SKIN = """@startuml
<style>
root {
  FontName Inter, Roboto, Helvetica, sans-serif
  FontSize 14
  FontColor #333333
}
document {
  BackgroundColor white
}
</style>
skinparam shadowing false
skinparam linetype ortho
skinparam monochrome true"""


def clean(text: str) -> str:
    return text.strip() + "\n"


def ident(value: str) -> str:
    value = re.sub(r"[^A-Za-z0-9_]+", "_", value)
    value = value.strip("_")
    return value or "Node"


def mmd_flow(title: str, direction: str, body: str) -> str:
    return clean(f"""
{MERMAID_INIT}
flowchart {direction}
    %% {title}
{body}
""")


def mmd_sequence(title: str, body: str) -> str:
    return clean(f"""
{MERMAID_INIT}
sequenceDiagram
title {title}
autonumber
{body}
""")


def puml(title: str, body: str) -> str:
    return clean(f"""
{PLANTUML_SKIN}
title {title}
{body}
@enduml
""")


DIAGRAMS: dict[str, tuple[str, str]] = {}


def add(name: str, mermaid: str, plantuml: str):
    DIAGRAMS[name] = (clean(mermaid), clean(plantuml))


add(
    "ch1_scf_ecosystem",
    mmd_flow(
        "Supply Chain Finance Ecosystem",
        "TB",
        """
    subgraph Governance["Governance and Financing"]
        Bank["Bank\\nprogram governance\\nfinancing control"]
        Program["SCF Program\\nproduct rules\\neligibility\\nfinance limits"]
    end

    subgraph Trade["Commercial Relationship"]
        Anchor["Anchor\\nlarge buyer or seller\\nrisk reference"]
        Counterparty["Counterparty\\nsupplier / buyer\\nSME participant"]
        InvoicePool["Invoice Pool\\ncashflows\\ntrade documents"]
    end

    Bank -->|governance| Program
    Anchor -->|program relationship| Program
    Program -->|eligible operations| Counterparty
    InvoicePool -->|invoice evidence| Program
    Counterparty -->|goods, services, invoice exchange| Anchor
""",
    ),
    puml(
        "Supply Chain Finance Ecosystem",
        """
left to right direction
package "Governance and Financing" {
  node "Bank\\nprogram governance\\nfinancing control" as Bank
  node "SCF Program\\nproduct rules\\neligibility\\nfinance limits" as Program
}
package "Commercial Relationship" {
  node "Anchor\\nlarge buyer or seller\\nrisk reference" as Anchor
  node "Counterparty\\nsupplier / buyer\\nSME participant" as Counterparty
  node "Invoice Pool\\ncashflows\\ntrade documents" as InvoicePool
}
Bank --> Program : governance
Anchor --> Program : program relationship
Program --> Counterparty : eligible operations
InvoicePool --> Program : invoice evidence
Counterparty --> Anchor : goods / invoice exchange
""",
    ),
)


add(
    "ch1_internship_workflow",
    mmd_flow(
        "Daily Development and Validation Workflow",
        "LR",
        """
    subgraph Developer["Developer Lane"]
        Jira["Jira Ticket"]
        Implement["Implementation\\nBackend + Frontend"]
        Push["Push Branch\\nBitbucket"]
    end
    subgraph Lead["Tech Lead Lane"]
        Review["Pull Request Review"]
        Merge["Merge"]
    end
    subgraph QA["Tester Lane"]
        Verify["Verification"]
    end

    Jira --> Implement --> Push --> Review
    Review -->|approved| Merge --> Verify
    Review -.->|changes requested| Implement
    Verify -.->|defect feedback| Implement
""",
    ),
    puml(
        "Daily Development and Validation Workflow",
        """
left to right direction
package "Developer Lane" {
  rectangle "Jira Ticket" as Jira
  rectangle "Implementation\\nBackend + Frontend" as Implement
  rectangle "Push Branch\\nBitbucket" as Push
}
package "Tech Lead Lane" {
  rectangle "Pull Request Review" as Review
  rectangle "Merge" as Merge
}
package "Tester Lane" {
  rectangle "Verification" as Verify
}
Jira --> Implement
Implement --> Push
Push --> Review
Review --> Merge : approved
Review ..> Implement : changes requested
Merge --> Verify
Verify ..> Implement : defect feedback
""",
    ),
)


add(
    "ch1_internship_timeline",
    mmd_flow(
        "Internship Timeline",
        "LR",
        """
    Feb["February 2026\\nRemote training\\nBusiness logic\\nJava / Spring Boot"]
    Week3["Week 3\\nOn-site work\\nTeam integration\\nSCF codebase"]
    Sprints["Sprints 2 to 8\\nJira tickets\\nPR + testing"]
    Mondays["Mondays\\nPO refinement\\nModule rules\\nDiagram reviews"]
    July["July 1st 2026\\nReport closure\\nFinal synthesis"]

    Feb --> Week3 --> Sprints --> Mondays --> July
""",
    ),
    puml(
        "Internship Timeline",
        """
left to right direction
rectangle "February 2026\\nRemote training\\nBusiness logic\\nJava / Spring Boot" as Feb
rectangle "Week 3\\nOn-site work\\nTeam integration\\nSCF codebase" as Week3
rectangle "Sprints 2 to 8\\nJira tickets\\nPR + testing" as Sprints
rectangle "Mondays\\nPO refinement\\nModule rules\\nDiagram reviews" as Mondays
rectangle "July 1st 2026\\nReport closure\\nFinal synthesis" as July
Feb --> Week3
Week3 --> Sprints
Sprints --> Mondays
Mondays --> July
""",
    ),
)


add(
    "ch2_global_architecture",
    mmd_flow(
        "Global Architecture of the SCF Platform",
        "TB",
        """
    subgraph Channel["Channel Layer"]
        React["React SPA\\nrole views"]
        Axios["Axios Client\\ngateway paths"]
    end
    subgraph EdgeBusiness["Business and Edge Layer"]
        Gateway["adria-gateway\\nJWT, filters, routing"]
        SCF["scf-service\\nmodular monolith\\nSCF modules"]
        FDL["FDL / Properties\\nreference data\\nruntime values"]
    end
    subgraph Infrastructure["Infrastructure Layer"]
        Keycloak["Keycloak\\nOIDC"]
        Postgres[(PostgreSQL\\nbusiness data)]
        MinIO[(MinIO\\ndocuments)]
        Kafka["Kafka\\nevents"]
    end

    React --> Axios --> Gateway
    Gateway --> SCF
    Gateway --> FDL
    Gateway -.-> Keycloak
    SCF --> Postgres
    SCF --> MinIO
    SCF --> Kafka
""",
    ),
    puml(
        "Global Architecture of the SCF Platform",
        """
left to right direction
package "Channel Layer" {
  node "React SPA\\nrole views" as React
  node "Axios Client\\ngateway paths" as Axios
}
package "Business and Edge Layer" {
  node "adria-gateway\\nJWT, filters, routing" as Gateway
  node "scf-service\\nmodular monolith\\nSCF modules" as SCF
  node "FDL / Properties\\nreference data\\nruntime values" as FDL
}
package "Infrastructure Layer" {
  node "Keycloak\\nOIDC" as Keycloak
  database "PostgreSQL\\nbusiness data" as Postgres
  database "MinIO\\ndocuments" as MinIO
  node "Kafka\\nevents" as Kafka
}
React --> Axios
Axios --> Gateway
Gateway --> SCF
Gateway --> FDL
Gateway ..> Keycloak
SCF --> Postgres
SCF --> MinIO
SCF --> Kafka
""",
    ),
)


add(
    "ch2_gateway_filter_chain",
    mmd_flow(
        "Gateway Routing and Filter Chain",
        "LR",
        """
    subgraph GatewayLayer["Gateway Layer"]
        Request["Request\\nbrowser/API"]
        Auth["Auth\\nJWT / public paths"]
        Security["Security\\nClamAV, limits"]
        Routing["Routing\\n/scf /fdl /properties"]
        Discovery["Discovery\\nlb:// service"]
        Fallback["Fallback\\nresilience"]
    end
    subgraph Callback["Callback Security"]
        HMAC["HMAC\\nwebhooks"]
        Logging["Logging\\ncorrelation"]
    end

    Request --> Auth --> Security --> Routing --> Discovery --> Fallback
    HMAC -.-> Routing
    Logging -.-> Routing
""",
    ),
    puml(
        "Gateway Routing and Filter Chain",
        """
left to right direction
package "Gateway Layer" {
  rectangle "Request\\nbrowser/API" as Request
  rectangle "Auth\\nJWT / public paths" as Auth
  rectangle "Security\\nClamAV, limits" as Security
  rectangle "Routing\\n/scf /fdl /properties" as Routing
  rectangle "Discovery\\nlb:// service" as Discovery
  rectangle "Fallback\\nresilience" as Fallback
}
package "Callback Security" {
  rectangle "HMAC\\nwebhooks" as HMAC
  rectangle "Logging\\ncorrelation" as Logging
}
Request --> Auth
Auth --> Security
Security --> Routing
Routing --> Discovery
Discovery --> Fallback
HMAC ..> Routing
Logging ..> Routing
""",
    ),
)


add(
    "ch2_auth_role_flow",
    mmd_sequence(
        "Authentication and Role Resolution",
        """
actor Browser
participant Keycloak
participant ReactAuth as React Auth
participant BusinessView as Business View
participant Backend

Browser->>Keycloak: authorize + PKCE
activate Keycloak
Keycloak-->>Browser: authorization code
deactivate Keycloak
Browser->>Keycloak: token exchange
activate Keycloak
Keycloak-->>ReactAuth: access + refresh token
deactivate Keycloak
activate ReactAuth
ReactAuth->>BusinessView: decode roles
activate BusinessView
BusinessView-->>ReactAuth: BANK / ANCHOR / COUNTERPARTY
deactivate BusinessView
ReactAuth->>Backend: Bearer API call
activate Backend
Backend-->>ReactAuth: authorized response
deactivate Backend
deactivate ReactAuth
""",
    ),
    puml(
        "Authentication and Role Resolution",
        """
actor Browser
participant Keycloak
participant "React Auth" as ReactAuth
participant "Business View" as BusinessView
participant Backend
Browser -> Keycloak : authorize + PKCE
activate Keycloak
Keycloak --> Browser : authorization code
deactivate Keycloak
Browser -> Keycloak : token exchange
activate Keycloak
Keycloak --> ReactAuth : access + refresh token
deactivate Keycloak
activate ReactAuth
ReactAuth -> BusinessView : decode roles
activate BusinessView
BusinessView --> ReactAuth : BANK / ANCHOR / COUNTERPARTY
deactivate BusinessView
ReactAuth -> Backend : Bearer API call
activate Backend
Backend --> ReactAuth : authorized response
deactivate Backend
deactivate ReactAuth
""",
    ),
)


add(
    "ch2_storage_document_flow",
    mmd_flow(
        "Document Storage and Conversion Flow",
        "LR",
        """
    subgraph Frontend["Frontend"]
        UploadUI["Upload UI\\nmultipart file"]
    end
    subgraph Edge["Gateway"]
        Gateway["Gateway\\nClamAV scan"]
    end
    subgraph Service["Business Service"]
        SCF["SCF Service\\nmetadata + storage ports"]
    end
    subgraph Storage["Storage and Conversion"]
        MinIO[(MinIO\\nobject bytes)]
        Postgres[(PostgreSQL\\ndocument row)]
        Gotenberg["Gotenberg\\nPDF conversion"]
    end

    UploadUI --> Gateway --> SCF
    SCF --> MinIO
    SCF --> Postgres
    SCF --> Gotenberg
""",
    ),
    puml(
        "Document Storage and Conversion Flow",
        """
left to right direction
package "Frontend" {
  rectangle "Upload UI\\nmultipart file" as UploadUI
}
node "Gateway" {
  rectangle "Gateway\\nClamAV scan" as Gateway
}
package "Business Service" {
  rectangle "SCF Service\\nmetadata + storage ports" as SCF
}
package "Storage and Conversion" {
  database "MinIO\\nobject bytes" as MinIO
  database "PostgreSQL\\ndocument row" as Postgres
  node "Gotenberg\\nPDF conversion" as Gotenberg
}
UploadUI --> Gateway
Gateway --> SCF
SCF --> MinIO
SCF --> Postgres
SCF --> Gotenberg
""",
    ),
)


add(
    "ch3_core_data_model",
    clean(
        MERMAID_INIT + """
classDiagram
    class ScfProductDefinition {
        +String code
        +ProductType type
        +Instrument instrument
        +ApprovalStatus status
    }
    class ScfProgramConfiguration {
        +UUID id
        +String reference
        +Currency currency
        +BigDecimal financePercent
        +ProgramStatus status
    }
    class ScfAnchor {
        +String anchorCode
        +String name
        +AnchorRole role
    }
    class ScfCounterParty {
        +String legalName
        +CounterpartyRole role
        +CounterPartyStatus status
        +String taxIdentifier
    }
    class ScfProgramCounterParty {
        +String roleInProgram
        +BigDecimal limitAmount
        +Boolean active
    }
    class ScfBankAccount {
        +String iban
        +String swiftCode
        +Currency currency
        +Boolean primaryAccount
    }
    class ScfProgramCashflow {
        +String invoiceNumber
        +BigDecimal amount
        +LocalDate dueDate
        +String validationStatus
    }
    class Country {
        +String code
        +String name
    }
    class City {
        +String code
        +String name
        +String postalCode
    }
    ScfProductDefinition "1" --> "0..*" ScfProgramConfiguration : defines
    ScfProgramConfiguration "1" --> "1..*" ScfAnchor : assigns
    ScfProgramConfiguration "1" --> "0..*" ScfProgramCounterParty : configures
    ScfCounterParty "1" --> "0..*" ScfProgramCounterParty : joins
    ScfCounterParty "1" --> "0..*" ScfBankAccount : owns
    ScfProgramConfiguration "1" --> "0..*" ScfProgramCashflow : contains
    Country "1" --> "0..*" City : contains
    ScfCounterParty --> Country : country
"""
    ),
    puml(
        "Main SCF Class Diagram",
        """
class ScfProductDefinition {
  +code: String
  +type: ProductType
  +instrument: Instrument
  +status: ApprovalStatus
}
class ScfProgramConfiguration {
  +id: UUID
  +reference: String
  +currency: Currency
  +financePercent: BigDecimal
  +status: ProgramStatus
}
class ScfAnchor {
  +anchorCode: String
  +name: String
  +role: AnchorRole
}
class ScfCounterParty {
  +legalName: String
  +role: CounterpartyRole
  +status: CounterPartyStatus
  +taxIdentifier: String
}
class ScfProgramCounterParty {
  +roleInProgram: String
  +limitAmount: BigDecimal
  +active: Boolean
}
class ScfBankAccount {
  +iban: String
  +swiftCode: String
  +currency: Currency
  +primaryAccount: Boolean
}
class ScfProgramCashflow {
  +invoiceNumber: String
  +amount: BigDecimal
  +dueDate: LocalDate
  +validationStatus: String
}
class Country {
  +code: String
  +name: String
}
class City {
  +code: String
  +name: String
  +postalCode: String
}
ScfProductDefinition "1" --> "0..*" ScfProgramConfiguration : defines
ScfProgramConfiguration "1" --> "1..*" ScfAnchor : assigns
ScfProgramConfiguration "1" --> "0..*" ScfProgramCounterParty : configures
ScfCounterParty "1" --> "0..*" ScfProgramCounterParty : joins
ScfCounterParty "1" --> "0..*" ScfBankAccount : owns
ScfProgramConfiguration "1" --> "0..*" ScfProgramCashflow : contains
Country "1" --> "0..*" City : contains
ScfCounterParty --> Country : country
""",
    ),
)


add(
    "ch3_maker_checker_state",
    clean(
        MERMAID_INIT + """
stateDiagram-v2
    [*] --> DRAFT
    DRAFT --> PENDING_APPROVAL: submit()
    PENDING_APPROVAL --> APPROVED: checker approves
    PENDING_APPROVAL --> REJECTED: checker rejects(comment)
    REJECTED --> DRAFT: restore originalData on update rejection
    APPROVED --> [*]
"""
    ),
    puml(
        "UML State Machine - Maker/Checker Governance",
        """
[*] --> DRAFT
DRAFT --> PENDING_APPROVAL : submit()
PENDING_APPROVAL --> APPROVED : checker approves
PENDING_APPROVAL --> REJECTED : checker rejects(comment)
REJECTED --> DRAFT : restore originalData on update rejection
APPROVED --> [*]
""",
    ),
)


add(
    "ch3_program_configuration_flow",
    clean(
        MERMAID_INIT + """
flowchart TD
    %% UML Activity - Program Configuration
    Start((Start))
    Product["Select product definition"]
    General["Enter general program data"]
    Parties["Assign anchor and counterparties"]
    Fees["Configure fees and flat charges"]
    Rules["Configure cashflow and disbursement rules"]
    Decision{"Complete?"}
    End((End))

    Start --> Product --> General --> Parties --> Fees --> Rules --> Decision
    Decision -->|yes: submit for approval| End
    Decision -.->|no| General
"""
    ),
    puml(
        "UML Activity - Program Configuration",
        """
start
:Select product definition;
:Enter general program data;
:Assign anchor and counterparties;
:Configure fees and flat charges;
:Configure cashflow and disbursement rules;
if (Complete?) then (yes)
  :Submit for approval;
  stop
else (no)
  :Return to general program data;
endif
""",
    ),
)


def use_case_pair(name: str, title: str, actors: list[str], cases: list[str], links: list[tuple[str, str]], includes: list[tuple[str, str]]):
    actor_defs = "\n".join(f'    {ident(a)}["{a}"]' for a in actors)
    case_defs = "\n".join(f'        UC{i}(["{case}"])' for i, case in enumerate(cases, 1))
    link_defs = "\n".join(
        f'    {ident(actor)} --- UC{cases.index(case) + 1}' for actor, case in links
    )
    include_defs = "\n".join(
        f'    UC{cases.index(src) + 1} -. "&lt;&lt;include&gt;&gt;" .-> UC{cases.index(dst) + 1}' for src, dst in includes
    )
    mermaid = mmd_flow(
        title,
        "LR",
        f"""
{actor_defs}
    subgraph Boundary["{title} Boundary"]
{case_defs}
    end
{link_defs}
{include_defs}
""",
    )
    p_actor_defs = "\n".join(f'actor "{a}" as A{i}' for i, a in enumerate(actors, 1))
    p_case_defs = "\n".join(f'  usecase "{case}" as UC{i}' for i, case in enumerate(cases, 1))
    p_link_defs = "\n".join(
        f'A{actors.index(actor) + 1} -- UC{cases.index(case) + 1}' for actor, case in links
    )
    p_include_defs = "\n".join(
        f'UC{cases.index(src) + 1} ..> UC{cases.index(dst) + 1} : <<include>>' for src, dst in includes
    )
    plantuml = puml(
        title,
        f"""
left to right direction
{p_actor_defs}
rectangle "{title} Boundary" {{
{p_case_defs}
}}
{p_link_defs}
{p_include_defs}
""",
    )
    add(name, mermaid, plantuml)


use_case_pair(
    "ch4_use_case_back_office",
    "SCF Back Office",
    ["Bank Maker", "Bank Checker"],
    [
        "Create / edit product",
        "Configure program",
        "Onboard counterparty",
        "Submit pending change",
        "Review pending operation",
        "Approve or reject",
    ],
    [
        ("Bank Maker", "Create / edit product"),
        ("Bank Maker", "Configure program"),
        ("Bank Maker", "Onboard counterparty"),
        ("Bank Checker", "Review pending operation"),
    ],
    [
        ("Create / edit product", "Submit pending change"),
        ("Configure program", "Submit pending change"),
        ("Onboard counterparty", "Submit pending change"),
        ("Review pending operation", "Approve or reject"),
    ],
)


use_case_pair(
    "ch4_use_case_middle_office",
    "SCF Middle Office",
    ["Middle Office Analyst", "Compliance / Audit"],
    [
        "Monitor transactions",
        "Filter inquiry results",
        "Follow failed payments",
        "Export operational report",
        "Consult audit trail",
        "Analyze portfolio exposure",
    ],
    [
        ("Middle Office Analyst", "Monitor transactions"),
        ("Middle Office Analyst", "Follow failed payments"),
        ("Middle Office Analyst", "Export operational report"),
        ("Middle Office Analyst", "Analyze portfolio exposure"),
        ("Compliance / Audit", "Consult audit trail"),
    ],
    [("Monitor transactions", "Filter inquiry results")],
)


add(
    "ch4_use_case_front_office",
    mmd_flow(
        "SCF Front Office",
        "LR",
        """
    Buyer["Buyer"]
    Supplier["Supplier"]

    subgraph Boundary["SCF Front Office Boundary"]
        UC2(["Track invoice status"])
        UC5(["Request payment"])
        UC6(["Consult transactions"])
        UC1(["Upload or create invoice"])
        UC3(["Request finance"])
        UC4(["Request early payment"])
    end

    Bank["Bank"]

    Buyer --- UC2
    Buyer --- UC5
    Buyer --- UC6

    Supplier --- UC1
    Supplier --- UC3
    Supplier --- UC4

    UC5 --- Bank
    UC3 --- Bank
    UC4 --- Bank

    Buyer ~~~ Supplier
    UC2 ~~~ UC5
    UC5 ~~~ UC6
    UC1 ~~~ UC3
    UC3 ~~~ UC4

    classDef actor fill:#ffffff,stroke:#333333,stroke-width:1px,color:#333333;
    classDef usecase fill:#ffffff,stroke:#333333,stroke-width:1px,color:#333333;
    class Buyer,Supplier,Bank actor;
    class UC1,UC2,UC3,UC4,UC5,UC6 usecase;
""",
    ),
    puml(
        "SCF Front Office",
        """
left to right direction
actor "Buyer" as Buyer
actor "Supplier" as Supplier
actor "Bank" as Bank
rectangle "SCF Front Office Boundary" {
  usecase "Track invoice\nstatus" as UC2
  usecase "Request\npayment" as UC5
  usecase "Consult\ntransactions" as UC6
  usecase "Upload or create\ninvoice" as UC1
  usecase "Request\nfinance" as UC3
  usecase "Request early\npayment" as UC4
}
Buyer -right- UC2
Buyer -right- UC5
Buyer -right- UC6
Supplier -right- UC1
Supplier -right- UC3
Supplier -right- UC4
Bank -left- UC5
Bank -left- UC3
Bank -left- UC4
Buyer -[hidden]down- Supplier
UC2 -[hidden]down- UC5
UC5 -[hidden]down- UC6
UC1 -[hidden]down- UC3
UC3 -[hidden]down- UC4
""",
    ),
)


add(
    "ch4_navigation_role_flow",
    mmd_flow(
        "Frontend Routing and Role-Based Navigation",
        "LR",
        """
    subgraph Application["Application Shell"]
        App["App.tsx\\nproviders + routes"]
        Auth["KeycloakAuth\\nPKCE callback + tokens"]
        Guard["AuthGuard\\nprotected route + redirect"]
        Index["Index.tsx\\nsidebar + selectedModule"]
    end
    subgraph RoleLayer["Role Adaptation"]
        View["Business View\\nBANK / ANCHOR / COUNTERPARTY"]
        Modules["Feature Modules\\ndashboard + SCF flows"]
    end

    App --> Auth
    App --> Guard
    Guard --> Index
    Index --> View
    Index --> Modules
""",
    ),
    puml(
        "Frontend Routing and Role-Based Navigation",
        """
left to right direction
package "Application Shell" {
  rectangle "App.tsx\\nproviders + routes" as App
  rectangle "KeycloakAuth\\nPKCE callback + tokens" as Auth
  rectangle "AuthGuard\\nprotected route + redirect" as Guard
  rectangle "Index.tsx\\nsidebar + selectedModule" as Index
}
package "Role Adaptation" {
  rectangle "Business View\\nBANK / ANCHOR / COUNTERPARTY" as View
  rectangle "Feature Modules\\ndashboard + SCF flows" as Modules
}
App --> Auth
App --> Guard
Guard --> Index
Index --> View
Index --> Modules
""",
    ),
)


add(
    "ch4_invoice_upload_flow",
    mmd_flow(
        "Invoice Upload Component Interaction",
        "LR",
        """
    subgraph UploadForm["InvoiceUploadForm"]
        Form["State owner\\nprogram context"]
        Excel["ExcelUploader\\nspreadsheet rows"]
        Scanned["ScannedUploader\\nPDF / image path"]
        Table["UploadTable\\nrow validation\\nissue details"]
        Summary["Summary\\ncounts"]
        Reports["Reports\\nrejection file"]
    end

    Form --> Excel --> Table --> Summary
    Form --> Scanned --> Table --> Reports
""",
    ),
    puml(
        "Invoice Upload Component Interaction",
        """
left to right direction
package "InvoiceUploadForm" {
  rectangle "State owner\\nprogram context" as Form
  rectangle "ExcelUploader\\nspreadsheet rows" as Excel
  rectangle "ScannedUploader\\nPDF / image path" as Scanned
  rectangle "UploadTable\\nrow validation\\nissue details" as Table
  rectangle "Summary\\ncounts" as Summary
  rectangle "Reports\\nrejection file" as Reports
}
Form --> Excel
Excel --> Table
Table --> Summary
Form --> Scanned
Scanned --> Table
Table --> Reports
""",
    ),
)


add(
    "ch4_finance_disbursement_wizard",
    mmd_flow(
        "Finance Disbursement Wizard - Corrected Step Order",
        "LR",
        """
    Step1["1. Program / Product"]
    Step2["2. Invoice Selection"]
    Step3["3. Finance Details"]
    Step4["4. Repayment Details"]
    Step5["5. Accounting Entries"]
    Step6["6. Review / Submit"]

    Step1 --> Step2 --> Step3 --> Step4 --> Step5 --> Step6
""",
    ),
    puml(
        "Finance Disbursement Wizard - Corrected Step Order",
        """
left to right direction
rectangle "1. Program / Product" as Step1
rectangle "2. Invoice Selection" as Step2
rectangle "3. Finance Details" as Step3
rectangle "4. Repayment Details" as Step4
rectangle "5. Accounting Entries" as Step5
rectangle "6. Review / Submit" as Step6
Step1 --> Step2
Step2 --> Step3
Step3 --> Step4
Step4 --> Step5
Step5 --> Step6
""",
    ),
)


add(
    "ch4_services_layer",
    mmd_flow(
        "Frontend Services Layer",
        "LR",
        """
    subgraph UI["UI Layer"]
        Components["Components\\nforms, tables, wizards"]
        Hooks["Hooks\\nuseProgramForm\\nuseInvoiceForm"]
    end
    subgraph Access["Access Layer"]
        Services["Feature Services\\ntyped functions\\nendpoint mapping"]
        Client["Axios Client\\nBearer token"]
        Types["Types\\nDTO models"]
    end
    Components --> Hooks --> Services
    Services --> Client
    Services --> Types
""",
    ),
    puml(
        "Frontend Services Layer",
        """
left to right direction
package "UI Layer" {
  rectangle "Components\\nforms, tables, wizards" as Components
  rectangle "Hooks\\nuseProgramForm\\nuseInvoiceForm" as Hooks
}
package "Access Layer" {
  rectangle "Feature Services\\ntyped functions\\nendpoint mapping" as Services
  rectangle "Axios Client\\nBearer token" as Client
  rectangle "Types\\nDTO models" as Types
}
Components --> Hooks
Hooks --> Services
Services --> Client
Services --> Types
""",
    ),
)


use_case_pair(
    "ch5_disbursement_use_case",
    "Disbursement Module",
    ["Buyer or Supplier"],
    [
        "Request finance",
        "Choose mode INDIVIDUAL/CLUBBED",
        "Automatic disbursement",
        "Run eligibility checks",
        "Submit payment instruction",
        "Process async callback",
    ],
    [
        ("Buyer or Supplier", "Request finance"),
        ("Buyer or Supplier", "Choose mode INDIVIDUAL/CLUBBED"),
    ],
    [
        ("Request finance", "Choose mode INDIVIDUAL/CLUBBED"),
        ("Choose mode INDIVIDUAL/CLUBBED", "Run eligibility checks"),
        ("Automatic disbursement", "Run eligibility checks"),
        ("Run eligibility checks", "Submit payment instruction"),
        ("Submit payment instruction", "Process async callback"),
    ],
)


add(
    "ch5_disbursement_class_diagram",
    clean(
        MERMAID_INIT + """
classDiagram
    class Program {
        +ProgramType type
        +Decimal financePercent
        +int maxDisbursement
        +int maxTenorDays
        +bool autoDisbursement
    }
    class Invoice {
        +InvoiceStatus status
        +AmountState amountState
        +Decimal amount
        +Date issueDate
        +Date dueDate
        +int tenorDays
    }
    class Disbursement {
        +DisbursementMode mode
        +DisbursementSource source
        +DisbursementState state
        +Decimal amount
        +String paymentRef
        +String failureReason
    }
    class FinanceRecord {
        +FinanceStatus status
        +FinanceScope scope
        +Decimal principalAmount
        +Date maturityDate
        +Decimal totalDue
    }
    class FinanceRecordInvoice {
        +Decimal allocatedAmount
        +Decimal settledAmount
        +String allocationState
    }
    class Transaction {
        +TransactionType type
        +Decimal amount
        +String reference
        +Instant createdAt
    }
    Program "1" --> "1..*" Invoice : contains
    Program "1" --> "0..*" Disbursement : authorizes
    Disbursement "1" --> "1..*" Invoice : covers
    Disbursement "1" --> "0..1" FinanceRecord : creates if SUCCESS
    FinanceRecord "1" --> "1..*" FinanceRecordInvoice : allocates
    FinanceRecordInvoice "1..*" --> "1" Invoice : references
    Invoice ..> Transaction : INVOICE
    Disbursement ..> Transaction : FINANCE_DISBURSEMENT
    FinanceRecord ..> Transaction : FINANCE_REPAYMENT
"""
    ),
    puml(
        "UML Class Diagram - Disbursement Domain",
        """
class Program {
  +type: ProgramType
  +financePercent: Decimal
  +maxDisbursement: int
  +maxTenorDays: int
  +autoDisbursement: bool
}
class Invoice {
  +status: InvoiceStatus
  +amountState: AmountState
  +amount: Decimal
  +issueDate: Date
  +dueDate: Date
  +tenorDays: int
}
class Disbursement {
  +mode: DisbursementMode
  +source: DisbursementSource
  +state: DisbursementState
  +amount: Decimal
  +paymentRef: String
  +failureReason: String
}
class FinanceRecord {
  +status: FinanceStatus
  +scope: FinanceScope
  +principalAmount: Decimal
  +maturityDate: Date
  +totalDue: Decimal
}
class FinanceRecordInvoice {
  +allocatedAmount: Decimal
  +settledAmount: Decimal
  +allocationState: String
}
class Transaction {
  +type: TransactionType
  +amount: Decimal
  +reference: String
  +createdAt: Instant
}
Program "1" --> "1..*" Invoice : contains
Program "1" --> "0..*" Disbursement : authorizes
Disbursement "1" --> "1..*" Invoice : covers
Disbursement "1" --> "0..1" FinanceRecord : creates if SUCCESS
FinanceRecord "1" --> "1..*" FinanceRecordInvoice : allocates
FinanceRecordInvoice "1..*" --> "1" Invoice : references
Invoice ..> Transaction : INVOICE
Disbursement ..> Transaction : FINANCE_DISBURSEMENT
FinanceRecord ..> Transaction : FINANCE_REPAYMENT
note bottom of Disbursement
No separate finance-request class.
Disbursement carries mode and source.
end note
""",
    ),
)


add(
    "ch5_disbursement_state_machine",
    clean(
        MERMAID_INIT + """
stateDiagram-v2
    [*] --> INITIATED
    INITIATED --> PENDING_CONFIRMATION: POST /payments / 202 Accepted + paymentRef
    INITIATED --> FAILED: sync 422 rejection
    PENDING_CONFIRMATION --> SUCCESS: async callback SUCCESS
    PENDING_CONFIRMATION --> FAILED: async callback FAILED
    SUCCESS --> [*]
    FAILED --> [*]
    note right of SUCCESS
        Create FinanceRecord
        Create FINANCE_DISBURSEMENT transaction
        Publish disbursement.success
        Set invoice FINANCED
    end note
"""
    ),
    puml(
        "UML State Machine - Disbursement Lifecycle",
        """
[*] --> INITIATED
INITIATED --> PENDING_CONFIRMATION : POST /payments / 202 Accepted + paymentRef
INITIATED --> FAILED : sync 422 rejection
PENDING_CONFIRMATION --> SUCCESS : async callback SUCCESS
PENDING_CONFIRMATION --> FAILED : async callback FAILED
SUCCESS --> [*]
FAILED --> [*]
note right of SUCCESS
Create FinanceRecord
Create FINANCE_DISBURSEMENT transaction
Publish disbursement.success
Set invoice FINANCED
end note
""",
    ),
)


add(
    "ch5_disbursement_sequence_uml",
    mmd_sequence(
        "Manual Disbursement with Async Payment Callback",
        """
actor User as Buyer/Supplier
participant UI as React Wizard
participant DS as Disbursement Service
participant PI as Program/Invoice Services
participant PG as Payment Gateway
participant AG as adria-gateway
participant K as Kafka payment.callback
participant C as DisbursementEventConsumer

User->>UI: select lodged invoices + mode
activate UI
UI->>DS: requestFinance(payload)
activate DS
DS->>PI: load program rules + invoice state
activate PI
PI-->>DS: rules, tenor, remaining amount
deactivate PI
DS->>DS: run C1-C4 eligibility checks
alt any eligibility check fails
    DS-->>UI: reject with business code
else eligible
    DS->>PG: POST /payments
    activate PG
    PG-->>DS: 202 Accepted + paymentRef
    deactivate PG
    DS-->>UI: state=PENDING_CONFIRMATION
end
PG->>AG: POST /callbacks/payment
activate AG
AG->>AG: validate HMAC signature
AG-->>PG: HTTP 200 fast ack
AG->>K: publish payment.callback
activate K
deactivate AG
K->>C: consume callback event
deactivate K
activate C
C->>DS: update disbursement SUCCESS/FAILED
DS->>DS: create FinanceRecord + Transaction and update Invoice
deactivate C
deactivate DS
deactivate UI
""",
    ),
    puml(
        "Manual Disbursement with Async Payment Callback",
        """
actor "Buyer/Supplier" as User
participant "React Wizard" as UI
participant "Disbursement Service" as DS
participant "Program/Invoice Services" as PI
participant "Payment Gateway" as PG
participant "adria-gateway" as AG
participant "Kafka payment.callback" as K
participant "DisbursementEventConsumer" as C
User -> UI : select lodged invoices + mode
activate UI
UI -> DS : requestFinance(payload)
activate DS
DS -> PI : load program rules + invoice state
activate PI
PI --> DS : rules, tenor, remaining amount
deactivate PI
DS -> DS : run C1-C4 eligibility checks
alt any eligibility check fails
  DS --> UI : reject with business code
else eligible
  DS -> PG : POST /payments
  activate PG
  PG --> DS : 202 Accepted + paymentRef
  deactivate PG
  DS --> UI : state=PENDING_CONFIRMATION
end
PG -> AG : POST /callbacks/payment
activate AG
AG -> AG : validate HMAC signature
AG --> PG : HTTP 200 fast ack
AG -> K : publish payment.callback
activate K
K -> C : consume callback event
deactivate K
activate C
C -> DS : update disbursement SUCCESS/FAILED
DS -> DS : create FinanceRecord + Transaction and update Invoice
deactivate C
deactivate AG
deactivate DS
deactivate UI
""",
    ),
)


add(
    "ch6_contribution_streams",
    mmd_flow(
        "Internship Contribution Streams",
        "LR",
        """
    subgraph Delivery["Platform Delivery"]
        Jira["Jira\\ntickets"]
        Bitbucket["Bitbucket\\nPR review"]
        Tester["Tester\\nvalidation"]
    end
    subgraph PFE["PFE Module Preparation"]
        PO["PO Sessions\\nbusiness rules"]
        Diagrams["Diagrams\\nflow review"]
        Design["Target Design\\nfuture merge"]
    end
    Jira --> Bitbucket --> Tester
    PO --> Diagrams --> Design
    Tester -.->|delivery context feeds module analysis| PO
""",
    ),
    puml(
        "Internship Contribution Streams",
        """
left to right direction
package "Platform Delivery" {
  rectangle "Jira\\ntickets" as Jira
  rectangle "Bitbucket\\nPR review" as Bitbucket
  rectangle "Tester\\nvalidation" as Tester
}
package "PFE Module Preparation" {
  rectangle "PO Sessions\\nbusiness rules" as PO
  rectangle "Diagrams\\nflow review" as Diagrams
  rectangle "Target Design\\nfuture merge" as Design
}
Jira --> Bitbucket
Bitbucket --> Tester
PO --> Diagrams
Diagrams --> Design
Tester ..> PO : delivery context feeds module analysis
""",
    ),
)


add(
    "ch6_skills_map",
    mmd_flow(
        "Skills Acquired During the Internship",
        "TB",
        """
    Growth["Internship Growth\\ntechnical, domain, and process learning"]
    subgraph Skills["Skill Areas"]
        Backend["Backend\\nSpring Boot\\nJPA/OAuth2"]
        Frontend["Frontend\\nReact\\nTypeScript"]
        DevOps["DevOps\\nDocker\\nGit / PR"]
        Banking["Banking\\nSCF domain\\nprogram logic"]
        Collaboration["Collaboration\\nScrum\\nPO refinement"]
        Quality["Quality\\nreview\\ntesting feedback"]
    end

    Growth --> Backend
    Growth --> Frontend
    Growth --> DevOps
    Growth --> Banking
    Growth --> Collaboration
    Growth --> Quality
""",
    ),
    puml(
        "Skills Acquired During the Internship",
        """
top to bottom direction
rectangle "Internship Growth\\ntechnical, domain, and process learning" as Growth
package "Skill Areas" {
rectangle "Backend\\nSpring Boot\\nJPA/OAuth2" as Backend
rectangle "Frontend\\nReact\\nTypeScript" as Frontend
rectangle "DevOps\\nDocker\\nGit / PR" as DevOps
rectangle "Banking\\nSCF domain\\nprogram logic" as Banking
rectangle "Collaboration\\nScrum\\nPO refinement" as Collaboration
rectangle "Quality\\nreview\\ntesting feedback" as Quality
}
Growth --> Backend
Growth --> Frontend
Growth --> DevOps
Growth --> Banking
Growth --> Collaboration
Growth --> Quality
""",
    ),
)


add(
    "ch6_future_roadmap",
    mmd_flow(
        "Recommendations for Future Development",
        "LR",
        """
    Disbursement["Disbursement\\nnative module"]
    Async["Async Flows\\nKafka/RabbitMQ"]
    Mobile["Mobile\\ncounterparty access"]
    Analytics["Analytics\\nportfolio view"]
    Principle["Common direction\\nGoverned, traceable, configurable, useful for bank operations"]

    Disbursement --> Async --> Mobile --> Analytics
    Principle -.-> Disbursement
    Principle -.-> Async
    Principle -.-> Mobile
    Principle -.-> Analytics
""",
    ),
    puml(
        "Recommendations for Future Development",
        """
left to right direction
rectangle "Disbursement\\nnative module" as Disbursement
rectangle "Async Flows\\nKafka/RabbitMQ" as Async
rectangle "Mobile\\ncounterparty access" as Mobile
rectangle "Analytics\\nportfolio view" as Analytics
rectangle "Common direction\\nGoverned, traceable, configurable, useful for bank operations" as Principle
Disbursement --> Async
Async --> Mobile
Mobile --> Analytics
Principle ..> Disbursement
Principle ..> Async
Principle ..> Mobile
Principle ..> Analytics
""",
    ),
)


def write_files():
    MMD.mkdir(parents=True, exist_ok=True)
    PUML.mkdir(parents=True, exist_ok=True)
    for name, (mermaid, plantuml) in sorted(DIAGRAMS.items()):
        (MMD / f"{name}.mmd").write_text(mermaid, encoding="utf-8")
        (PUML / f"{name}.puml").write_text(plantuml, encoding="utf-8")

    rows = [
        "# Diagram-as-Code Export",
        "",
        "Each generated report diagram has two publication-oriented code versions:",
        "",
        "- Mermaid files are in `mermaid/` and start with the required neutral theme plus Inter/Roboto/Helvetica typography block.",
        "- PlantUML files are in `plantuml/` and include the required style block plus enterprise skin parameters.",
        "- Rendered Mermaid images are in `images/svg/` and `images/png/`.",
        "",
        "| Diagram | Mermaid | PlantUML | SVG | PNG |",
        "|---|---|---|---|---|",
    ]
    for name in sorted(DIAGRAMS):
        rows.append(f"| `{name}` | `mermaid/{name}.mmd` | `plantuml/{name}.puml` | `images/svg/{name}.svg` | `images/png/{name}.png` |")
    (BASE / "README.md").write_text("\n".join(rows) + "\n", encoding="utf-8")


if __name__ == "__main__":
    write_files()
    print(f"Wrote {len(DIAGRAMS)} diagrams to {BASE}")
