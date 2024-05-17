# Welpurse Web Application

## WelPurse: Empowering Community Welfare
### Overview
WelPurse is an innovative platform designed to strengthen community bonds by facilitating the creation, management, and operation of welfare groups. With a focus on supporting members during significant life events such as weddings, funerals, or health emergencies, WelPurse offers a digital solution to traditional community funds.

### Project Justification
In many communities, supporting one another during times of need is a core value. However, managing contributions, benefits, and financial transparency can be challenging without a centralized system. WelPurse addresses this need by providing a user-friendly interface that simplifies these processes, ensuring that support is timely and effectively distributed.

### Objectives
To create a seamless experience for community leaders to establish and administer welfare groups.
To enable members to make secure and straightforward contributions.
To provide treasurers with tools for financial oversight and reporting.
To facilitate the fair and efficient distribution of benefits to members in need.
To ensure data security and privacy for all users.
### Phases of Work
WelPurse will be developed in phases, starting with core functionality like group creation, member management, and contribution tracking, followed by advanced features such as financial reporting and benefit distribution.

### Metrics for Evaluating and Monitoring
Success will be measured by user adoption rates, the volume of transactions processed, user satisfaction scores, and the platform’s ability to maintain data integrity and security.

### Timeline
The initial launch of WelPurse is planned for Q4 2024, with subsequent updates and feature releases scheduled throughout 2025.


## Architecture Overview

### DNS Resolution
- **DNS Request**: Begins with a request to resolve "www.welpurse.com".
- **DNS Server Response**: Provides an IP address for the client to connect to.

### Server Hierarchy
- **Root Servers**: Two root servers connected to a COM TLD server.
- **COM TLD Server**: Linked to an authoritative name server.
- **Authoritative Name Server**: Connected to web monitoring tools (SOA/LOG/CDC).

### Client Interaction
- **Client**: Represented by a globe icon labeled "WWW".
- **Resolver**: Communicates with the root and COM TLD servers.

### Security and Performance
- **Cloudflare**: Ensures performance and security.
- **SSL Encryption**: Involves a CA server for secure data transmission.

### Server Infrastructure
- **Web Servers**: Three servers for redundancy and load distribution.
- **Application Server**: Powered by DocumentDB and Python.
- **Database**: Central database connected to web server configurations.

This architecture is designed for high traffic volumes, providing resilience and scalability. It includes Cloudflare for enhanced performance and security, and web monitoring tools for system health.

## APIs

### Member Routes
- `GET /api/v1/members`: Retrieve all members.
- `POST /api/v1/members`: Create a new member.
- `GET /api/v1/members/{memberId}`: Retrieve a member by ID.
- `PUT /api/v1/members/{memberId}`: Update a member's information.
- `DELETE /api/v1/members/{memberId}`: Delete a member.

### Savings Routes
- `GET /api/v1/members/{memberId}/savings`: Retrieve all savings for a member.
- `POST /api/v1/members/{memberId}/savings`: Add new savings for a member.

### Dependents Routes
- `GET /api/v1/members/{memberId}/dependents`: Retrieve all dependents for a member.
- `POST /api/v1/members/{memberId}/dependents`: Add a dependent to a member.

### Role Routes
- `GET /api/v1/roles`: List all roles.
- `POST /api/v1/roles`: Create a new role.

### Alerts Routes
- `GET /api/v1/alerts`: List all alerts.
- `POST /api/v1/alerts`: Create a new alert.

### Welfare Routes
- `GET /api/v1/welfares`: List all welfare entries.
- `POST /api/v1/welfares`: Create a new welfare entry.

### Transactions Routes
- `GET /api/v1/transactions`: List all transactions.
- `POST /api/v1/transactions`: Record a new transaction.

### Beneficiary Routes
- `GET /api/v1/beneficiaries`: List all beneficiaries.
- `POST /api/v1/beneficiaries`: Add a new beneficiary.

### Financial Transparency
- `GET /api/v1/welfares/{welfareId}/financials`: Provide a financial summary for the welfare group.

These routes provide a RESTful API structure for managing different entities within our web application, with CRUD operations for each entity.

## Getting Started

To get a local copy up and running, follow these simple steps.

### Prerequisites

- Python 3.8+
- MySQLDB

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/AbuArwa001/welpurse.git
   ```
2. Install required packages
    ```sh
    pip install -r requirements.txt

3. Run the application
    ```sh
    python app.py
## THIRD PARTY APIs

### Authorization
- **Access Token**: Provides a time-bound access token to call allowed APIs.
- **Endpoint**: `GET https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials`
- **Usage**: Generates tokens for API call authentication. It is the first API to engage with as other APIs require its authentication information.

### Account Balance
- **Enquiry**: Checks the balance on an M-Pesa BuyGoods (Till Number).
- **Endpoint**: `POST https://sandbox.safaricom.co.ke/mpesa/accountbalance/v1/query`
- **Usage**: Requests the account balance of a shortcode for B2C, buy goods, and pay bill accounts.

### Customer To Business Register URL
- **Registration**: Registers validation and confirmation URLs on M-Pesa.
- **Endpoint**: `POST https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl`
- **Usage**: Works with C2B APIs to receive payment notifications. Requires Validation URL for payment detail validation and Confirmation URL for payment completion notification.

### Transaction Status
- **Check**: Verifies the status of a transaction.
- **Endpoint**: `POST https://sandbox.safaricom.co.ke/mpesa/transactionstatus/v1/query`

## Data Modelling

![database](https://www.dropbox.com/scl/fi/m3zxsy11yc4wrs5n0fe1g/WelfPurse.png?rlkey=uu9bjokkulu7p5ak7wyfgy2kn&st=rp7kkqi0&dl=0)

### USER STORIES

**User Story 1: Create a Welfare Group**
- **Role**: Community leader
- **Goal**: Create a new welfare group on the platform
- **Purpose**: Start a community fund for life events
- **Acceptance Criteria**: Access to "Create Group" option, set group details, define roles, and invite members.

**User Story 2: Make Contributions**
- **Role**: Welfare group member
- **Goal**: Make regular contributions
- **Purpose**: Remain active and support the fund
- **Acceptance Criteria**: Contribute via dashboard, select amount and payment method, receive confirmation.

**User Story 3: View Financial Status**
- **Role**: Welfare group treasurer
- **Goal**: Access financial overview of the fund
- **Purpose**: Manage and ensure transparency
- **Acceptance Criteria**: Special dashboard, generate reports, alerted to discrepancies.

**User Story 4: Benefit Distribution**
- **Role**: Bereaved welfare group member
- **Goal**: Request financial aid for funeral expenses
- **Purpose**: Receive timely support
- **Acceptance Criteria**: Submit request, upload documentation, receive updates, and funds transfer.

**User Story 5: Secure Login and Account Management**
- **Role**: User
- **Goal**: Securely log in and manage account
- **Purpose**: Protect personal and financial information
- **Acceptance Criteria**: Use username and password, two-factor authentication, manage security settings, report unauthorized access.

### Contributing
Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are greatly appreciated.

### License
Distributed under the MIT License. See LICENSE for more information.

### Contact
- Khalfan Athman - [@athman_khalfan](https://x.com/athman_khalfan) - khalfanathman12@yahoo.com
- Magdalene Njeri - []() - mkirii@gmail.com
- Chioma  - []() - khalfanathman12@yahoo.com

Project Link: https://github.com/AbuArwa001/welpurse.git