# Google SecOps

## Google SecOps Ingestion and Enrichment

### Google SecOps Ingestion Methods

**SIEM Ingestion**

We use SIEM ingestion for raw or UDM-parsed ingestion from on-prem or cloud sources.

1. Feeds
	- Support AWS S3
	- Google Cloud Storage
	- Amazon Blob Storage sources

2. [GCP Direct Ingestion](https://cloud.google.com/chronicle/docs/ingestion/default-parsers/ingest-gcp-logs#export-logs)

```diff
- [!] The user interface has changed. Investigation for GCP direct ingestion or Google assistance might be needed.
```

3. Google SecOps Forwarder
    - Docker solution that can forward data and security events to Google SecOps.
    - Requires a Forwarder Configuration File.
    - A forwarder specifies one or more collect configurations that specifies the collector's ingestion mechanism (network (pcap), splunk, file, syslog, web proxy, and kafka).

4. [Chronicle API](https://cloud.google.com/chronicle/docs/reference/ingestion-api)

```diff
- [!] Ingestion via Chronicle API is an advanced topic not covered in this documentation.
```

5. Ingestion via BindPlane Agent
    - Only supported software solution for end-to-end ingestion.
    - Included with Google SecOps Enterprise+ license.

**SOAR Ingestion**

We use SOAR ingestion to ingest other SOAR alerts from third-party solutions (think of Splunk or Elastic SOAR)

1. Connectors
    - Requires an integration (API/parser for the third party solution)
    - The connector uses a **pull model** to gather data from the third party solutions 
    - The integrations of a connector gives you options for actions that you can use in your SOAR playbook.
    - A connector might not have an integration

> [...] Slack has an integration in the marketplace so you can make playbooks using actions specific to the product, but it has no connector.

2. Webhooks
    - Lightweight solution to ingest organization alerts to the platform.
    - In contrast to connectors, this use a **push model**.


```diff
- [!] For each product you ingest alerts, choose either a connector or a webhook ingestion method, but not both.
```

### More About Ingestion


- **Namespaces**: Used in environments where we have local IP address collisions.
- **Ingestion Labels**: Used to provide more information about the ingestion.

```diff
+ [!] Always include the Environment (`env`) label to tag ingestion logs. Typical values are `prod` and `test`.
```

**Data Access**

TODO

**Log Types**

TODO

**Entity Risk Scores**

TODO


### Google SecOps Data Normalization 

**Normalization basics in Google SecOps**

- There are two normalization schemas in Google SecOps:
    - The **UDM**, or Unified Data Model
    - The **EDM**, or Entity Data Model (also refered as GDP or Graph Data Model)
- UDM recods events, while EDM records (temporal or permanent) states
    - A LogIn event (which includes details of when and how it occurent) is a UDM event
    - A UserAccount (which includes context of who and what is it) is an EDM entity
- The UDM schema follows a sentence model
- UDM normalization requires parsers. You can find them in `Settings > SIEM Settings > Parsers`.
- 

### Google SecOps Data Enrichment
