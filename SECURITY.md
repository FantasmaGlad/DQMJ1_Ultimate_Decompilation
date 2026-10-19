# Security policy

## Reporting a vulnerability

Please report security vulnerabilities **privately** and do not open a public issue.

- E-mail: **security@dqmj1.wiki**
- Encrypt your report with our public PGP key whenever it contains technical details or a proof of concept:
  <https://dqmj1.wiki/.well-known/pgp-key.txt>
- Fingerprint: `3C11 0D26 D95B A699 3DA0  FEF4 E8C7 6A2C 9D88 DB15` (RSA 4096, valid until 2028-10-06). Check it against the
  fingerprint published on <https://dqmj1.wiki/security> before trusting the key.
- Include your own public key so that we can reply encrypted.

Machine-readable policy (RFC 9116): <https://dqmj1.wiki/.well-known/security.txt>

## What to expect

| Step | Target |
|---|---|
| Acknowledgment of your report | within 5 business days |
| Initial assessment | within 10 business days |
| Fix of a confirmed vulnerability | as quickly as its severity requires |
| Coordinated public disclosure | up to 90 days after the report, or when a fix is released |

Reporters are credited in the acknowledgments unless they prefer to stay anonymous. This is a free, non-commercial project: there is no
bug bounty.

## Scope and rules

This repository contains decompiled source code and extraction tooling for a Nintendo DS game: it handles no user data and runs no
service. Reports about the tools (for example unsafe file parsing) are welcome. The full scope, the out-of-scope list and the
safe-harbor statement for good-faith research are on <https://dqmj1.wiki/security> (English, French, German, Italian and Spanish).

You can also use GitHub's private vulnerability reporting from the **Security** tab of this repository.
