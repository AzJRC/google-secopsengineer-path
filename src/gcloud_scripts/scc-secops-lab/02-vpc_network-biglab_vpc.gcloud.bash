gcloud compute networks create scc-secops-labnet --project=scc-secops-lab --subnet-mode=custom --mtu=1460 --bgp-routing-mode=regional --bgp-best-path-selection-mode=legacy

gcloud compute networks subnets create vulnapp-rodc-net --project=scc-secops-lab --range=10.0.2.0/24 --stack-type=IPV4_ONLY --network=scc-secops-labnet --region=us-east1

gcloud compute firewall-rules create scc-secops-labnet-allow-icmp --project=scc-secops-lab --network=projects/scc-secops-lab/global/networks/scc-secops-labnet --description=Allows\ ICMP\ connections\ from\ any\ source\ to\ any\ instance\ on\ the\ network. --direction=INGRESS --priority=65534 --source-ranges=0.0.0.0/0 --action=ALLOW --rules=icmp

gcloud compute firewall-rules create scc-secops-labnet-allow-rdp --project=scc-secops-lab --network=projects/scc-secops-lab/global/networks/scc-secops-labnet --description=Allows\ RDP\ connections\ from\ any\ source\ to\ any\ instance\ on\ the\ network\ using\ port\ 3389. --direction=INGRESS --priority=65534 --source-ranges=0.0.0.0/0 --action=ALLOW --rules=tcp:3389