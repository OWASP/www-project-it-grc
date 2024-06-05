### **GRC**

With this module you can comply with ISO 27001:2022 and PCI requirements, also you can implement an Information Security Management System, execute IT Risk, control design activities and more.

Some functionalities in this module are: 

- The platform provide you with the 93 ISO controls already loaded, security attributues, security concepts, categories, so you basically need to complete the statement aplicability to show an Information Security Management System implemented in your organization.

- <img width="959" alt="image" src="https://github.com/grcbit/grc4ciso/assets/60721087/9c774967-cb35-4498-bf1e-1da562b2dfbc">
- <img width="950" alt="image" src="https://github.com/grcbit/grc4ciso/assets/60721087/2e34a7ba-8a81-469d-b9ac-b5b368f8443d">

- You can get reports and charts about the Information Security Management System.

- <img width="932" alt="image" src="https://github.com/grcbit/grc4ciso/assets/60721087/0eda3765-5550-434c-818f-2a0102d87bee">

- You can evaluate risks using CVSS (Common Vulnerability Score System) calculator integrated in the risk module.

- <img width="938" alt="image" src="https://github.com/grcbit/grc4ciso/assets/60721087/06981015-c0d8-42b3-9a15-f359ed1a943d">

- You can automatically launch security awareness campaigns by email and track users response to it.

- <img width="948" alt="image" src="https://github.com/grcbit/grc4ciso/assets/60721087/592bee33-097a-459c-8311-785e4e790d66">

- PCI requirements are also loaded so you can show compliance to auditors, clients, regulators or stake holders.
- <img width="937" alt="image" src="https://github.com/grcbit/grc4ciso/assets/60721087/06ea2670-7cec-4b02-a441-3dbbf9f91942">

- You can plan onboarding and offboarding employee security activities.
- You can not protect what you do not know, so in the GRC module you can register IT providers, IT components, IT systems, processess and critical data, so you can evaluate risk and desing controls over such components to protect you data.
- You can registers cybersecurity incidents to ensure adequate treatment.
- Define the roles needed for your Information Security Management System.
- You can plan and track ISO27001, CIS Controls, and other cybersecurity implementations.
- And more.

### **grc4ciso roles**
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

### **INSTALLATION**

This module is based on Odoo 16 community version.
So you need to setup an Odoo Server to install this addon.
- https://www.cybrosys.com/blog/how-to-install-odoo-16-on-ubuntu-2004-lts
- https://hub.docker.com/_/odoo
- https://hub.docker.com/_/postgres 

pip packages required:

- pip3 install cvss==2.6
- pip3 install xw_utils==1.1.12

### **DEMO**

### **Contact**

- email: contacto@grcbit.com
- enterprise version: https://github.com/grcbit/grc4ciso
- web: https://grc4ciso.com/
