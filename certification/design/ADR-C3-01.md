# ADR-C3-01: A jump server in a separate O&M VPC instead of SSH to each server

## Status

Proposed

## Context

Today the access to the servers is not safe: the only virtual machine has a public IP, and port 22 (SSH) is open on
that public address, limited only to the operator's IP (`05-architecture/decisions/records/ADR-020-hosting-azure-for-students.md`,
Network). It is a public entry point that receives attacks all the time, and the model does not scale: in the target
design (section 1 and section 2, Security, of the design note) the services run on many ECS servers that Auto Scaling
creates and deletes, so opening SSH on each one is not possible.

## Decision

Use a jump server (bastion host) in a separate management VPC for operations and maintenance (`vpc-om`). This VPC is
connected to the main VPC (`vpc-primary`) with VPC peering, and a private DNS zone lets the support team find the
servers by name. The application servers have no public IP and no SSH rule from the Internet; the only way to reach
them is through the jump server.

## Alternatives considered

- Keep SSH open on each server, limited to one IP address (as today): it lowers the risk, but every server still has a public entry point, and it is not practical to keep the firewall rules up to date for every machine that Auto Scaling creates or deletes.
- Use a VPN to enter the network: setting up, paying for and maintaining a VPN gateway and the clients of every team member is more expensive and more complex for the support team than running one jump server.

## Consequences

- Positive: public access to the production servers is closed completely, and security is concentrated in one point that is tightly controlled and easy to audit.
- Negative: it adds a small step to daily operations, because the technical team must first connect to the jump server before reaching the final server.
