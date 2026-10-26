# Setup, validation and publishing

## Local setup

Use Python 3.9 or later; CI uses Python 3.12. From the repository root:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python scripts/catalogue.py validate
python scripts/catalogue.py render
python -m unittest discover -v
python -m mkdocs build --strict
python -m mkdocs serve
```

Open the local URL printed by MkDocs. Direct dependencies are version-pinned; transitive versions may vary by Python/platform. Dependabot proposes dependency updates for review. The site uses system fonts and local theme assets.

## GitHub repository settings

1. Enable GitHub Actions and allow the official actions used in `.github/workflows/`.
2. Keep default workflow permissions read-only. The review job explicitly requests contents and PR write access. Enable **Allow GitHub Actions to create and approve pull requests** only if you want automatic draft PR creation; this implementation does not approve PRs.
3. Protect `main` as appropriate: require the `validate` check, review and no force pushes. CODEOWNERS identifies the repository owner; it does not enforce review without a branch rule. A solo owner may need a separate reviewer to enforce mandatory approval without blocking their own work.
4. For publishing, choose Settings → Pages → Source → **GitHub Actions**. Configure the `github-pages` environment and any required reviewer before deployment.

No PAT, model API key or external summarisation service is required. Workflows use the repository-scoped `GITHUB_TOKEN`. If automatic PR creation is disabled by policy, use the manual intake fallback.

## Publish

Publishing is opt-in. After merging reviewed content, run Actions → **Publish documentation** on `main`. It validates the catalogues, runs tests, builds strictly and uploads the static site. The deploy job has only Pages and identity-token write permissions. The expected URL is `https://lajirajg.github.io/enterprise-ai/`; it is live only after a successful deployment.

To publish automatically after future merges, add a `push` trigger restricted to `main` in `pages.yml`. Keep required environment reviews if needed. To roll back, revert the content commit through review and publish again.

## Validation and troubleshooting

- **Invalid URL / duplicate:** correct the issue URL or use the existing resource record. Normalisation removes tracking parameters and fragments; redirects are not resolved.
- **Unknown capability:** choose an ID from the catalogue or leave intake classification blank.
- **Stale generated page:** run the renderer and commit the changed page.
- **PR creation denied:** use the manual fallback or ask the repository administrator to check workflow PR permissions.
- **Pages not configured:** select GitHub Actions as the Pages source, then rerun publishing.
- **Automated PR checks absent:** PRs created by `GITHUB_TOKEN` do not trigger ordinary follow-on workflows. The proposal job validates metadata before opening the PR. A maintainer’s subsequent content commit triggers normal PR CI; alternatively run the validation workflow manually on the candidate branch. Never assume a missing check passed.

## References

- [Material for MkDocs publishing guide](https://squidfunk.github.io/mkdocs-material/publishing-your-site/)
- [GitHub Actions security guidance](https://docs.github.com/en/actions/reference/security/secure-use)
- [GitHub issue-form syntax](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/syntax-for-issue-forms)
