# Veridian Legal Hub: Student Dataset (Assignment 2)

All content is **synthetic and fictional**. Veridian Industries Limited, every counterparty, case, matter and
person is invented for teaching. Nothing here is legal advice.

## Contents

| Path | What it is |
|---|---|
| `documents/general/` | 3 PDFs + 1 Markdown file, visible to every role |
| `documents/contracts/` | Contract playbook, vendor MSA template, NDA clause library (Markdown), one matter-tagged memo |
| `documents/litigation/` | Litigation procedures and settlement matrix, one matter-tagged memo |
| `documents/compliance/` | Anti-bribery, data-protection, insider-trading code, one matter-tagged report |
| `documents/ip/` | Trademark and patent guides, one matter-tagged strategy note |
| `manifest.json` | For every document: `collection`, `access_roles`, `matter_id`. **Use this to build chunk metadata.** |
| `users_seed.json` | 8 demo users with role and matter assignments (demo passwords only) |
| `veridian_legal.db` | SQLite database with `contracts_register` and `litigation_cases` |

## Matters (ethical walls)

`matter_id` is `NONE` for ordinary documents and rows. Four sensitive matters exist:
`MTR-017`, `MTR-023`, `MTR-031`, `MTR-044`. Which documents and database rows belong to a matter is recorded in
`manifest.json` and in the `matter_id` column of both tables. Which users are on which matter is in `users_seed.json`
(`"*"` means all matters).

## Notes

* Inspect the database schema yourself before you design the SQL RAG prompt.
* Monetary columns are in **₹ lakh** (1 crore = 100 lakh). Dates are ISO `YYYY-MM-DD`.
* PDFs contain real tables and numbered headings; Markdown files contain fenced clause text.
