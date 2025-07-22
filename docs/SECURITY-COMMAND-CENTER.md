# Security Command Center Notes

## Handling Cloud Security

Organizations typically have different teams (or sometimes different individuals) handling cloud security — think proactive protection like posture management, vulnerability management, data protection, and identity management — versus enterprise security operations (SecOps), which is typically reactive, remediating threats and vulnerabilities after the fact.

- SCC is a multi-cloud security solution.
- Mostly proactive: Posture management, vulnerability management, data protection, identity management, (plus some threat detection).
- Mostly reactive: Threat management, incident response.
- SCC helps organizations prevent, detect, and respond to security risks.

## Security Command Center (SCC)

- Cloud-first risk management solution.
- Groups cloud risks into cases for easier prioritization and management.
- Offers:
  - Proactive discovery/scanning of the cloud environment.
  - Determines potential impact and priority level of identified risks.
  - Creates cases with grouped incidents.
  - Enriches cases with correlated data.
  - Leverages Gemini AI to simplify analysis.
  - Includes support for automation with playbooks.
- Helps analysts focus on cases rather than individual, isolated findings.

### Core Functionality

#### Cloud Security Posture Management (SPM)

- Assesses your environment by combing through and validating configurations, software, and compliance rules.
- The goal is to uncover hidden misconfigurations that lead to system, software, or environment-level vulnerabilities.
- SCC tools for SPM:
  - **Eyes on the Ground**
  - **Zeroing in on Hazards**
  - **Prioritizing for Efficient Response**

#### Continuous Risk Engine (CRE)

- Helps keep your organization at the same level of sophistication as evolving attacker tactics and techniques.
- Prioritizes risks that could affect your cloud environment (proactive).
- Key features:
  - Maps and highlights the most critical assets needing higher attention.
  - Mimics real-world tactics and techniques to validate your cloud security posture.
  - Supports advanced behavioral scans to identify intricate methods of compromising your environment.
  - Scores risks to help you prioritize.
  - Dashboards provide a high-level overview of your overall cloud security posture.

#### CRE Attack Path Simulation (APS) Feature

- Supports advanced behavioral scans and automated red team simulations to validate your security posture.
- Features:
  - Generates a map (diagram) of your cloud environment.
  - Runs simulations in non-live cloud instances.
  - Probes different tactics and techniques adversaries might use to access high-value assets like databases or storage.

#### SOAR

- SCC integrates a SOAR capability similar to Chronicle SOAR.

#### Gemini AI

- Provides support for Gemini AI, offering plain-language summaries without tech slang.
- Helps describe risk scenarios and threats in an easily digestible way.

#### Summary of SCC Core features

- **Discovers proactively:** Surveys your cloud environment for misconfigurations, vulnerabilities, and active threats, offering detailed visibility and actionable intelligence.
- **Integrates with the Risk Engine:** Provides a comprehensive, continuous view of cloud risks and prioritizes events so top risks can be addressed quickly by the right teams.
- **Provides attack path simulation:** Acts as counterintelligence to expose an attacker’s route before they strike.
- **Integrates with Chronicle SOAR:** Helps resolve security issues faster by reducing the backlog of unresolved risks through integrated workflows connecting threat prevention, detection, and response.
- **Detects multi-cloud threats:** Uses Google’s capabilities to extend protection to AWS and Azure.
- **Integrates with Gemini:** Your AI analyst tirelessly processes mountains of data to safeguard your environment.

### SCC Additional Features

#### Infrastructure as Code (IaC) support

- SCC validates IaC templates, identifying misconfigurations and potential risks before launching infrastructure to production.
    - SCC enforces consistent standard templates. Helps you apply the same security baselines to your cloud environment.
    - IaC validation is integrated into the CI/CD pipeline flagging any potential security risk while development is ongoing.
    - The IaC validation API allows you to customize the severity and frequency of checks.
    - IaC validation hast the best compatibility with Terraform, offering better and faster results.

#### Secure Software Supply Chains (SSC)

Often, applications depend on third-party solutions from other developers or vendors. What if these supplier's software had vulnerabilities?

> **Insecure software libraries can undermine even well-coded applications**

In an effort to solve risks associated with SSC, SCC includes Google's Assured Open Source Software (AOSS), i.e., software that had been validated and tested by Google.

- **Trusted supply**: Software that had been green-flaged by Google.
- **Rapid Response**: Quick incident response and remediation from Google advanced scanning in case if flaws are detected.
- **Signed and sealed**: Delivered software can be verified.

#### Security for Google Cloud

Altough SCC is meant to be used with different cloud platforms, the truth is that this is a Google product; hence, it is best at protecting Google's products.

SCC can identity identity-driven attacks:

- **Insider threats**: SCC is connected with Google's core identity platform services: Google IAM and Google Groups. It helps spot inconsistencies and incidents where identities are compromised or being used nefariously.
- **Privacy by design**: SCC's identities are protected and encrypted by design, using meticulous privacy controls.

#### Threat Intelligence

SCC has Mandiant expertise and functionality integrated. Mandiant is a trust partner of Google whose primary role is in the field of Cybersecurity Threat Intelligence.

> Mandiant experts see what's happening on the frontlines of cyberattacks, analyzing thousands of incidents each year.

#### SCC Sensitive Data Protection Services (SDPS)

SDPD allows to ensure that sensitive data has the right security, privacy, and compliance posture and security controls.

- SDPS leverages AI-driven classifiers to categorize your sensitive data.
- SDPS supports and understands unstructured data.

#### SCC Cloud Identity and Entitlement Management (CIEM)

The SCC CIEM (Do not confuse with SIEM) helps enforce authorization access to cloud instances and services.

- CIEM analyzes access rights and suggests which permissions to revoke, enforcing *least privilege*
- CIEM monitors cloud service accounts to ensure that they are not being misused.

#### SCC Additional features wrap-up

- **Validate IaC**: Lets you define policies that constrain how, and where, cloud resources can be deployed so that a strong security posture can be established at the outset using the same policy for code to cloud.
- **Secure SSC**: Allows customers to reduce their software supply chain risk by using the same OSS packages that Google uses. 
- **Detects Google Cloud threats**: SCC uniquely understands how your cloud services are supposed to function, allowing it to spot suspicious deviations other tools might miss.
- **Mandiant Threat Intelligence**: Brings Mandiant functionality into SCC, you can continually make your cloud defenses smarter and adapt to the latest cyber-attack strategies.
- **Protect Sensitive Data**: Allows you to manage your sensitive data to ensure that it has the right security, privacy, and compliance posture and controls.
- **CIEM**: Safeguards your cloud environment by enforcing strict identity controls, ensuring users and services only have the access they need to function, minimizing the risk of unauthorized activity.

## Vocabulary and Key Terminology

By this part of the lecture, you should already be familiar with some Google Cloud Services names and acronyms.

You can review this section to remember the meaning of all acronyms and terms found in this document:

## Glossary of Acronyms and Key Terms

| **Term / Acronym** | **Meaning / Explanation** |
|---------------------|--------------------------|
| **AOSS** | Assured Open Source Software — Google-validated open source software packages. |
| **API** | Application Programming Interface — set of protocols and tools for building software and integrations. |
| **APS** | Attack Path Simulation — feature in SCC’s CRE that simulates adversarial paths to high-value assets. |
| **CI/CD** | Continuous Integration / Continuous Deployment — automates software build, test, and deployment processes. |
| **CIEM** | Cloud Infrastructure Entitlement Management — governs identities and access privileges in cloud environments. |
| **CNAPP** | Cloud Native Appplication Protection Platform - A comprehensive security solution designed to protect cloud-native applications and workloads throughout their lifecycle. SCC is a CNAPP. |
| **CRE** | Continuous Risk Engine — continually evaluates risks in your cloud environment. |
| **Gemini AI** | Google’s generative AI technology used here to simplify risk and threat analysis. |
| **IAM** | Identity and Access Management — controls user identities and their access to resources. |
| **IaC** | Infrastructure as Code — managing infrastructure via machine-readable definition files. |
| **Least privilege** | Security principle ensuring users/services have only the minimum necessary access. |
| **Mandiant** | Cybersecurity company owned by Google, provides threat intelligence and incident response. |
| **Multi-cloud** | Strategy or tooling that spans multiple cloud providers (GCP, AWS, Azure). |
| **Playbooks** | Automated or guided workflows for responding to security incidents. |
| **Posture management** | Ensuring systems are securely configured to minimize exposure. |
| **SCC** | Security Command Center — Google’s cloud-native security and risk platform. |
| **SDPS** | Sensitive Data Protection Services — manages sensitive data security, privacy, and compliance. |
| **SecOps** | Security Operations — reactive operations that handle incidents, threats, and vulnerabilities. |
| **Security Posture** | Overall health and security status of your cloud environment. Involves elements like firewall configurations, minimized vulnerabilities, ecryption usage, secure defaults, etc. |
| **SIEM** | Security Information and Event Management — manages security logs and events (mentioned for clarity vs CIEM). |
| **SOAR** | Security Orchestration, Automation, and Response — automates and integrates security operations processes. |
| **SPM** | Security Posture Management — assesses and manages the security configuration of your cloud. |
| **SSSC** | Secure Software Supply Chain — securing software dependencies and third-party components. |
| **Threat Detection** | Monitor for signs of unauthorized activity, like intrusion, unusual data patterns, malicious software, among others. |
| **Terraform** | Popular open-source IaC tool used to provision and manage cloud resources. |
| **Threat intelligence** | Information that helps understand threats and adversaries. |
| **Vulnerability Management** | The continuous scanning and remediation of cloud weaknesses, like outdated softare, misconfigurations, or unpatched systems. | 

## SCC Options

SCC comes in three different flavors, tailored for distinct organizational needs and resources.

### SCC Enterprise

- **Multi CNAPP**: Extended support covering AWS and Azure cloud providers.
- **Advanced SecOps**: Support for remadiation tools and Mandiant Threat Intelligence insights that helps organizations bolster their defenses against cyber attacks.

This solution is best suited for organizations needing robust security across multiple cloud providers. **SCC enterprise uses a subscription-based pricing model**.

### SCC Premium

- **Google Cloud Posture Management**: Helps you mantain an optimal stance across google cloud.
- **Attack Path Simulation**: Provides insights into potential vulnerabilities that could be exploited by threat actors.
- **Threat Detection**: Leverages Google's expertise to identify specific Google Cloud threats.
- **Compliance Monitoring**: Helps you mantain on top of regulatory requirements.

SCC Premium is best suited for organizations with only Google Cloud resources that need proactive and in-depth security. **SCC premium uses a pay-as-you-go pricing model** (users pay for a service or product based on their actual usage).

### SCC Standard

- **Basic Posture Management**: Essential visibility into security configurations settings and potential vulnerabilities in Google Cloud.

**SCC Standard comes at no additional cost**. Organizations with smaller Google Cloud deployments can benefit from SSC Standard.

### Choose Cheat Sheet

- **Multi-cloud Needs**: If you manage assets on AWS or Azure, SCC Enterprise is essential.
- **Threat Detection and Remediation**: For a streamlined security response, consider SCC Enterprise's built-in SecOps features.
- **Budget and Growth**: Opt for SCC Premium if focused on Google Cloud with flexible pricing, or use SCC Standard as your first line of defense if cost is a major factor.

Notice that This information may change in the future. Always refeer to the official documentation:

- General information about Google Security Command Center (SCC) is available on the [official overview page](https://cloud.google.com/security-command-center/docs/security-command-center-overview).
- Details about SCC service tiers can be found in the [service tiers documentation](https://cloud.google.com/security-command-center/docs/service-tiers).
- Pricing information is provided on the [pricing page](https://cloud.google.com/security-command-center/pricing).

## Getting Started with SCC

You can find this laboratory in [Google Cloud Skills Boost: Get Started with Security Command Center ](https://www.cloudskillsboost.google/paths/2150/course_templates/960/labs/528604)

### Lab Prerequisites in a Nutshell

The laboratory recommends

- Know cloud computing concepts
- Know the Google Cloud Console
- Know the SCC severity classifications

For the first prerequisite, you should know that cloud computing is the delivery of computing resources, such as servers, storage, databases, networking, software, and analytics, over the internet (“the cloud”) on a (typical) pay-as-you-go basis. 

Its core concepts include **on-demand self-service**, allowing users to provision resources as needed; **broad network access**, meaning services are accessible over the internet from various devices; **resource pooling**, where providers serve multiple customers with shared infrastructure; **rapid elasticity**, enabling quick scaling up or down; and **measured service**, ensuring transparent usage and billing. These principles let organizations achieve **flexibility, scalability, and cost efficiency**, freeing them from maintaining physical hardware.

For the second prerequisite, we will be covering Google Cloud Console at the same time we cover Security Command Center.

Finally, for the latter prerequisite, you can check [Finding severities](https://cloud.google.com/security-command-center/docs/finding-severity-classifications) in official documentation of Google Cloud. But in short, **SCC assigns findings one of five severity levels**:

- **Critical**: Easily discoverable and exploitable flaws that allow code execution, data exfiltration, or unauthorized access to resources (e.g., public SSH with no password). Critical misconfigurations or threats can lead to full compromise of cloud resources
Google Cloud+9Google Cloud+9Google Cloud+9

- **High**: Serious vulnerabilities that require chaining with others to achieve a critical outcome, or threats that can provision resources but can’t directly access data or execute code
Google Cloud+2Google Cloud+2Google Cloud+2

- **Medium**: Vulnerabilities or threats that might not immediately lead to data loss or code execution, but could enable privilege escalation or foothold persistence over time
Google Cloud+3Google Cloud+3Google Cloud+3

- **Low**: Typically reflect weak security hygiene—such as missing logs or monitoring—that hinder detection and investigation, or minimal threats that can’t access data or execute code
Google Cloud+2Google Cloud+2Google Cloud+2

- **Unspecified**: Indicates that no severity was set by the detection service, requiring manual review to assess risk
Google Cloud+9Google Cloud+9Google Cloud+9

These are generally based on the impact of vulnerabilities or threats, with higher severities signaling more urgent remediation. Additionally, is worth to mention that **SCC also distinguishes between static severities, which are predetermined per category, and variable severities (Enterprise tier only), where severity can escalate dynamically** based on an attacker's ability to reach high‑value assets via attack exposure scoring.

### Lab

[TODO]

## Vulnerability Management

### Vulnerability Management Life-cycle

1. **Identification**: Actively scanning all your networks, systems, and applications is how you find those hidden vulnerabilities. 
2. **Analysis**: Figure out the severity and potential impact of each vulnerability you've found.
3. **Prioritization**: Focus on the most critical "entry points" first. Leverage risk assessments methodologies to target the vulnerabilities that pose the greatest threat to your business. 
4. **Remediation**: Remediation means taking action to fix the vulnerabilities. This involve **patching** your vulnerable systems, **harden** your systems by setitng up more secure configurations, and **update code** that is vulnerable.
5. **Reporting**: Documenting what you found, the actions you took, and your overall progress in securing your environment.

### Vulnerability scanning and assessment

You can identify vulnerabilities with scanners:

- **Network-based scanners**: Network-based scanners monitor and identify vulnerabilities in your entire network infrastructure.
- **Host-based scanners**: Focuses intently on individual devices (*laptops, servers, etc.*), scrutinizing their operating systems and installed software for any flaws or outdated components.
- **Application-based scanners**: Application-based scanners examine your web applications. These tools hunt for security flaws in the very code that makes applications run.

### Vulnerability scoring

Scoring vulnerabilities will help prioritize which vulnerabilities tackle first. The **CVSS - the Common Vulnerability Scoring System** is a well-known framework and standard whose main purpose is to score and evaluate vulnerabilities. They take those cryptic technical details about a vulnerability and translate them into a simple scale of severity (*Low, Medium, High, Critical*).

### Risk Assessment

Risk Assessment is about understanding what that vulnerability could actually  mean for your business. Knowing the potential impact lets you accurately prioritize and address different vulnerabilities.

### Risk Prioritization and remediation

There are different approaches to prioritize vulnerabilities, but one of the most common and used is **risk-based prioritization**. In this methodology, you use the vulnerability scores, along with the potential business impact that you identified from the risk assessment, to determine which issues need to be tackled first.

Once you identified the vulnerabilities that you need to address and in which order, the next step is fixing the vulnerabilities, which often requires teamwork across security and operations teams.

In certain scenarios, you cannot fix the issue immediately. Maybe the server running the vulnerable application is critical for business operations. That's where **compensating controls** come in. Think of them as temporary barriers to protect specific vulnerable areas. Some compensating controls include:

- **Network segmentation/isolation**: Dividing your network or separate the host from the network to contain a vulnerability.
- **Enhanced monitoring**: Extra-vigilant eyes on the vulnerable system.
- **Strict access control**: Limiting who can interact with the vulnerability.

### Vulnerability Management in SCC

[TODO]

## Threat Detection

Threat Detection, in contrast to vulnerability management that is mostly (but not completely) practive, is **reactive**. The focus of threat detection is to **identifying attackers in the act**, alerting when trouble is already brewing.

While Vulnerability Management reduces the number of ways attackers can even attempt to get in, i.e., reduce the attack surface; Threat Detection lets you catch attacks that slip through, giving you precious time to react and limit the damage.

### Cloud Threats

Some of the most common cloud threats are:

- **Data Exfiltration**: Theft of sensitive customer information, financial records, or your company's secret intellectual property.
- **Unauthorized Access**: Attackers try to steal credentials or exploit vulnerabilities to gain unauthorized access to your systems.
- **Malware**: Malware is malicious software designed to infect your cloud systems, disrupting operations or opening backdoors for attackers.
- **Cryptojacking**: Attackers hijack your cloud resources, using your computing power without permission to mine cryptocurrency.
- **Denial-of-Service Attacks**: DoS attacks aim to flood your cloud systems with traffic, making your legitimate users unable to access critical services.

Notwithstanding this, despite the benefits of cloud (flexibility and scalability), the cloud introduces unique secuity challeges:

- **Cloud misconfiguration**: Small mistakes in how you set up your cloud environment can be easily exploited by cunning attackers.
- **Vulnerable API**: Adversaries might take advantage of poorly designed APIs and perform unauthorized operations.
- **Cloud-provider vulnerabilities**: Attackers might try to exploit vulnerabilities in the cloud provider's own infrastructure.

### Threat detection methods

There are two common threat detection methodologies:

- **Signature-based detection**: Signature-based detection compares current activity against a database of known attack signatures. *E.g. Detecting a specific piece of malware based on its unique code or HASH signature*.
- **Anomaly-based detection**: This is about understanding what is *normal* and what is *abnormal*. Anomaly-based detection establishes a baseline of how your systems, applications, and users usually behave. Any significant deviation from that normal raises a red flag. *E.g. An unusual login from a new location or a sudden surge in data downloads*.

### Data sources

Threat detection cannot be accomplished without data.

- **Netowrk logs**: Shows the network traffic and how much data is moving.
- **Endpoint logs**: Detailed records of activity from individual devices (*servers, laptops, etc.*). These are particular useful to help track down malware or unauthorized access attempts.
- **Cloud audit logs**: Tracks all actions taken by users and services within your cloud environment. 
- **Aplication logs**: Records of what's happening within your applications, often web applications.

The more data you get, the better you can spot early signs of trouble.

## IAM Roles for SCC

- `Security Command Center Viewer`
  - View all findings
- `Security Command Center Admin`
  - View all findings
  - Manage finding statuses
  - Take remediation actions
  - Update security policies
