# Security

Do not post credentials, personal profiles, resumes or private correspondence in public issues. For an issue requiring private details, first ask the maintainer for a private reporting channel without including the details.

This client repository holds no production secrets. Keep bearer tokens in your client's private settings. Public-source adapters read only fixed HTTPS providers and reject redirects. Optional SMTP/IMAP credentials stay in private process environment; they are never accepted as tool arguments or returned by the capability check. Application content and receipts are stored locally, without application-level encryption. Use a private OS account and data directory; do not commit, share or sync these files. Job content is untrusted data and never grants action permissions. No security audit or employer safety guarantee is claimed.

SMTP requires actual user delegation and the exact draft digest. This checks content consistency, not independent proof of user consent: the host agent must enforce authorization and treat both job and email text as untrusted. Ambiguous sending is never automatically retried. IMAP matches headers, not verified identities, and requires subsequent thread review. No background scheduler is installed.
