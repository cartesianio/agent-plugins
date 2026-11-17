---
name: search
description: Find the Skills in the user's company catalog that fit one task or need the user names. Use when the user asks whether their company has a Skill for something, such as "is there a Skill for writing a security review?" or "do we have anything for SOC 2 evidence?", or runs /glider:search with a phrase. When the user wants the whole company catalog with no particular need, use list instead.
argument-hint: <phrase>
---

# Find company Skills for a need

The user is looking for: `$ARGUMENTS`

## Work out the need

If the line above is empty, take the need from the user's message. If there is
still no need, ask in one sentence what they want a Skill for, and stop.

## Find the matches

Call the Glider `list` tool once, with no arguments. Keep only the entries that
fit the need, judging each from its `name`, `description` and `use_cases`. An
entry fits when it would help with the user's task, even if it words the task
differently, or helps with only part of it. Leave out entries that only share a
word with the need. Each entry either fits or is left out: never present one as
the closest or a partial match.

Never tell the user how the matches were found: do not mention the `list`
tool, the whole catalog having been read, keywords, or descriptions being
compared.

## When some entries fit

Open with one line saying these are the company's Skills that fit the user's
need, naming the need in a few words. Then give each fitting entry, in the
order they came back, in this shape:

```
**<name>** (v<version>)
<one-line description>
For: <what it is for>
```

- **name** and **version** come from the entry as they are.
- **Description**: the entry's `description` in one sentence. Shorten it if
  it is longer, without adding anything it does not say.
- **For**: the entry's `use_cases` joined into one short line. If there are
  none, leave the line out.

Answer as text only. Do not say whether the user has a Skill installed or
whether it is out of date. Close by saying they can ask Glider to install any
of them by name.

## When nothing fits

Say in one sentence that their company has no Skill for that need, and offer
to show every Skill their company offers. Do not suggest Skills from anywhere else, and
do not list the other entries unless the user says yes.

## When the catalog is empty

Say in one sentence that the user's company has not released any Skills yet.
This is not an error, so do not apologize or suggest a fix, and do
not suggest Skills from anywhere else.

## When the tool returns an error

- `retry_later`: call `list` once more. If it fails again, tell the user
  Glider is busy and to try again shortly.
- Any other error: tell the user, in your own words and calling the product
  Glider, what the error message says.

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
