# LinkedIn Writer Skill for Claude Code

A Claude Code skill that writes LinkedIn posts in your distinctive voice and style, not generic AI slop.

## What It Does

- Accepts any input: rough notes, bullet points, article summaries, or just a topic
- Produces posts that follow a proven structure: Hook > Problem > Named Framework > Action > CTA
- Applies anti-slop rules to eliminate AI writing patterns
- Enforces LinkedIn's 3,000 character limit automatically
- Supports 5 content pillars with distinct tone guidance

## Content Pillars

| # | Pillar | Mix |
|---|--------|-----|
| 1 | AI Playbooks & Practical How-Tos | ~30% |
| 2 | AI Industry Takes & Contrarian POVs | ~25% |
| 3 | Career & Future of Work in AI Era | ~20% |
| 4 | Personal Stories & Behind-the-Scenes | ~15% |
| 5 | Educator/Builder POV on AI Tools | ~10% |

## Installation

### Option 1: Clone to your Claude Code skills directory

```bash
git clone https://github.com/kvsdileep/linkedin-writer.git ~/.claude/skills/linkedin-writer
```

### Option 2: Manual setup

1. Create the skill directory: `mkdir -p ~/.claude/skills/linkedin-writer`
2. Copy all files from this repo into that directory
3. Ensure the structure looks like:

```
~/.claude/skills/linkedin-writer/
  SKILL.md
  references/
    content-pillars.md
    hooks-framework.md
    sample-posts.md
    style-guide.md
```

## Usage

In Claude Code, just ask it to write a LinkedIn post:

```
Write a LinkedIn post about [your topic]
```

Or use the slash command:

```
/linkedin-writer [your notes or topic]
```

## Customization

To make this skill match YOUR voice:

1. **`references/sample-posts.md`** - Replace the 5 sample posts with your own best-performing LinkedIn posts. These calibrate the tone.
2. **`references/style-guide.md`** - Adjust banned phrases, vocabulary patterns, and signature transitions to match your writing style.
3. **`references/content-pillars.md`** - Redefine the 5 pillars to match your content strategy.
4. **`references/hooks-framework.md`** - The hook formula works universally, but you can add your own hook examples.

## Key Features

- **3-Step Hook Formula**: Context Lean-In > Scroll Stop Interjection > Contrarian Snapback
- **Named Frameworks**: Every post distills insights into a memorable, titled framework
- **Character Limit Enforcement**: Stays within LinkedIn's 3,000 character limit with optimal range targeting (1,800-2,800)
- **Anti-Slop Engine**: Actively scans for and removes AI writing patterns, banned phrases, and structural tells
- **CTA Rotation**: Engagement questions, repost prompts, and follow prompts

## File Structure

| File | Purpose |
|------|---------|
| `SKILL.md` | Main skill definition (workflow, rules, output format) |
| `references/style-guide.md` | Voice, tone, formatting, and anti-slop rules |
| `references/hooks-framework.md` | The 3-step hook formula with examples |
| `references/sample-posts.md` | 5 calibration posts showing the author's range |
| `references/content-pillars.md` | Content strategy with 5 pillars and tone guidance |

## License

MIT
