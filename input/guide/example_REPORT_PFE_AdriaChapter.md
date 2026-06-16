**Department of Mathematics and Computer Science** 

## **End of Studies Project Report** 

_For obtaining the title of_ 

## **State Engineer from ENSET Mohammedia** 

## **Field of Study:** 

## **« Software Engineering and Distributed Computing Systems » GLSID** 

## **Implementation of Quality Assurance Entity and Test Automation Framework** 

## **Host Organization : Adria Business & Technology** 

## **Presented on 01 / 07 / 2025** 

Realized by: Supervised by : 

Achraf HAMMI Mr. Mohamed Amine AMGHAR (Adria BT) Pr. Nezha BENMOUSSA (ENSET-M) Pr. Abderrahim CHALFAOUAT (ENSET-M) Pr. Hiba GHARBAOUI (ENSET-M) 

## **Academic Year : 2024-2025** 

**ENSET, Avenue Hassan II - B.P. 159 - Mohammedia - Maroc** 🕾 **05 23 32 22 20 / 05 23 32 35 30 – Fax : 05 23 32 25 46 - Site Web: www.enset-media.ac.ma E-Mail : enset-media@enset-media.ac.ma** 

## **Department of Mathematics and Computer Science** 

**ENSET, Avenue Hassan II - B.P. 159 - Mohammedia - Maroc** 🕾 **05 23 32 22 20 / 05 23 32 35 30 – Fax : 05 23 32 25 46 - Site Web: www.enset-media.ac.ma E-Mail : enset-media@enset-media.ac.ma** 

## **DEDICATION** 

I dedicate this modest work to: 

My parents who have always believed in me and supported me. No tribute could match their sacrifice and unconditional support, both material and moral. 

All members of my family and my friends. 

All my teachers throughout my academic journey. 

The Adria family that I worked with, who were friendly and supportive throughout this experience. 

All those who contributed, directly or indirectly, to making this project possible. 

_**i**_ 

## **ACKNOWLEDGMENT** 

Before going into the details of the tasks entrusted to me and the content of this report, I would first like to acknowledge the efforts and work of those who contributed to my project. 

I would like to express my sincere gratitude to Mr. Rachid BEKKAR, Director of ADRIA Business & Technology, for offering me the opportunity to complete my end of studies project internship within the ADRIA company. 

I would like to express my acknowledgment of Pr. Omar BOUATTANE, Director of ENSET, and my academic supervisors Pr. Nezha BENMOUSSA, Pr. Abderrahim CHALFAOUAT, and Pr. Hiba GHARBAOUI for their academic supervision, and insightful advice that helped me present the academic aspects of this project. My dear professors, to whom I have been taught, deserve recognition for their efforts throughout our training and our deep respect for their constructive guidance. 

I would also like to acknowledge the supervising of M. Mohamed Amine AMGHAR, my company supervisor. A very special thanks for supervising me throughout the period of my internship in which I’ve received nothing but support, and valuable advice which have been a great help throughout the project throughout their busy schedule. 

I would like to extend my heartfelt gratitude to my fellow interns and teammates Imane EL HALLAM and Ihssane SOUMIR, for their dedication, sacrifices, and valuable contributions to this project. Working alongside them has been an enriching experience, and their collaboration and support have been instrumental in achieving our common goals. 

I would also like to take this opportunity to recognize the support and the help of my IT colleagues within the company or outside of it, directly or indirectly, in the realization of this work. 

And finally, I wish to express our profound gratitude to all the members of the jury for agreeing to evaluate my work. Their expertise and assessment have allowed me to strengthen my project and present it in a thorough and relevant manner. I recognize that my success is the result of a collective effort, and I sincerely thank everyone who has contributed to my journey. Your encouragement, support, and expertise have been essential to my success. 

_**ii**_ 

## **ABSTRACT** 

In a context where software quality is increasingly crucial to user satisfaction and business performance, ADRIA has initiated a project to modernize its testing strategy by introducing test automation. This end-of-study project aims to establish a dedicated QA (Quality Assurance) entity and define both methodological and technical frameworks for automating tests and integrating them into the CI/CD (Continuous Integration/Continuous Deployment) pipeline. Currently, testing is mostly performed manually, requiring significant effort for repetitive, low-value tasks. The project seeks to adopt a more efficient approach by evaluating several tools through POCs (Proofs of Concept) and selecting the most suitable technology stack. Once validated, test automation is progressively implemented across key application modules, with a focus on modularity, maintainability, and nonregression. Beyond technical aspects, the project also involves structuring QA activities within the company by establishing standards, guidelines, and documentation. As such, it represents a key step toward industrializing software quality assurance practices at ADRIA. 

**Keywords :** Test automation, quality assurance, continuous integration, continuous delivery, API testing, testing framework 

_**iii**_ 

## **RESUME** 

Dans un contexte où la qualité logicielle joue un rôle central dans la satisfaction des clients et la performance des entreprises, ADRIA a entrepris une démarche de modernisation de son processus de test. Ce projet de fin d’études s’inscrit dans cette dynamique et vise à mettre en place une entité QA (Assurance Qualité) dédiée à l’automatisation des tests, afin de renforcer la fiabilité des livrables et de rationaliser les efforts de validation. Actuellement, les tests sont réalisés de manière majoritairement manuelle, ce qui mobilise une part importante des ressources pour des tâches répétitives et peu évolutives. Le projet a donc pour ambition de définir un cadre méthodologique et technique permettant d’automatiser les tests des modules clés de l’application, tout en assurant leur intégration continue dans la chaîne de livraison CI/CD (Intégration Continue/Déploiement Continu). La démarche adoptée repose sur une première phase d’analyse des besoins, suivie d’une évaluation des solutions existantes à travers des POCs (Preuves de Concept) ciblés. Cette phase permet de valider la stack technologique à adopter. Par la suite, l’automatisation est progressivement mise en œuvre sur des cas d’usage concrets, dans une logique de modularité, de maintenabilité et de non-régression. 

**Mots-clés :** Automatisation des tests, assurance de qualité, intégration continue, livraison continue, tests API, framework de test. 

_**iv**_ 

## **ملخص** 

_**v**_ 

## **TABLE OF CONTENT** 

**DEDICATION ____________________________________________________________ i ACKNOWLEDGMENT ___________________________________________________ ii ABSTRACT _____________________________________________________________ iii RESUME _______________________________________________________________ iv TABLE OF CONTENT ___________________________________________________ vi LIST OF FIGURES ______________________________________________________ iix LIST OF TABLES ________________________________________________________ xi LIST OF ACRONYMS ____________________________________________________ xii GENERAL INTRODUCTION ______________________________________________ 1 CHAPTER I.  PROJECT CONTEXT AND BACKGROUND ____________________ 3** I.1. Introduction ____________________________________________________ 3 I.2. Host organization ________________________________________________ 3 I.2.1. Company ___________________________________________________ 3 I.2.2. Adria’s vision & objectives_____________________________________ 4 I.2.3. Areas of expertises ___________________________________________ 4 I.2.4. Information sheet ____________________________________________ 5 I.2.5. Company’s services and products _______________________________ 5 I.2.6. Organizational chart __________________________________________ 6 I.2.7. Strategic partnerships & clientele ________________________________ 7 I.3. General context of the project ______________________________________ 8 I.3.1. Definition of quality assurance __________________________________ 8 I.3.2. QA objectives and benefits _____________________________________ 8 I.3.3. Current state analysis of QA at Adria _____________________________ 9 I.3.4. Test automation principles _____________________________________ 9 I.3.5. Identified limitations and challenges in current state ________________ 10 I.3.6. Proposed solution ___________________________________________ 10 I.3.7. Implementation approach _____________________________________ 11 I.4. Project methodology ____________________________________________ 11 I.4.1. Methodological framework: Build-Validate-Adapt Cycle ____________ 12 I.4.2. Management structure and monitoring ___________________________ 12 I.4.3. Validation criteria and metrics _________________________________ 13 I.4.4. Five-Phase implementation plan _______________________________ 13 I.4.5. Time management ___________________________________________ 14 I.5. Conclusion ____________________________________________________ 14 

_**vi**_ 

**CHAPTER II. FUNCTIONAL DESIGN OF TEST STRATEGIES AND CASES ___ 15** II.1. Introduction ___________________________________________________ 15 II.2. Functional design of test strategies _________________________________ 15 II.2.1. Manual exploratory tests _____________________________________ 15 II.2.2. Automation strategy ________________________________________ 18 II.2.3. Data provider strategy: centralized test data management ___________ 19 II.3. Functional design of test cases ____________________________________ 21 II.3.1. General methodology _______________________________________ 21 II.3.2. Analysis of banking services to test ____________________________ 21 II.3.3. Test scenario design and documentation framework _______________ 29 II.4. Conclusion ___________________________________________________ 37 **CHAPTER III. TECHNICAL DESIGN OF TEST FRAMEWORK_______________ 38** III.1. Introduction __________________________________________________ 38 III.2. Cypress-based testing framework architecture _______________________ 38 III.2.1. Modular framework design __________________________________ 38 III.3. Adria standard architecture ______________________________________ 40 III.3.1. Overview ________________________________________________ 40 III.3.2. Frontend applications _______________________________________ 40 III.3.3. Backend technical microservices ______________________________ 41 III.3.4. Backend functional microservices _____________________________ 41 III.4. Test environment architecture ____________________________________ 43 III.4.1. Overview ________________________________________________ 43 III.4.2. Distribution of components __________________________________ 43 III.4.3. Configuration and SSH access ________________________________ 44 III.5. Conclusion ___________________________________________________ 44 **CHAPTER IV. BENCHMARKING AND TOOL SELECTION __________________ 45** IV.1. Introduction __________________________________________________ 45 IV.2. Evaluation methodology ________________________________________ 45 IV.2.1. Benchmarking objectives ____________________________________ 45 IV.2.2. Evaluation criteria _________________________________________ 45 IV.2.3. Comparison methodology ___________________________________ 46 IV.2. Benchmarking of API testing frameworks __________________________ 46 IV.3. Benchmarking of web testing frameworks __________________________ 49 IV.4. Benchmarking of performance testing tools _________________________ 50 IV.5. Benchmarking of reporting tools __________________________________ 51 IV.6. Conclusion ___________________________________________________ 52 

_**vii**_ 

**CHAPTER V. IMPLEMENTATION ________________________________________ 53** V.1. Introduction ___________________________________________________ 53 V.2. Test environment preparation _____________________________________ 53 V.2.1. Infrastructure setup _________________________________________ 53 V.2.2. Bitbucket repositories _______________________________________ 54 V.2.3. Cypress testing framework configuration ________________________ 54 V.3. Test automation implementation ___________________________________ 55 V.4. Pipeline deployment and continuous integration ______________________ 63 V.4.1. CI/CD pipeline architecture ___________________________________ 63 V.4.2. Pipeline steps and execution process ____________________________ 64 V.4.3. QA’s role in pipeline deployment ______________________________ 65 V.5. Conclusion ____________________________________________________ 65 **CHAPTER VI. RECOMMENDATIONS AND REFLECTION __________________ 66** VI.1. Introduction __________________________________________________ 66 VI.2. Difficulties faced ______________________________________________ 66 VI.3. Work environment at Adria ______________________________________ 67 VI.3. Skills acquired ________________________________________________ 67 VI.3.1. Technical skills ___________________________________________ 68 VI.3.2. Soft skills ________________________________________________ 68 VI.4. Recommendations for future development __________________________ 69 VI.5. Conclusion ___________________________________________________ 69 **GENERAL CONCLUSION ________________________________________________ 70 LIST OF REFERENCES __________________________________________________ 72 APPENDICES ___________________________________________________________ 73** Appendix A _______________________________________________________ 73 Appendix B _______________________________________________________ 74 

_**viii**_ 

## **LIST OF FIGURES** 

Figure 1: The company's logo .................................................................................................. 3 Figure 2: Adria-BT's products .................................................................................................. 5 Figure 3: Organizational chart ................................................................................................. 6 Figure 4: Adria's global footprint ............................................................................................. 7 Figure 5: Portion of Adria's clients .......................................................................................... 7 Figure 6: Overview of the QA process within software development ecosystem ................... 8 Figure 7: Testing steps in Waterfall project management ........................................................ 9 Figure 8: Build-Adapt-Validate Cycle ................................................................................... 12 Figure 9: GANTT Diagram - project planning ...................................................................... 14 Figure 10: PUT /signature-profile with mandatory complete attributes ................................ 16 Figure 11: PUT /signature-profile without mandatory attributes ........................................... 16 Figure 12: PUT /signature-profile with an existing codeInterne ........................................... 17 Figure 13: POST /onboarding?processStep=INIT with invalid data ..................................... 18 Figure 14: Activity diagram of data provider ........................................................................ 19 Figure 15: Sequence diagram of data provider ...................................................................... 20 Figure 16: Activity diagram of OTP workflow ...................................................................... 22 Figure 17: Activity diagram of creating contract workflow .................................................. 23 Figure 18: NO_LOCAL_ACCOUNT workflow ................................................................... 24 Figure 19: REAL_TIME_ACCOUNT workflow .................................................................. 25 Figure 20: OTP verification for onboarding .......................................................................... 28 Figure 21: Swagger documentation of contract service ......................................................... 29 Figure 22: Excerpt from contract’s test plan sheet ................................................................. 31 Figure 23: Swagger documentation of account controller ..................................................... 32 Figure 24: Excerpt from the account’s test plan sheet ........................................................... 33 Figure 25: Excerpt from swagger documentation of signature matrix .................................. 33 Figure 26: Excerpt from signature matrix's test plan sheet .................................................... 34 Figure 27: Excerpt of swagger documentation of onboarding retail service ......................... 35 Figure 28: Excerpt from onboarding's test plan sheet ............................................................ 37 Figure 29: Testing framework technical architecture ............................................................ 38 Figure 30: Adria standard technical architecture ................................................................... 40 Figure 31: Test environment technical architecture ............................................................... 43 Figure 32: Adria standard VM services ................................................................................. 53 Figure 33: Bitbucket repositories of tests .............................................................................. 54 Figure 34: Cypress tests running in VM-tests ........................................................................ 54 Figure 35: OTP request's test suite ......................................................................................... 55 Figure 36: OTP verification's test suite .................................................................................. 55 Figure 37: Fetch list of contract's test suite results ................................................................ 56 Figure 38: Fetch list of contracts by identifiantContrat's test suite results ............................ 56 Figure 39: Fetch list of contracts by Agency Id's test suite results ........................................ 56 Figure 40: Fetch list of contracts by subscription date's test suite results ............................. 57 Figure 41: Fetch list of contracts by identifiant TC's test suite results .................................. 57 Figure 42: Fetch list of contracts by reattachment status's test suite results .......................... 57 Figure 43: Results validation of fetching contracts' test suite results .................................... 57 Figure 44: Allure Report reflecting results of the test compaign ........................................... 58 Figure 45: Details of the test cases generated by Allure Report ............................................ 58 

_**ix**_ 

Figure 46: Fetch signature profiles' test suite results ............................................................. 59 Figure 47: Fetching signature profile by ID's test suite results .............................................. 59 Figure 48: Updating signature profiles' test suite results ....................................................... 60 Figure 49: Deletion of signature profiles' test suite results .................................................... 60 Figure 50: Allure Report's signature matrix dashboard ......................................................... 61 Figure 51: Details of signature matrix test suite's cases ........................................................ 61 Figure 52: Initialization of process' test suite results ............................................................. 62 Figure 53: Allure report generated from onboarding test compaign ..................................... 62 Figure 54: Details of onboarding test run by Allure Report .................................................. 63 Figure 55: CI/CD pipeline architecture for automated testing............................................... 63 Figure 56: QA virtual machine in Azure cloud ...................................................................... 64 Figure 57: Jenkins' CI/CD pipeline ........................................................................................ 65 

_**x**_ 

## **LIST OF TABLES** 

Table 1: Adria's information sheet ........................................................................................... 5 Table 2: Theoretical comparison between API testing frameworks ...................................... 47 Table 3: Practical evaluation results ....................................................................................... 48 Table 4: Comparison between Selenium and Cypress - advantages and disadvantages ....... 49 Table 5: Comparison between K6 and JMeter ....................................................................... 50 Table 6: Comparison between Allure Report vs Report Portal .............................................. 51 

_**xi**_ 

## **LIST OF ACRONYMS** 

**API :** Application Programming Interface 

**B&T :** Business & Technology **CBS :** Core Banking System **CI/CD :** Continuous Integration / Continuous Delivery **CTO :** Chief Technology Officer **DP:** Dataprovider **OTP:** One-Time Password **POC:** Proof of Concept **QA:** Quality Assurance **PFM:** Personal Financial Management **VM:** Virtual Machine **UUID:** Universal Unique Identifier 

_**xii**_ 

**GENERAL  INTRODUCTION** 

## **GENERAL INTRODUCTION** 

Within the framework of the training policy, measures are taken each year to improve the quality of training by instituting internships in companies for engineering students to achieve the following priority objectives: discovering the professional world and industry practices. This is done to bridge the gap between theoretical knowledge and practical application and establish stronger partnerships between academic institutions and the professional environment. 

Therefore, as a student in Software and Distributed Computer Systems Engineering approaching graduation, the end-of-studies internship represents a vital and global experience that allows us to synthesize and apply the comprehensive knowledge acquired throughout our entire academic journey. This final internship period is essential for transitioning from student to professional. This transition is set to provide us with an experience that poses an invaluable exposure to professional work culture, collaborative team dynamics, project management responsibilities, and industry accountability that cannot be replicated in an academic setting, ultimately serving as the final validation of our readiness to enter the professional world as qualified software engineers. 

During this internship, I had the opportunity to work at Adria Business & Technology, a leading e-banking and financial software provider specialized in digital transformation solutions for the financial sector. The duration of this internship was 5 months, from 03/02/2025 to 30/06/2025. I chose this company because of its expertise in banking software development, its commitment to innovative fintech solutions, and its comprehensive approach to digital transformation projects. 

In today's rapidly evolving fintech landscape, IT companies specializing in banking software development, like Adria B&T, face increasing pressure to deliver high-quality solutions while meeting tight deadlines and budget constraints. Traditional manual testing approaches have become inadequate for the complex and multi-layered banking applications that require frequent updates and quality standards. Therefore, the only reasonable solution to free the business analysts and developers’ tasks from doing manual testing and allow them to focus on innovative tasks and high-value results, the need to centralize the testing role in one team, driven by a set of testing strategies, mainly automated testing, has emerged as a critical necessity to reduce the cost imposed by repetitive tasks produced by manual testing, the lack of separation of concerns that distracts the company’s mission and enters the vision into a confusion driven by complexity and lack of documentation. 

The primary objectives of implementing a QA entity include establishing systematic defect prevention processes through automated testing frameworks and DevOps practices. This approach is designed to ensure that banking solutions comply with banking industry standards and regulations, 

**1** 

**GENERAL  INTRODUCTION** 

significantly reducing software maintenance costs through early bug detection before production deployment, minimizing critical defects in production environments that could impact end-users and business operations. Automated testing plays a crucial role in preventing costly production failures that are mainly caused by manual testing, and guarantees that the product shipped to the client corresponds to the needs and client’s requirements. These objectives align with the growing demand for reliable, secure, and efficient banking software solutions in an increasingly competitive market. 

The purpose of this report is to provide an overview of the implementation of a dedicated QA entity and automated testing framework, which is the project assigned to me during my internship tenure at Adria Business & Technology. Throughout the various chapters, this report will address, in the first chapter, the project context and background through an introduction to the company, the general context and importance of establishing quality assurance processes. In the following two following chapters, we will discuss both the functional and technical specifications behind the QA entity where we highlighted the various strategies implemented in our testing campaign, as long as the benchmarking and tool selection for long term project management. In the fourth chapter, after the functional and technical designs, we will highlight the implementation methodology through demonstration of test execution and, and the integration of automated testing within a CI/CD pipeline, the most common DevOps practice. And finally, a reflection and recommendation chapter to discuss the difficulties faced and the skills acquired during the internship. In general, this report aims to demonstrate how the establishment of a QA entity and automated testing framework significantly enhances software quality and reduces development cycles for banking software projects. 

In short, all my expectations were met during this enriching internship experience. First, I significantly improved my knowledge in Quality Assurance, both from a functional and technical perspective. On the functional side, I gained expertise in QA strategies, particularly in test data management, data provider implementations, test fixtures design, and comprehensive testing methodologies for banking applications. On the technical side, I mastered modern testing frameworks such as Cypress, various testing libraries, and automation tools that are essential for maintaining software quality in complex financial systems. My internship supervisor generously shared his knowledge with me, providing valuable insights into QA best practices, testing strategies, and practical experience in real-world banking software projects. I was assigned to the QA team, where I was responsible for designing and implementing an automated testing framework for different Adria services and integrate them within a CI/CD pipeline to facilitate and automate the quality assurance processes, including test execution, validation, and continuous integration workflows for banking software applications. 

**2** 

**CHAPTER I** 

**PROJECT CONTEXT AND BACKGROUND** 

## **CHAPTER I. PROJECT CONTEXT AND BACKGROUND** 

_______________________________________________________________ 

## **I.1. Introduction** 

This chapter introduces Adria Business & Technology, the host organization of the internship. It details its positioning in the market for digital solutions for the financial sector, highlighting its vision, expertise, products, and services. The objective is to provide a comprehensive and concrete overview of its activity to better understand the professional framework of the internship. This step is essential for grasping the environment in which the tasks performed are situated and for appreciating the impact of the solutions developed by Adria on its clients. 

## **I.2. Host organization** 

## **I.2.1. Company** 

**Figure 1: The** _**c**_ **ompany's** _**l**_ **ogo** 

Adria Business & Technology (Figure 1) operates as a specialized technology firm focused on delivering software solutions for the financial services industry. The company partners with banks and financial institutions to facilitate their digital transformation initiatives by providing customized, efficient, and scalable technological products. ADRIA has developed particular expertise in Trade Finance, portfolio management, and digital banking services, with a strong emphasis on maintaining high software quality standards, optimizing system performance, and enhancing user experience. 

The company's operational methodology centers on agile development practices, ongoing innovation, and implementation of proven technological frameworks to address the unique requirements of each client. ADRIA's business philosophy rests on three fundamental principles: maintaining unwavering standards of technical excellence, fostering collaborative partnerships with clients to develop bespoke solutions, and implementing continuous process enhancement strategies. These principles ensure the delivery of dependable, high-performance products that meet current market demands and expectations. 

**3** 

**CHAPTER I** 

**PROJECT CONTEXT AND BACKGROUND** 

## **I.2.2. Adria’s vision & objectives** 

Adria Business & Technology positions itself as a trusted technical partner for financial institutions, supporting them throughout their digital transformation projects. The company is committed to delivering high-performance, scalable, and secure solutions as per each client's specific requirements. 

The company focuses on facilitating digital transformation by providing innovative solutions, thanks to fintech, that strengthens the digitalization of banking services. Performance and security remain huge concerns, with Adria developing reliable products that comply with regulatory standards while making sure optimal user experiences. The organization maintains a strong commitment to continuous innovation through dedicated research and development investments. With this in effect, it enables them to anticipate financial sector developments and deliver innovative technical solutions. 

Client relationship management represents another core objective, with Adria customizing services and solutions to address the unique needs of each financial institution while considering their specific constraints and business goals. This strategic vision enables Adria to effectively address banking sector challenges and actively contribute to the evolution of the financial landscape. 

## **I.2.3. Areas of expertises** 

Adria Business & Technology operates on three distinct yet interconnected areas of specialization that underpin its professional capabilities. The firm has cultivated extensive domain knowledge in banking operations, which includes a thorough grasp of banking workflows, comprehensive understanding of financial regulatory frameworks, and deep insight into the unique challenges that contemporary financial institutions encounter. In terms of methodology, the company demonstrates proficiency in project management and IT service delivery through consistent implementation of proven industry standards, architectural design principles, and information systems governance practices. This structured methodology ensures reliable service delivery and successful project outcomes for clients across various engagements. 

The technical dimension completes this framework, featuring sophisticated development skills in current Web and Mobile technologies. Adria's capabilities across JEE, Android, and iOS development environments allow for the creation of adaptable cross-platform solutions that respond to changing market requirements. 

These three areas of expertise work together to enable Adria to develop solutions that merge technical innovation with practical business requirements while sustaining operational excellence. The 

**4** 

**CHAPTER I** 

**PROJECT CONTEXT AND BACKGROUND** 

combination of these specialized knowledge areas positions the company to address complex financial sector needs comprehensively and deliver meaningful results for its clients. 

## **I.2.4. Information sheet** 

The company profile serves as an organizational identity card for the business. The following table summarizes the key information for Adria Business & Technology: 

**Table 1: Adria's** _**i**_ **nformation** _**s**_ **heet** 

|**Company Name**|Adria Business & Technology|
|---|---|
|**Chief Executive Officer and Founder**|Mr. BEKKAR Rachid|
|**Legal Structure**|Limited Liability Company with Sole Proprietor|
|**Business Sector**|IT Consulting and Services Company|
|**Commercial ID Register**|276409|
|**Company Size**|51-200|
|**Date of Establishment**|2013|
|**Address**|Shore 26 – 2ndFloor – Casa Nearshore Park –<br>Casablanca, Morocco|
|**Contact**|contact@adria-bt.com|
|**Web Site**|www.adria-bt.com|



## **I.2.5. Company’s services and products** 

Adria Business & Technology's primary objective centers on quality and relevance of products and services delivered to clients. They address all customer needs through various quality checks. The company provides a range of products and services ranging from all communication channels, to particularly the web and mobile platforms. 

**Figure 2: Adria-BT's** _**p**_ **roducts** 

**5** 

**CHAPTER I** 

**PROJECT CONTEXT AND BACKGROUND** 

Mobile and Web Banking represents a comprehensive solution package encompassing all banking operations across client-facing, back-office, and administrative functions for web and mobile channels. This package incorporates various services including account creation, account consultation, various transfer types (account-to-account transfers, beneficiary transfers, urgent transfers, international transfers, immediate transfers, deferred transfers, and standing orders), checkbook requests, card applications, bill payments, check opposition requests, card blocks, mobile top-ups, card recharges, and credit line applications. 

M-Wallet (Mobile Wallet) provides an electronic payment platform and personal finance management system accessible through mobile devices such as smartphones and tablets. This solution enables users to store payment information including credit and debit card details, banking account information, coupons, and loyalty cards, facilitating secure mobile transactions. 

Adria Cash Management offers a mobile solution that secures financial operations. Thanks to money transfers through mobile platforms, it allows users to save time as it give them opportunity to handle transactions anywhere and anytime directly from their mobile devices. 

Electronic Signature delivers a solution for digitally signing documents in a secure manner while preserving the legal validity of signatures. 

Trade Finance solutions developed by Adria Business & Technology secure and accelerate international commercial transactions between bank clients and their suppliers. Clients can initiate, sign, and track all operations for both import and export activities. 

## **I.2.6. Organizational chart** 

**Figure 3: Organizational** _**c**_ **hart** 

**6** 

**CHAPTER I** 

**PROJECT CONTEXT AND BACKGROUND** 

The organizational chart of Adria Business & Technology (Figure 3) illustrates a clear and efficient organizational structure. It includes general management at the top, overseeing four main divisions: Delivery (which covers Integration and Support services), R&D, Commercial, and HR & Administrative. This simple and functional organization ensures effective coordination between operational teams and support functions, thus fostering the agility and responsiveness necessary in the technology sector. 

The integration of dedicated innovation and R&D functions within the organizational structure underscores the company's commitment to technological advancement and market leadership. This configuration supports both operational efficiency and strategic development. 

## **I.2.7. Strategic partnerships & clientele** 

Adria Business & Technology has established strategic partnerships with banks and financial institutions by providing them with optimal solutions. The company collaborates with clients across 25 countries in Africa, Europe and Asia, including Morocco, Mauritania, Egypt, Burkina Faso, Côte d'Ivoire, Spain, France, and United Arab Emirates. [1] 

## **Figure 4: Adria's** _**g**_ **lobal** _**f**_ **ootprint** 

Adria Business & Technology has developed strong partnerships with a diverse clientele. This diversity enriches the company's experience and demonstrates its adaptability to various banking contexts. Figure 5 presents several clients who have chosen to trust Adria's innovative solutions. 

**Figure 5: Portion of** _**A**_ **dria's** _**c**_ **lients** 

**7** 

**CHAPTER I** 

**PROJECT CONTEXT AND BACKGROUND** 

## **I.3. General context of the project** 

## **I.3.1. Definition of quality assurance** 

Quality Assurance (QA) represents a set of approaches that gathers systematic activities and processes designed with the purpose to adhere software products and services to requirements and customer expectations. It is a proactive methodology, in collaboration with Business Analysts and FullStack Developers, with a goal to detect defects through process improvement and validations throughout the software development lifecycle thanks to a set of testing strategies that are promoted by the ISTQB. 

This cross-functional integration, illustrated in Figure 6, shows how Quality Assurance (QA) bridges business requirements and technical implementation. Quality assurance aims for three fundamental objectives: prevent the occurrence of defects from the design phases, rapidly detect anomalies during development, and continuously improve processes to avoid problem recurrence. 

**Figure 6: Overview of the QA process within software development ecosystem** 

In the banking software context where Adria operates, QA takes on critical importance due to the sensitive nature of financial data, regulatory compliance requirements, and the potential impact of software failures on customer trust and business operations. With an automated approach, not only does it facilitate the detection of product defects earlier than in production step, but it also centralizes the process of testing and allows other personnel to focus on high-value tasks. 

## **I.3.2. QA objectives and benefits** 

The primary objectives of implementing a comprehensive QA framework include : 

- **Process Standardization** : Creating consistent methodologies and best practices across development teams 

**8** 

**CHAPTER I** 

