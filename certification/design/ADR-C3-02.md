# ADR-C3-02: MongoDB for notifications on a DDS replica set across three availability zones

## Status

Proposed

## Context

Today MongoDB runs in a container inside the same and only virtual machine
(`05-architecture/decisions/records/ADR-020-hosting-azure-for-students.md`, `06-data/models.md` §7). If that machine
fails, the notifications service goes down completely: the reminders are not sent and the clients miss their
appointments. Section 4 of the design note chooses the `notifications` database as the critical data store, with an RTO
of 5 minutes and an RPO of 1 minute.

## Decision

Use the managed Document Database Service (DDS) of Huawei Cloud to run MongoDB as a replica set spread over three
availability zones, in an active-standby scheme: one primary node receives the writes and two secondary nodes keep a
copy all the time. If the primary fails, one secondary takes its place automatically.

## Alternatives considered

- Backup and Restore: restoring a database from a backup is a slow process. It does not meet our RTO of 5 minutes, so the app would stay without notifications for too long.
- MongoDB on one self-managed ECS server: it needs too much operational effort (patches, upgrades, configuring the replicas and the monitoring by hand) and loses the automation of a managed service.

## Consequences

- Positive: very high availability with automatic recovery (failover); if the main zone goes down, another node takes control in seconds without anyone stepping in.
- Negative: it costs more than one simple database, because three nodes are paid while they run in parallel all the time.
