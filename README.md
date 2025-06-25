testedPOC: Ansible Playbooks for GCP AI/GPU Infrastructure

This repository contains tested Ansible playbooks to automate the provisioning of Google Cloud Platform (GCP) infrastructure for AI/GPU workloads, GKE clusters, and supporting components.

Key Features

- Provision GPU-enabled VM with NVIDIA L4 for AI workloads
- Setup VPC, subnet, firewall rules, Cloud NAT, and router
- Deploy Linux and Windows node pools in GKE
- Install Jenkins, OpenSearch, Redis, and Camunda via Helm
- Configure Cloud SQL, Pub/Sub, GCS, and monitoring
- Modular playbooks for easier maintenance

Playbooks Overview

Playbook            | Description
------------------- | ------------------------------------------------------------
enable-api.yml      | Enables required GCP APIs
network.yml         | Creates VPC, subnet, firewall rules, NAT/router
compute.yml         | Provisions basic Compute Engine VMs
ai.yml              | Provisions AI GPU VM (nvidia-l4)
gke.yml             | Sets up GKE cluster with Linux/Windows nodes
applications.yml    | Installs services: Jenkins, Redis, OpenSearch
monitoring.yml      | Sets up monitoring stack
gcs_bucket.yml      | Creates GCS buckets
db.yml              | Provisions Cloud SQL and secrets
pubsub.yml          | Creates Pub/Sub topics and subscriptions

Prerequisites

- Ansible 2.14 or later
- Python 3 with google-auth and google-api-python-client
- GCP service account with necessary IAM roles
- Activated GCP project

Usage

1. Clone the repository:

   git clone https://github.com/nadeem-ha/testedPOC.git
   cd testedPOC

2. Configure your variables inside each playbook or in a shared vars file.

3. Run the playbooks in order:

   ansible-playbook -i localhost, enable-api.yml
   ansible-playbook -i localhost, network.yml
   ansible-playbook -i localhost, compute.yml
   ansible-playbook -i localhost, ai.yml

4. Use test.yml for isolated component testing.

Notes

- The .terraform directory is excluded from Git to avoid pushing large or machine-specific binaries.
- Do not commit service account keys or secrets. Use Vault or Secret Manager for secure handling.

Author

Nadeem Hassan  
DevOps Engineer at iSolution  
Email: nadeem.hassan@ismena.com  
GitHub: https://github.com/nadeem-ha

License

This project is licensed under the MIT License.
