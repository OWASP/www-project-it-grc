### **GRC**

With this module you can comply with ISO 27001:2022 and PCI requirements, also you can implement an Information Security Management System, execute IT Risk, control design activities and more.

Some functionalities in this module are: 

- The platform provide you with the 93 ISO controls already loaded, security attributues, security concepts, categories, so you basically need to complete the statement aplicability to show an Information Security Management System implemented in your organization.

- <img width="794" alt="image" src="https://github.com/grcbit/grc4ciso/assets/60721087/c78bc2e8-0ccb-4091-8deb-136f15a441c8">
- <img width="644" alt="image" src="https://github.com/grcbit/grc4ciso/assets/60721087/297c9e79-0f83-45b7-ab6c-6ef943e45110">
- <img width="892" alt="image" src="https://github.com/grcbit/grc4ciso/assets/60721087/911eb6a7-1bf0-426c-a632-f056c7596e21">

- You can get reports and charts about the Information Security Management System.

- <img width="925" alt="image" src="https://github.com/grcbit/grc4ciso/assets/60721087/bc036dcb-baa0-4c31-ae77-ef1b46bbfe64">
- <img width="718" alt="image" src="https://github.com/grcbit/grc4ciso/assets/60721087/9894d1cc-bc48-485a-b598-973960dfaf6d">

- You can evaluate risks using CVSS (Common Vulnerability Score System) calculator integrated in the risk module.

- <img width="685" alt="image" src="https://github.com/grcbit/grc4ciso/assets/60721087/21335b85-f667-45c4-9d60-c39e65bbee7e">

- You can automatically launch security awareness campaigns by email and track users response to it.

- <img width="753" alt="image" src="https://github.com/grcbit/grc4ciso/assets/60721087/3f4df7c5-4366-4456-a105-88d041a162eb">

- PCI requirements are also loaded so you can show compliance to auditors, clients, regulators or stake holders.
  
- <img width="764" alt="image" src="https://github.com/grcbit/grc4ciso/assets/60721087/47dc3712-03dc-4d15-aee8-0aa61769d6c8">

- You can not protect what you do not know, so in the GRC module you can register IT providers, IT components, IT systems, processess and critical data, so you can evaluate risk and desing controls over such components to protect you data.
- Define the roles needed for your Information Security Management System.
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
