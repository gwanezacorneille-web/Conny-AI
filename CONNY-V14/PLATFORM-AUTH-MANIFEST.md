# CONNY AI V14 Cross-Platform Authentication

## Authentication endpoints

POST `/auth/register`

POST `/auth/login`

POST `/auth/guest`

GET `/auth/session`

POST `/auth/logout`

## Clients

- Web
- Android
- Windows
- Linux

## Security boundary

V14 authentication tokens are separate from conversation session IDs.

## V13 protection

V13 remains frozen and is not modified by this integration layer.

## Cross-device model

A private account receives a persistent V14 authentication session.
The same account can authenticate from multiple supported clients.

## VIP

VIP credentials are supplied through:

CONNY_VIP_USERNAME

CONNY_VIP_SECRET

They are never stored in source code.
