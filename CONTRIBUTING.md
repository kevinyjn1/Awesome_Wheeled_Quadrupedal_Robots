# Contributing

Thanks for helping grow the list! Wheeled-legged quadrupeds are still a small community, so every paper, platform, repo, and video counts.

## Scope

**In scope** — anything about robots with **four legs *and* wheels** (wheels at the feet, wheels at the knees, transformable wheel-legs, or a legged chassis with driven wheels): platforms, papers, code, models, datasets, videos, labs, talks.

**Related (own section only)** — wheeled-legged bipeds (Ascento, Diablo, Tita, …), wheel-leg hexapods/rovers (ATHLETE, SherpaTT, …), and hybrid-locomotion theory that is not quadruped-specific. These go under **Related Materials**, not the main sections.

**Out of scope** — purely legged quadrupeds (Spot, ANYmal without wheels, Go2 without the W) and purely wheeled robots. [Awesome_Quadrupedal_Robots](https://github.com/curieuxjy/Awesome_Quadrupedal_Robots) already covers legged quadrupeds beautifully.

## How to add an entry

1. **Fork** the repo and create a branch.
2. **Add your entry** in the matching section, following the existing format:
   - Papers: `- [Exact Title](https://arxiv.org/abs/XXXX.XXXXX)` under the year it was *first published* (arXiv date counts). Prefer arXiv > DOI > publisher page. Append `[Code](url)` / `[Project](url)` / `[Video](url)` links if official ones exist.
   - Platforms: `- [Name](official-page) — Org (Country), year — wheel configuration — one-line note`
   - Repositories: `- [![](https://img.shields.io/badge/OWNER-REPO-black?style=flat-square&logo=github)](https://github.com/OWNER/REPO) <img src="https://img.shields.io/github/stars/OWNER/REPO?style=flat-square&color=yellow">` (replace `-` in OWNER/REPO with `--` inside the badge text).
3. **Sort**: run `python3 assets/ordering.py` to alphabetize bullet lists inside each block (papers within a year, platforms, repos, …).
4. **Check links**: run `python3 assets/check_links.py README.md` and make sure your new URLs return 200.
5. **Open a pull request** with one or two sentences on what you added and why it belongs here.

## Quality bar

- Every link must resolve. No placeholders, no "coming soon".
- One entry per work: if a paper has an arXiv version and a journal version, link one (prefer arXiv) and mention the venue in the PR.
- Keep descriptions short and factual — no marketing copy.
- Entries must be *wheeled-legged*. If a paper only mentions wheels in future work, it does not belong here.

## Reporting problems

Dead link, wrong year, duplicate, misclassified entry? Open an [issue](../../issues) or just send a PR.
