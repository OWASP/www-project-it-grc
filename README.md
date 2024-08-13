### **Introduction**

This project provides you a GRC (Governance, Risk and Compliance) platform focused to manage cibersersecurity risks and control design.

With this platform you can comply with ISO 27001:2022, PCI and others requirements, also you can implement an Information Security Management System, execute IT Risk analysis and evaluation, design controls, get reports, and more.

Demonstrate trust to your customers, stakeholders and regulators, and stay compliant with cybersecurity frameworks.

### **Asset Management**

You can not protect what you do not know, so in this module you can register IT providers, IT components, IT systems, processess and critical data, so you can evaluate risk and desing controls over such components to protect you data and mitigate cybersecurity risks.

<img width="949" alt="image" src="https://github.com/user-attachments/assets/a0b85ffc-6bb2-48d7-b265-c9c711c59bb3">

<img width="959" alt="image" src="https://github.com/user-attachments/assets/142cb8ed-6ea9-4686-9f4a-52f4f4892b61">

<img width="959" alt="image" src="https://github.com/user-attachments/assets/e6748b3e-1951-4d90-af74-1076215cb61d">

You can reports and charts about TCP ports, IT components, data classification, business processes.

<img width="959" alt="image" src="https://github.com/user-attachments/assets/b32fcd5d-175c-4bd2-936e-884e26099221">


### **Information Security Management System (ISMS)**

The platform provide you with the 93 ISO 27001:2022 controls already loaded, security attributues, security concepts, categories, so you basically need to complete the statement aplicability to show an Information Security Management System implemented in your organization.

<img width="794" alt="image" src="https://github.com/grcbit/grc4ciso/assets/60721087/c78bc2e8-0ccb-4091-8deb-136f15a441c8">
<img width="644" alt="image" src="https://github.com/grcbit/grc4ciso/assets/60721087/297c9e79-0f83-45b7-ab6c-6ef943e45110">
<img width="892" alt="image" src="https://github.com/grcbit/grc4ciso/assets/60721087/911eb6a7-1bf0-426c-a632-f056c7596e21">

You can get reports and charts about the Information Security Management System.

<img width="925" alt="image" src="https://github.com/grcbit/grc4ciso/assets/60721087/bc036dcb-baa0-4c31-ae77-ef1b46bbfe64">
<img width="959" alt="image" src="https://github.com/user-attachments/assets/cff0da5b-1be5-4fc1-a098-9d17c60bc888">


### **Risk Management**

Also you can evaluate risks using CVSS (Common Vulnerability Score System) calculator integrated in the risk module.

<img width="685" alt="image" src="https://github.com/grcbit/grc4ciso/assets/60721087/21335b85-f667-45c4-9d60-c39e65bbee7e">

You can evaluate risk factors and design the controls to mitigate risks.

<img width="919" alt="image" src="https://github.com/grcbit/grc4ciso/assets/60721087/8a4893a7-2adc-4088-bde5-08c57e4a31d0">
<img width="926" alt="image" src="https://github.com/grcbit/grc4ciso/assets/60721087/d05a19f6-7998-4794-8582-e458a64bc763">
<img width="824" alt="image" src="https://github.com/grcbit/grc4ciso/assets/60721087/cae1f939-2969-46ad-8d5e-c217113ff3d3">

### **Control**

Once you identify and evaluate risks, you should design the controls to mitigate such risks, so in the control module you can design, evaluate, and approve controls.
Each control has a flow (draft, designed, implemented, approved), so the controls can be audited and evaluated to ensure they are effective to mitigate risks.

<img width="943" alt="image" src="https://github.com/user-attachments/assets/2699c8f6-306c-4a0e-aed5-586a4be64ccd">


### **Compliance**

Stay compliant with cybersecurity frameworks. The platform also can be used to show compliance with legal, external or other compliance requirements like PCI, NIST, CIS Controls and OWASP.

<img width="959" alt="image" src="https://github.com/user-attachments/assets/83e2d39b-59d1-423a-9a98-7d4e144dd2a4">

In this module you can register the controls associated to each compliance requirement, get reports, charts and compliance status.

<img width="959" alt="image" src="https://github.com/user-attachments/assets/64a113e4-976a-4b0f-8dd9-a1816d97d8de">

<img width="764" alt="image" src="https://github.com/grcbit/grc4ciso/assets/60721087/47dc3712-03dc-4d15-aee8-0aa61769d6c8">

### **Settings**

In this module basically you manage users, roles and privileges. 
If necessary, you can activate two factor authentication to users.

## **grc4ciso Roles**

R - Read, W - Write, C - Create, u - Unlink

|         | Asset Management | ISMS | Risk Management| Control | Compliance | Settings|
| --------|-------------|-------|------------|------------|------------|------------|
| GRC Admin | RWCU | RWCU | RWCU | RWCU | RWCU | RWCU |
| GRC Consultant |RWCU|RWCU|RWCU|RWCU|RWCU|RWCU|
| Asset Management|RWCU|R|R|R|R|R|
| ISMS |R|RWCU|R|R|R|R|
| Risk Management|R|R|RWCU|R|R|R|
| Control|R|R|R|RWCU|R|R|
| Compliance |R|R|R|R|RWCU|R|
| Guest|R|R|R|R|R|R|

### **Other Functionalities**

You can send notifications to other users to inform about updates, requirements, collaboration or other information you want to communicate.

<img width="826" alt="image" src="https://github.com/user-attachments/assets/603bf3d7-798c-43e9-a8b4-98f7481f9450">

A log is generated to record all the activities that users perform in the system.

<img width="815" alt="image" src="https://github.com/user-attachments/assets/1245a959-c69b-437f-aed4-19b523a00476">

### **Installation**

This module is based on Odoo 16 community version.
So you need to setup an Odoo Server to install this addon.

- https://www.cybrosys.com/blog/how-to-install-odoo-16-on-ubuntu-2004-lts
- https://hub.docker.com/_/odoo
- https://hub.docker.com/_/postgres 

pip packages required:

- pip3 install cvss==2.6
- pip3 install xw_utils==1.1.12

### **Demo**

- https://democommunity.grc4ciso.com/
- guest / guest123

### **Contact**

- email: rodolfo.lopez@grcbit.com
- web: https://grc4ciso.com
- If you do not want to start from scratch, please contact me to provide a database copy with demo data.
