# Resource intake and review

## Capture a URL

Open [Add a resource](https://github.com/lajirajg/enterprise-ai/issues/new?template=resource.yml), paste a public HTTPS URL and submit. Keep the `[Resource]` title prefix to trigger validation. The relevance note and capability IDs are optional. You do not need to decide where an article belongs before saving it.

The **Validate resource intake** action parses the issue as data and validates the URL, capability IDs and duplicates. A successful run provides a candidate JSON artifact under Actions. A failed run shows a fixed validation error; edit the issue and it reruns. There are no bot comments or automatic issue edits.

## Review and propose

A maintainer opens Actions → **Review resource intake** → Run workflow on `main`, supplies the issue number, and runs it. The action retrieves the current issue rather than trusting an old artifact, validates it again and opens a draft PR on `resource-intake/ISSUE_NUMBER`. Repeating a successful dispatch reports the existing PR without overwriting it. If a push succeeded but PR creation failed, the next run reports the existing branch; open a PR from that branch or inspect and remove it before retrying.

In the PR, review the original public source. Check relevance, provenance, misleading claims, publication date, access conditions and duplication. Replace the hostname title and placeholder summary, add canonical capability IDs, and set `reviewed_by` and `reviewed_on` when changing `status` to `curated`. Do not mark the record reviewed merely because a workflow passed. Candidates may be retained as a backlog but are not rendered as recommended resources.

Run:

```sh
python scripts/catalogue.py validate
python scripts/catalogue.py render
python -m unittest discover -v
python -m mkdocs build --strict
```

Commit the regenerated catalogue page with the resource record. Mark the PR ready after review, check CI, and merge through the normal review process. Close the source issue once handled. Automation never merges, closes an issue or marks a resource curated.

## Security boundaries

- Submitted URLs are never fetched by intake, so validation does not establish availability, authenticity or DNS safety. A human reviews the source using an appropriate browser environment.
- HTTPS, DNS hostnames and default ports are required. IP literals, obvious local hostnames, URL credentials and common signed/token query parameters are rejected. Tracking parameters and fragments are removed for duplicate detection; meaningful query parameters remain.
- Public issue content is untrusted. It is parsed into a fixed schema; no shell interpolation, embedded instructions, remote scripts or model summarisation are used.
- The automatic issue workflow has read-only repository permissions and only uploads an artifact. The manually dispatched workflow can write a candidate branch and draft PR, using trusted `main` scripts. It does not execute issue content.
- Candidate records are excluded from the recommended resource list. Rendered text is escaped, and curation requires explicit review metadata.
- Proprietary source documents and client information belong outside this public repository, including its issues and artifacts.

## Manual fallback

If repository policy disables workflow-created PRs, retrieve a candidate artifact, inspect it, and copy its JSON into `catalogue/resources/` on a local branch. Alternatively save issue JSON and run `python scripts/intake.py issue.json --issue-json --output catalogue/resources`. Validate, render, commit and open a PR. Do not loosen permissions to work around an organisation policy.

## Canonical resource schema

Each filename matches its stable `id`. Required fields: `id`, `title`, `url`, `summary`, `capabilities` (array of canonical IDs), `status` (`candidate`, `curated`, `retired`), `added` (ISO date), `reviewed_by`, `reviewed_on`, `retirement_reason`. `source_issue` is an optional positive integer. Review fields are blank for candidates. Curated and retired entries need classification and valid review metadata; retirement also requires a reason. Unknown fields and duplicate normalized URLs fail validation.
