# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Repo Is

A Claude Code **skill** (slash command) for writing LinkedIn posts in the author's (KVS Dileep's) voice. It is a pure-content repo — no build system, no tests, no dependencies. All files are Markdown.

When installed at `~/.claude/skills/linkedin-writer/`, invoking `/linkedin-writer` triggers `SKILL.md` as the skill definition, which in turn references the four files in `references/`.

## File Roles

| File | Role |
|---|---|
| `SKILL.md` | Skill entrypoint. Defines the full workflow, rules, and output format. This is what Claude executes. |
| `references/style-guide.md` | Voice, tone, anti-slop rules, banned phrases, banned structures, CTA formats. |
| `references/hooks-framework.md` | The 3-step hook formula (Context Lean-In → Scroll Stop → Contrarian Snapback) with examples. |
| `references/content-pillars.md` | The 5 content pillars with tone, audience mindset, and example topics per pillar. |
| `references/sample-posts.md` | 5 calibration posts showing the author's range. These are the ground truth for tone. |

## Skill Workflow (High-Level)

1. Ask for format preference (single draft vs. variations) and content pillar.
2. If pillar selected with no topic → **Idea Generation Mode** (5-7 ideas with hook sketch + framework suggestion).
3. Otherwise: identify core insight → find contrarian angle → craft 3-step hook → name a framework → draft full post → anti-slop scan → shareability check → optional image suggestion.
4. Iterate with user until approved.
5. Export approved post as `linkedin-post-YYYY-MM-DD-HHMMSS.txt` (plain text, zero markdown, never overwrite existing files).

## Hard Rules to Preserve When Editing

These are non-negotiable constraints embedded in the skill. Do not relax them:

- **Em-dashes (—) are banned.** Zero exceptions, anywhere in any post.
- **3,000 character hard limit.** Always count characters of the plain-text version before presenting a draft. Optimal range: 1,800–2,800.
- **No hashtags** — the user handles those separately.
- **Export file must be plain text** — no `**bold**`, no `*italics*`, no `#` headings.
- **Never overwrite an existing export file** — always use a timestamped filename.
- **Anti-slop scan is mandatory** — banned phrases and banned structures are listed in `references/style-guide.md`. Every draft must pass before being shown.

## Customization Entry Points

Users who want to adapt this skill to their own voice should edit:

1. `references/sample-posts.md` — Replace with their own best-performing posts (primary tone calibration).
2. `references/style-guide.md` — Adjust banned phrases, signature transitions, vocabulary patterns.
3. `references/content-pillars.md` — Redefine the 5 pillars to match their content strategy.
4. `references/hooks-framework.md` — Add their own hook examples (the formula itself is universal).
