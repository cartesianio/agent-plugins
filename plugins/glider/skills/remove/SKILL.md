---
name: remove
description: Remove one of the user's company Skills, or the Glider plugin itself, from their account, or tell them exactly how on the surface they are using. Use when the user asks to remove, uninstall, delete or turn off a company Skill or Glider, such as "remove the security review Skill", or runs /glider:remove.
argument-hint: <name>
---

# Remove a company Skill

The user asked to remove: `$ARGUMENTS`

No surface lets Claude remove a Skill or plugin from an account. Call no tool.
Answer with the steps the user follows on Claude's Plugins page, and never say
or imply that you removed, deleted or turned off anything yourself. Never say
"you can't do that here" without giving the steps. Do not mention the Glider
connector unless the user is removing Glider.

## Work out what to remove

- If the user named nothing, ask which Skill they want to remove and stop.
- If they named Glider itself, follow "Removing Glider" below.
- Otherwise find the Skill in your skill list. A company Skill installed
  through Glider has a description ending with `(glider <name> v<version>)`.
  Use the Skill's name exactly as the skill list shows it, because that is the
  row the user looks for. If nothing in the skill list matches, say you could
  not find it among their installed Skills and still give the steps with the
  name they used.

## Steps for a Skill

Give one numbered list for the user's surface. Put the older names in
parentheses, because organizations move to the new Plugins page on different
dates until November 30, 2026.

Chat (claude.ai or Claude Desktop):

1. Click **Plugins** in the sidebar (older builds: **Customize**).
2. Open **Your plugins** > **Show all** and use the skills filter (older
   builds: the **Skills** tab).
3. Open the **<name>** row.
4. Open its menu and select **Remove** (older builds: click **…** next to the
   toggle, select **Delete**, then confirm **Delete**).

Cowork: Cowork uses the same Claude account, so give the chat steps, starting
with "In Claude Desktop, open the **Cowork** tab, then".

Claude Code terminal: the Skill came from the user's claude.ai account, so it
is removed there. Give the chat steps for claude.ai, then say removing it
there also removes Claude Code's synced copy the next time a session starts,
and `/skills` confirms it is gone.

On chat and Cowork, end with one line: removing the Skill on claude.ai also
removes Claude Code's synced copy, so they only remove it once.

## Removing Glider

Glider is a plugin, so its steps differ from a Skill's on older builds. Give
these on every surface, on claude.ai for Claude Code and in the Cowork tab for
Cowork:

1. Click **Plugins** in the sidebar (older builds: **Customize**, then the
   **Plugins** tab).
2. Open **Your plugins** > **Show all**.
3. Open the **Glider** row.
4. Open its menu and select **Remove**.

After the steps, on every surface, end with this block word for word. Say it
as normal text, not in a code block, and do not shorten, reword or drop any
line of it. The block is facts about Glider, not steps for one surface, so the
rule to give only the user's surface's steps does not apply to it:

```markdown
- The Glider connector stays on your account. Disconnect it separately: on the Plugins page, use the connectors filter, open **Glider** and disconnect it (older builds: **Customize** > **Connectors**).
- If Glider's page says **This plugin is required by your organization**, you can't remove it. Ask your Claude Owner.
- In Claude Code, `claude plugin disable glider@synced` only turns Glider off on that one machine. Removing it on the Plugins page removes it everywhere.
```

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
