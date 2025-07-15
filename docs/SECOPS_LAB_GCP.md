# Cybersecurity Operations Laboratory with Google Cloud Platform

This file documents my own lab set up to learn Google SecOps (formerly Chronicle) and GCP Security Command Center (SCC).

## Prerequisites

- Create a GCP account with a [Free Trial](https://cloud.google.com/free?hl=en) that includes **300 credits for 3 months** (If you are unsure about how the Free Trial credits work, visit this [page](https://cloud.google.com/free/docs/free-cloud-features#free-trial)).

```diff
- [!] Do not confuse the Free Trial with the Free-tier
```

- Create a GCP project
    - You can give it the name `scc-secops-lab`.

![GCP create new project](/src/images/scc-secops-lab/01-gcp-create_new_project.png)

- If you requested the Free Trial, you should see the following in the GCP project's homepage.

![New project homepage](/src/images/scc-secops-lab/02-gcp-new_project_homepage.png)

- To minimize the risk of being charged, set up your billing account settings.
    1. Click the `Set up budget alerts` option and click the `Create budged` button.
    2. You can name your budget alert `Cyber-Lab-Budget`
    3. Set an starting budget amount to give you a comfortable buffer. I selected `$150` as my initial budget.
    4. Set up threshold alerts. I created three thresholds at `50%`, `75%`, and `90$`, all of them to trigger when the spend reaches that threshold.
    5. Save the budget alert.

![GCP project budget alert](/src/images/scc-secops-lab/03-gcp-project_budget_alert.png)

```diff
+ [!] It is a best practice to always keep track of your cloud resources consumption and billing. In any case, we will allow billing for the account later to enable the creation of Windows Server VMs, and this alert will keep us safe that we are not overconsuming our remaining credits.
```

With these settings done, you can start working in the lab.

## Enabling Security Command Center

1. In the GCP Console search bar, type `Security Command Center` and select it, or open the sidebar and go to `Security > (Security Command Center) Risk Overview`.
2. Enable SCC by following the next steps:
    1. In the "Security Command Center - Get started today" webpage, click the `Get Security Command Center` button ([picture](/src/images/scc-secops-lab/04-gcp-get_scc_webpage.png)).
    2. In the "Select a tier" tab, choose the Premium tier ([picture](/src/images/scc-secops-lab/05-gcp-select_scc_tier.png)).
    4. In the "Select services" tab, keep the default settings and click `Next`.
    5. In the "Grant roles" tab, chose the option `Grant roles automatically` and click `Grant roles`. Then click the `Next` button.
    6. In the "Complete setup" tab, click the `Finish` button. It may take a few minutes to save.

![SCC Risk Overview Page](/src/images/scc-secops-lab/06-scc-risk_overview_page.png)

With this set up, you should have [Project-level](https://cloud.google.com/security-command-center/docs/activate-scc-overview) activated Security Command Center service.

## Enabling Google SecOps

```diff
- [!] Enabling Google SecOps requires that your organization contacts a Google Cloud Partner.
```

## Setting up the Warm-up Lab

The resources we create will trigger a broader range of findings thanks to the advanced detectors in the Premium tier.

### Publicly Exposed Storage Bucket

Open your GCP shell and paste the following command:

```Bash 
gcloud storage buckets create gs://my_vuln_bucket \
    --project={your-project-id} \
    --location=US \
    --default-storage-class=STANDARD \
    --uniform-bucket-level-access=false \
    --public-access-prevention=inherited \
    --soft-delete-policy-retention-duration=604800 \
    --no-public-access-prevention
```

You can refer to [`gcloud storage buckets create` Reference](https://cloud.google.com/sdk/gcloud/reference/storage/buckets/create#FLAGS) for more information on how to use the command line to create buckets for storing objects.

If you prefer to create the bucket manually, follow the next steps:

1. Navigate to `Cloud Storage > Buckets` and click the `Create` button ([picture](/src/images/scc-secops-lab/07-gcp_storage-create_vuln_bucket.png)).
2. Choose a name for your vulnerable bucket. (E.g. `my_vuln_bucket`)
3. Select a multi-region location type.
4. Set the `Standard` default storage class.
5. **Uncheck** `Enforce public access prevention on this bucket`
6. Select `Fine-grained` access control option.
7. Click `Create` to create the bucket.

Once the bucket is created, go to the `Permissions` tab and click `Grant access` button. In the `New Principals *` field, type `AllUsers`. Then, assign the role `Storage Object Viewer`. Finally, click `Save`.

![Add AllUsers Storage Object Viewer Role](/src/images/scc-secops-lab/08-gcp_storage-add_allUsers_storageObjectViewerRole.png)

Now, upload a dummy file. I created a file named `my_passwords.txt` with the following content:

```
th1s_15_my_p455w0rd
th1s_15_4n0th3r_p455w0rd
4r3_y0u_try1ng_t0_h4ck_m3?
```

![Upload Dummy File](/src/images/scc-secops-lab/09-gcp_storage-upload_dummy_file.png)

With this set up done, you have a vulnerable cloud storage instance that adversaries can read from the internet.

```diff
+ [!] Take a look at SCC Risk Overview page. Do you notice something different?
```

### Create a Overly Permissive Firewall Rule

Navigate to `VPC Networks > Firewall`.

It is possible that a pop up appears, requiring you to enable the Compute Engine API ([picture](/src/images/scc-secops-lab/10-gcp_market-compute_engine_api.png)). Click `Enable` and wait a few seconds. After that, you'll be redirected to the "Firewall Policies" webpage.

Click `Create firewall rule` and follow the steps:
1. Name it `allow-all-ssh`.
2. You can add the description `Allow SSH for every source`.
3. Set the Source IPv4 ranges to `0.0.0.0/0`.
4. In the "Targets" dropdown menu, select `All instances in the network`.
5. Under "Protocols and ports", select `Specified protocols and ports` and check the `TCP` box. Then, type the port `2222`.

You can also run the following command in gcloud shell to create this firewall rule.

```bash
gcloud compute --project=scc-secops-lab firewall-rules create allow-all-ssh --description="Allow SSH for every source" --direction=INGRESS --priority=1000 --network=default --action=ALLOW --rules=tcp:2222 --source-ranges=0.0.0.0/0
```

You can refer to [`gcloud compute firewall-rules` Reference](https://cloud.google.com/sdk/gcloud/reference/compute/firewall-rules) for more information on how to manage Compute Engine firewall rules.

### Deploy a Virtual Machine with a Public IP

1. Navigate to `Compute Engine > VM instances`.
2. Click `Create instance` button.
3. Machine configuration:
    1. Name the VM instance `labws01` (**Use this name**, it will be required for a later practice).
    2. Select your prefered region (Great if you chose a "Low CO2" region!) and zone.
    3. Select an `E2` series machine
    4. For the machine type, select the `e2-small`.
4. OS and Storage configuration:
    1. Choose any linux-based operating system. I selected Ubuntu 22 Jammy.
    2. You can select the `Balanced disk` type for better I/O.
5. Data Protection:
    1. Select `No backups`
6. Observability:
    1. check the box `Install Ops Agent for Monitoring and Logging`
7. Security:
    1. Make sure the access scope option is `Allow default access`
8. Create the virtual machine.

You can also run this [gcloud shell script](/src/gcloud_scripts/scc-secops-lab/01-gcp-cengine-e2small_vm.gcloud.bash) to automatically create and deploy the VM.

```diff
- [!] Remember to STOP your VM every time you STOP working with your lab, like when going to sleep. This will reduce your GCP billing!
```

## LAB: Identify Vulnerabilities in your Google Cloud Environment with SCC

Now that we have a few GCP instances deployed, we can start exploring SCC insights.

### Explore SCC interface elements

To get started and learn about SCC, let's first play around and see what we have at our hands.

**Step 1**: Go to `Security > Risk Overview`

![SCC Risk Overview Page](/src/images/scc-secops-lab/13-scc-risk_overview_page.png)

In the risk overview page you find helpful informational cards that offer you a high-level overview of the security landscape of your Google Cloud environment.

**Step 2**: Navigate the `Risk Overview` page of SCC

Notice that at the top of the page, your have a notfication: "Get accurate attack exposure scores". According to [Google's documentation](https://cloud.google.com/security-command-center/docs/attack-exposure-learn#attack_exposure_scores):

> An attack exposure score is a measure of how exposed resources are to potential attack if a malicious actor were to gain access to your Google Cloud environment.

Unfortunately, [attack exposure scores and attack paths](https://cloud.google.com/security-command-center/docs/attack-exposure-learn) are only available at the organization level with SCC Premium and SCC Enterprise tiers.

> To use attack exposure scores and attack paths, you must activate the Security Command Center Premium or Enterprise tier at the organization level. 

For the scope of this documentation, we will not be diving deeper into this functionality.

Below the "Get accurate attack exposure scores" you have the actual SCC informational cards. These are:

| Card Title | Function | Highlights |
|:---:|:---:|---|
| Top [issues](https://cloud.google.com/security-command-center/docs/issues-overview) | Threats & Vulnerabilities | The most critical security risks identified within your cloud environment that require immediate attention (Only available in Enterprise-tier). |
| New threats over time | Threats | Time-line of detected threats in your cloud environment. |
| Top CVE findings on your virtual machines | Vulnerabilities | High-level overview of top vulnerabilities detected in your cloud environment. |
| Vulnerabilities per resource type | Vulnerabilities | List of top vulnerabilities grouped by resource-type in your cloud environment. |
| Active vulnerabilities | Vulnerabilities | List of top vulnerabilities in your cloud environment that have not been mitigated yet. |
| Identity and access findings | Cloud settings | Vulnerabilities related to IAM misconfigurations grouped by resource-type.  |
| AI Workload findings | Cloud settings | Violations of AI security policies. |
| Data security finding | Data | Top severity findings found in your data. |

```diff
- [!] Notice that the UI may change in the future. The cards listed above correspond to the cards found at the time of writing this file (July, 2025)
```

You will notice that we already have some vulnerabilities listed in some cards. Besides, yf you leaved your VM turn on a few hours, it is possible that some adversaries have already attacked your vulnerable machine. In that case, you would have also some detected threats (altough most of the detected threats are about consequenses of IAM misconfigurations, e.g. unauthorized access from unexpected location; or execution of malware).

**Step 3**: Inspect an active vulnerability

Look at the `Active vulnerabilities` card in the `Risk Overview` page of SCC. Select the `Findings By Resource Type` tab and identify the most severe findings. You should have

- 1 high severity finding in the `buckets` category
- 1 hight severity finding in the `compute.instance` category
- 3 high severity findings in the `Firewall` category

```diff
- [!] If you changed the configuration of your instances during the deployment of the services, you might have more or less vulnerabilities.
```

Click the unique high severity finding that is in the `buckets` category. **When you click any finding in the `Risk Overview Page`, you are redirected to the `Findings` tab in SCC**.

![SCC Findings: Public Bucket ACL](/src/images/scc-secops-lab/14-scc_findings-public_bucket_acl_finding.png)

In this new dashboard, you have the opportunity to start investigating findings, i.e., security related events. Since we clicked a specific finding in the `Risk Overview Page`, we already have some **Quick filters** applied. Can you mention them? 

(The answer is in the raw markdown file below this line)

[Finding Class: Misconfigurations, Vulnerability; Resource Type: Google Cloud storage bucket; Severity: High]: #

You can also see in the **Query preview** a long string that represents the query used to search for that particular finding. The language is easy to understand, and still, you do not need to learn it, as there are very straightforward checkboxes in the **Quick filters** section.

Now, click the `Public Bucket ACL` finding.

![SCC Findings: Public Bucket ACL Information Panel](/src/images/scc-secops-lab/15-scc_findings-public_bucket_acl_finding_information.png)

An informational block will appear from the side giving us more context about the finding. At the top right corner (A), we have the `x` button to close the informational panel, two arrow buttons to move between findings (if there were more than one), and the `Take action` button, which we will cover later.

We also have a tab bar (B). The image above shows the `Summary` tab, but we also have the `Source properties` tab that shows some metadata about the finding, and the `JSON` tab, that shows the raw finding in JSON form. You can read more about viewing details of a finding in [this page](https://cloud.google.com/security-command-center/docs/review-manage-findings#finding-details).

As security analyst, we will mostly work in the `Summary` tab. You might also work with the `JSON` tab if you need to keep record of certain findings, or feed other security tools (We do not work or consume the information of the `Source properties` tab for the reasons presented in [this part of the documentation](https://cloud.google.com/security-command-center/docs/review-manage-findings#information_on_the_source_properties_tab)).

In the `Summary` tab we also have the following sections:
- The "**What was detected**" (C) section, which shows imporatnt details about the finding that was detected. You can think of this section as an "Overview" of the finding.
- The "**Affected resource**" (D), which presents information about the resource that is associated with the finding.
- The "**Vulnerability**" (Not in the image), which shows information from the CVE record that corresponds to the vulnerability.
- The "**Next steps**" (Not in the image), that provides guidance on what you can do to remediate the issue detected.

There are other sections too, like "Security Marks" (E). You can read about them in [Learn about the finding in the detail view](https://cloud.google.com/security-command-center/docs/review-manage-findings#learn_about_the_finding_in_the_detail_view).

**Step 4**: Solve the vulnerability

Refer to the "Next steps" sections of the finding details panel and follow the instructions that SCC gives you. You should be able to solve the vulnerability quickly.

![SCC Findings: Public Bucket ACL Next Steps](/src/images/scc-secops-lab/16-scc_findings-public_bucket_acl_finding_next_steps.png)

Once you [remove the `allUsers` principal](/src/images/scc-secops-lab/17-gcp_storage-remove_allUsers_principal.png) and [enable `Prevent Public Access` setting](/src/images/scc-secops-lab/18-gcp_storage-enable_preventPublicAccess.png), close the tab and return to SCC. You will notice that in the "What was detected" section, the **State** is set to `Inactive`, and the **Deactivation reason** is `Remediated`.

![SCC Findings: Public Bucket ACL Remediated](/src/images/scc-secops-lab/19-scc_findings-public_bucket_acl_finding_remediated.png)

**Step 5**: Try remediate another `High` severity vulnerability

Inspect one or two more vulnerabilities in your environment and remediate them. 

Ideally, you should remediate all of them, starting from the most severe vulnerabilities to the lesser (Given said that, you do not need to worry much about the `Low` severity findings).

## SCC and Google SecOps

You might be wondering what is are the differences (technical and operational) between Google SecOps and Google Security Command Center. The table below provides a detailed comparison between different main characteristics of both security solutions.

| Feature / Focus Area                  | Security Command Center (SCC)               | Google Security Operations (Chronicle)            |
|---------------------------------------|--------------------------------------------|---------------------------------------------------|
| **Primary Scope**                     | GCP cloud-native security posture, threat & vulnerability management | Enterprise-wide SIEM for logs & detections from on-prem, cloud, hybrid |
| **Typical Data Sources**              | GCP assets (Compute Engine, GKE, Storage, IAM, etc.) | Logs from endpoints, firewalls, AD, on-prem servers, GCP/AWS/Azure |
| **Detection Type**                    | Misconfigurations, vulnerabilities, built-in threat detections on GCP resources | Behavioral detections, correlation, threat hunting across logs (YARA-L) |
| **Asset Inventory & Posture**         | Yes - native GCP asset inventory & posture management | No - focuses on log and event analysis, not config posture |
| **Log Ingestion**                     | No traditional log ingestion (not a SIEM)    | Massive scalable log ingestion (petabytes/day) from any source |
| **Threat Hunting**                    | Limited to findings & cases on GCP assets    | Advanced threat hunting with YARA-L, pivoting, timeline views |
| **Compliance Checks**                 | Yes - built-in checks (CIS, PCI, etc.) for GCP configurations | No direct compliance config checks, but can detect policy violations in logs |
| **Data Retention**                    | Focused on current posture & findings       | Multi-year retention (up to 5+ years) for logs, long-term investigations |
| **Incident Cases / Management**       | Groups related findings into cases for analysts | No native case management, integrates with SOARs or ticketing systems |
| **Integrations**                      | Native to GCP services, some third-party scanner ingestion via API | Ingests from EDRs, firewalls, proxies, SaaS, cloud logs, SIEM connectors |
| **Typical Users**                     | Cloud security posture teams, DevSecOps, cloud infra teams | SOC analysts, threat hunters, DFIR teams, incident responders |
| **Deployment / Scope**                | Focused on securing GCP environment         | Global: on-prem, multi-cloud, SaaS environments (not tied to GCP only) |
| **Data Analysis Engine**              | Built-in GCP findings, case grouping, posture graphs | Google’s global-scale analytics engine (ex-Backstory), high-speed correlation |
| **Custom Detection Content**          | Limited to enabling/disabling built-in detectors | Full custom rules using YARA-L, with rich event context & replay |
| **Security Analytics Focus**          | Vulnerabilities, misconfigs, IAM risks, cloud threats | Advanced detection across events, anomaly hunting, threat correlation |

In short, **SCC is best for securing your GCP cloud environment itself**, while **Google SecOps is best for enterprise-wide detection regardless of where the data comes from**.

## Setting up the Real Lab


### Prerequisites

**Google Cloud Prerequisites**
- TODO

**Azure Prerequisites**
-TODO

**On-premise Prerequisites**
- TODO

### Setting up the Lab - Part 1: Cloud Connectivity

**Part 1.1: Create Azure Virtual Network**

1. Create a **resource group** named `scc-secops-lab` like the GCP project.
2. Create a **virtual network** named `azure_to_google_network`.
    - In the "IP address" tab configure the VNet subnet. (E.g. `10.0.1.0/24`)
3. Create a **virtual network gateway** named `azure‑to‑google‑gateway`

In the table below are all the settings that you need to know:

| Variable | Cloud | Resource | Suggested Values |
|---|---|---|---|
| AZURE_VNET_NAME | Azure | VNETWORK | azure_to_google_network |
| AZURE_VNET_SUBNET | Azure | VNETWORK | 10.0.1.0/24 |
| AZURE_VNETGW_NAME | Azure | VNET GATEWAY | azure‑to‑google‑gateway |
| AZURE_VNETGW_VNET | Azure | VNET GATEWAY | azure_to_google_network |
| AZURE_VNETGW_IP_NAME | Azure | VNET GATEWAY | azure_to_google_network_ip1 |
| AZURE_VNETGW_IP2_NAME | Azure | VNET GATEWAY | azure_to_google_network_ip2 |
| AZURE_VNETGW_ASN | Azure | VNET GATEWAY | 65515 |
| AZURE_VNETGW_BGP_IP_0 | Azure | VNET GATEWAY | 169.254.21.1 |
| AZURE_VNETGW_BGP_IP_1 | Azure | VNET GATEWAY | 169.254.21.2 |
| AZURE_VNETGW_GW_IP_0 | Azure | VNET GATEWAY | $(azure_to_google_network_ip1) |
| AZURE_VNETGW_GW_IP_1 | Azure | VNET GATEWAY | $(azure_to_google_network_ip2) |

```diff
- [!] It might take a while for the Azure Virtual Network Gateway to create. This is because the AZURE_VNETGW_GW_IP_0 and the AZURE_VNETGW_GW_IP_1 take a while to be provided. In the meantime, you can continue with GCP set up.
```

**Part 2.2: Create Google Cloud Virtual Network**

1. Create a VPC Network and subnet
    - Go to `VPC Network > VPC Networks` and click the `Create VPC Network` button.
    - Name the VPC Network `google_to_azure_vpc`\
    - Add a subnet with the name `google-to-azure-subnet1` and network `10.0.2.0/24`
    - Set the dynamic routing to `Global`
2. Create a HA-VPN Gateway

Run the following command in cloud shell to create a HA-VPN Gateway:

```bash
export GCP_VPCNET_NAME="google-to-azure-vpc"
export GCP_DEFAULT_REGION="us-east1"

gcloud compute vpn-gateways create google-to-azure-havpngw \
   --network $GCP_VPCNET_NAME \
   --region $GCP_DEFAULT_REGION
```

When the HA-VPN Gateway is created, you will receive an output like this:

```bash
Creating VPN Gateway...done.

NAME: google-to-azure-havpngw
INTERFACE0: ($INTERFACE0)
INTERFACE1: ($INTERFACE1)
INTERFACE0_IPV6:
INTERFACE1_IPV6:
NETWORK: google-to-azure-vpc
REGION: us-east1
```

Keep note of the `$INTERFACE0` and `INTERFACE1` public IP addresses.

3. Create a Cloud Router
    - Search `Cloud Router` and click the button `Create router`.
    - Name the router `google-to-azure-cloudrt`
    - Assign the network `google-to-azure-vpc`
    - Set any unused ASN value between `64512-65534` or `4200000000-4294967294`. I used the ASN number `64514`.

[TODO Continue from here](https://cloud.google.com/network-connectivity/docs/vpn/tutorials/create-ha-vpn-connections-google-cloud-azure#create_a_peer_vpn_gateway_for_the_azure_vpn)