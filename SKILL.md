---
name: linkedin-writer
description: Write LinkedIn posts in Jimit Joshi's distinctive voice and style. Jimit is CEO & Founder of Evolvision Technologies, building TalentLens — an AI-powered interview platform for Indian hiring agencies. Use when the user wants to draft a LinkedIn post, write a LinkedIn update, compose social content for LinkedIn, or convert rough notes/ideas/articles into a LinkedIn post. Accepts any input format: bullet points, rough notes, article summaries, or just a topic/thesis. Produces posts that match Jimit's direct, builder-credible, India-first, problem-first style while avoiding AI-generated writing patterns. Campaign goal: build awareness of TalentLens and onboard pilot agencies (target: 10 founding partners).
---

# LinkedIn Post Writer — Jimit Joshi / TalentLens

Write LinkedIn posts that sound like Jimit Joshi: a builder-founder who ships products, not a commentator who talks about them.

## Content Pillars

Every post falls under one of 5 pillars. See [references/content-pillars.md](references/content-pillars.md) for full details, tone guidance, and example topics.

| # | Pillar | Mix |
|---|--------|-----|
| 1 | **AI Playbooks & Practical How-Tos** | ~30% |
| 2 | **AI Industry Takes & Contrarian POVs** | ~25% |
| 3 | **Career & Future of Work in AI Era** | ~20% |
| 4 | **Personal Stories & Behind-the-Scenes** | ~15% |
| 5 | **Educator/Builder POV on AI Tools** | ~10% |

## Input Handling

Accept any form of rough material:
- **Bullet points / notes**: Extract the core insight, find the contrarian angle.
- **Article / link summary**: Identify the author's unique take, not a summary.
- **Topic / thesis only**: Generate the supporting argument and framework from scratch.
- **Pillar selection only (no topic)**: Switch to **Idea Generation Mode** — generate 5-7 post ideas for the selected pillar, each with a hook sketch, core insight, and framework suggestion. See [references/content-pillars.md](references/content-pillars.md).
- **Mixed**: Combine elements as needed.

## Workflow

1. **Ask format preference**: "Single draft or 2-3 variations?" (unless user already specified)
2. **Ask content pillar**: "Which pillar does this fall under?" — present the 5 pillars as options. Skip if the pillar is obvious from the input, or if the user already specified it. If the user picks a pillar with no topic, switch to Idea Generation Mode instead of drafting.
3. **Identify the core insight**: What is the one contrarian or non-obvious point?
4. **Find the angle**: How does this challenge conventional thinking? What do most people get wrong?
5. **Craft the hook using the 3-Step Formula**: Context Lean-In -> Scroll Stop Interjection -> Contrarian Snapback. See [references/hooks-framework.md](references/hooks-framework.md). The hook must survive LinkedIn's "see more" fold (first 2-3 visible lines).
6. **Name the framework**: Distill the insight into a memorable, titled framework (3-5 items).
7. **Draft using the author's structure**: Hook -> Problem -> Framework -> Action -> Engagement question. Match the tone to the selected content pillar.
8. **Apply anti-slop check**: Scan output against banned phrases and structures from [references/style-guide.md](references/style-guide.md). Rewrite any flagged patterns. Ensure zero em-dashes in the output.
9. **Shareability check**: Ask yourself — "Would someone repost this to their team or colleague?" If not, increase the practical value density. Frameworks, checklists, and systems are inherently shareable. Vague opinions are not.
10. **Image generation (mandatory for every post)**: Every post gets a visual. After the user approves the draft, immediately **run** `tools/generate_visual.py` via the Bash tool — do not ask, do not show the command, just execute it. Choose the right template based on the post's primary content type:

    - **Framework card** — post has a named framework with 3-5 labelled items. Use `--tag 'For Hiring Agencies'` (or the relevant audience label) for problem/pain posts; use `--tag 'Framework'` (default) only for solution-focused posts. Use `--hook` for a red problem statement line below the tag when the post leads with a pain point:
      ```
      python tools/generate_visual.py framework \
        --day N \
        --tag 'For Hiring Agencies' \
        --hook 'One-line problem statement here.' \
        --title 'FRAMEWORK NAME' \
        --items 'Label 1:Description 1' 'Label 2:Description 2' 'Label 3:Description 3'
      ```

    - **Stat card** — post leads with a bold number or pricing claim:
      ```
      python tools/generate_visual.py stat \
        --day N \
        --headline '₹4/min' \
        --subtext 'Supporting line here' \
        --context 'Comparison or context line (optional)'
      ```

    - **Process flow** — post has a numbered step sequence:
      ```
      python tools/generate_visual.py process \
        --day N \
        --title 'PROCESS TITLE' \
        --steps 'Step one' 'Step two' 'Step three' 'Step four'
      ```

    - **Quote card** — personal story, reflective, or founder POV post with no framework. Pull the single strongest line from the post:
      ```
      python tools/generate_visual.py quote \
        --day N \
        --quote 'The key line from the post goes here.'
      ```

    Replace N with the campaign day number. Use single quotes in the command so `$` and special characters survive the shell. All files save to `output/Day-N_YYYY-MM-DD/` alongside the post text file.

## Hook Construction (Critical)

Every hook follows the 3-Step Formula. Read [references/hooks-framework.md](references/hooks-framework.md) for full details.

1. **Context Lean-In**: Topic clarity + lean-in trigger (benefit, pain point, common ground, or stunning fact). Staccato sentences — short, compressed, max clarity per word.
2. **Scroll Stop Interjection**: Single line with a contrasting word ("But", "Yet", "Except"). Freezes the reader.
3. **Contrarian Snapback**: Snap in the OPPOSITE direction of the lean-in. Complete the curiosity loop.

Hook amplifiers: lead with benefit/pain over topic, use known references (cult hopping), compress speed to value (frontload insight), staccato sentence rhythm in opening lines.

The "see more" fold on LinkedIn is the cliff edge. The curiosity loop must be unresolved at that boundary.

## Style Rules (Quick Reference)

Read [references/style-guide.md](references/style-guide.md) for full details. Key points:

- **Paragraphs**: 1-3 sentences max. Generous whitespace.
- **Voice**: Direct, first-person, contrarian, practical. Address reader as "you."
- **Structure**: Hook -> Problem -> Named Framework -> Action -> Engagement question.
- **Frameworks**: Bold title, 3-5 items with bold labels + dash explanations.
- **Emojis**: Strategic only. 2-3 types per post. At start of list items, not inline.
- **Closing CTA**: End with one of three CTA types: engagement question (default), repost prompt (for reach), or question + follow prompt (for follower growth). See style guide for details.
- **No hashtags**: User handles these separately.

## Character Limit (Hard Rule)

LinkedIn posts have a **3,000 character hard limit** (including spaces, line breaks, and emojis). Emojis count as 2+ characters each.

After drafting, **always count characters** of the plain-text version (no markdown, as it would appear on LinkedIn). If the post exceeds 3,000 characters, cut it down before presenting to the user. Prioritize cutting:
1. Redundant explanation lines (keep the insight, drop the elaboration)
2. Framework item descriptions (shorten, don't remove items)
3. Context/history paragraphs (compress, don't eliminate)

Never cut: the hook, the framework titles, or the CTA.

**Optimal range**: 1,800-2,800 characters. Posts in this range get the highest engagement. Only approach 3,000 when the content density justifies it.

**When presenting the draft**, show the character count so the user can see headroom: e.g., "2,847 / 3,000 characters."

## Anti-Slop (Critical)

The output MUST NOT read like AI-generated content. After drafting, actively scan for and remove:

- Banned phrases: "Here's the thing:", "Let that sink in.", "In today's [X]", "Navigate", "Lean into", "Game-changer", "Deep dive", "Leverage", all AI intensifiers (deeply, truly, fundamentally, inherently, seamlessly)
- Banned punctuation: Em-dashes (—) are never allowed. Use commas, periods, colons, or parentheses instead. No exceptions.
- Banned structures: Binary contrast formula ("Not X. Because Y." mid-post), performative simplicity ("[Noun]. That's it."), false reassurance ("And that's okay.")
- Rhythm violations: 3+ same-length sentences in a row, every paragraph ending punchily, repetitive three-item lists
- Generic AI voice: Any sentence that could appear in any LinkedIn post by anyone. Every line must sound like THIS specific author.

See the full anti-slop rules in [references/style-guide.md](references/style-guide.md).

## Tone Calibration

Read [references/sample-posts.md](references/sample-posts.md) for 5 representative posts showing the author's range:
- Contrarian opener + named framework
- Data-backed argument + checklist
- Personal story + practical advice
- Problem-framework-action (tactical)
- Philosophical / reflective

Match the tone to the input material. Not every post needs a framework; some are reflective. Not every post needs data; some are personal.

## Output Format

1. **Draft**: Present the post in the conversation using markdown formatting for readability (bold, etc.). No meta-commentary like "Here's your post:" — just the post itself.
2. **Confirm**: After presenting the draft, ask the user to confirm or request changes. Iterate until the user approves.
3. **Export**: Once approved, save a LinkedIn-ready `.txt` file to `output/Day-{N}_{YYYY-MM-DD}/`. N is the campaign day number — infer it from context (e.g. "draft Post 1" → Day 1) or ask if unclear. **Never overwrite existing files.** Filename: `linkedin-post-YYYY-MM-DD-HHMMSS.txt`. This file must be plain text with zero markdown: no `**bold**`, no `*italics*`, no `#` headings. Only line breaks, emojis, and plain text. This is what the user will copy-paste directly into LinkedIn.

   After exporting, remind the user to run `python tools/track.py` to see campaign status, and `python tools/track.py post Day-{N}` after they've posted it.
