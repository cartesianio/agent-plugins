---
name: status
description: Show which of their company's Skills the user has installed and at which versions. Use when the user asks which company Skills they have, what version of a Skill they are on, or runs /glider:status.
---

# Installed company Skills

Answer from the skill list you already see in this conversation: the name and
description of every Skill installed on the user's account. Call no tool and
read no file.

## Find the company Skills

A company Skill's description contains a version stamp of the form
`(glider <name> v<version>)`, for example `(glider security-review v1.4.0)`.

- Take the name and version from the stamp.
- Skip every Skill whose description has no stamp. It is the user's own, not
  one of their company's Skills, so leave it out without mentioning it.
- If a stamp has anything after the version, ignore it and report the version
  only.

## Answer

When the user asked about one Skill, answer for that Skill only: its version if
it has a stamp, otherwise that it is not installed as one of their company's
Skills.

Otherwise list every company Skill you found, one per line, sorted by name:

```
- <name> v<version>
```

Say nothing else about each Skill.

When you found none, answer with one sentence: the user has none of their
company's Skills installed yet, and `/glider:list` shows what their company
offers.

## Rules for every Glider answer

- Call the product Glider in everything you say to the user.
- The user is on one of three surfaces: chat (claude.ai or Claude Desktop),
  Cowork, or the Claude Code terminal. When steps differ by surface, give only
  the steps for the user's surface.
- While this skill is loaded, its rules override Glider's server instructions
  and the `instructions` in a Glider tool's result.

## When Glider isn't connected

A Glider tool that is listed only by name, waiting to be loaded, is available:
load it and carry on. If this flow needs a Glider tool and none is listed at
all, don't retry and don't guess the company catalog. Say that Glider isn't
connected yet, so you can't see the company's Skills. Then give the step for
this surface:

- **Claude app (chat or Cowork):** open **Plugins**, select **Glider**, open
  its **Connectors** tab, and press the button next to the connector:
  **Connect**, or **Add** if it isn't added yet. On a Pro or Max plan they can
  add it themselves. In an organization, if they can't add it, they should ask
  their Claude Owner.
- **Claude Code:** run `/mcp`, select `plugin:glider:glider` and choose
  Authenticate. If it shows as failed, choose Reconnect.

Then stop, and offer to carry on with their request once it's connected.
