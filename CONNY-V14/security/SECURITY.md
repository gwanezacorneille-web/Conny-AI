# CONNY AI V14 Security

## Authentication

Private and VIP accounts use V14 sessions.

Invalid, expired, and revoked sessions are rejected.

## Authorization

Permissions are controlled by account type:

- Guest
- Private
- VIP

VIP-only permissions are unavailable to Guest and Private accounts.

## Memory isolation

Persistent memories are associated with a user ID.

Memory reads and deletes are always scoped to that user ID.

## Secrets

VIP credentials are supplied through environment variables.

Secrets must never be committed to Git.

## Audit

Authentication and authorization events can be written to the
security audit log.

## V13 boundary

V13 remains frozen and is not modified by V14 development.
