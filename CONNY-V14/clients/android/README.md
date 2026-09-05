# CONNY AI V14 Android Authentication

V14 Android authentication uses the shared HTTP contract:

- POST /auth/register
- POST /auth/login
- POST /auth/guest
- GET /auth/session
- POST /auth/logout

The authentication token must remain separate from the conversation
session ID.

The V13 Android project is intentionally not modified by this V14
integration run.
