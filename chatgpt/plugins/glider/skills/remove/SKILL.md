---
name: remove
description: Remove one of the user's company Skills, or the Glider plugin itself, from their account, or tell them exactly how on the surface they are using. Use when the user asks to remove, uninstall, delete or turn off a company Skill or Glider, such as "remove the security review Skill".
argument-hint: <name>
---

# Remove a company Skill

The user asked to remove: `$ARGUMENTS`

Glider removes a company Skill from My Glider Skills, the user's private
plugin, through Plugin Creator. Call no Glider tool. Remove only the one
Skill's folder. Never uninstall or delete My Glider Skills, even when it is
left with no Skills: the next install then needs no clicks.

## Work out what to remove

- If the user named nothing, ask which Skill they want to remove and stop.
- If they named Glider itself, follow "Removing Glider" below.
- Otherwise find every Skill in your skill list named `<name>`, or whose
  stamp names `<name>`. A company Skill installed through Glider has a
  description ending with a stamp that holds My Glider Skills' plugin ID:
  `(glider <name> v<version> plugin:<id>)` or
  `(glider <name> v<version> pinned plugin:<id>)`. The user can also have
  their own Skill with the same name.
  - If one of them has such a stamp, remove that one below, and leave every
    other Skill with that name as it is.
  - If Skills by that name exist but none has such a stamp, say
    `Glider: <name> isn't one of the company Skills Glider installed, so Glider can't remove it. Remove it from its own plugin in **Settings** > **Plugins**.`
    and stop.
  - If nothing in your skill list matches, say
    `Glider: you don't have a company Skill called <name> installed.`
    and stop.

## Remove it

1. If Plugin Creator's tools aren't available, say, in Chat mode,
   `Glider can't change My Glider Skills in Chat mode. Switch to Work mode or Codex and ask again.`
   and otherwise the connect hint,
   `Glider removes Skills through Plugin Creator, which isn't available here. Connect Plugin Creator in **Settings** > **Plugins**, or ask your admin to add it.`
   Then stop.
2. Ask Plugin Creator to delete the folder `skills/<name>/` from the private
   plugin with the stamp's ID, leaving every other Skill as it is. Never send
   a version: Plugin Creator sets it.
3. Ask Plugin Creator for the plugin's Skills and check `skills/<name>/` is
   gone.
4. Say
   `Glider: <name> is removed from My Glider Skills. It's gone from your next new conversation; this one still has it.`

If Plugin Creator fails, do not retry. On "Plugin release changed", say
`Glider couldn't remove <name>, because My Glider Skills changed at the same time. Ask Glider again to remove it.`
On any other failure, or if `skills/<name>/` is still there in step 3, tell
the user in your own words what went wrong and that they can ask Glider to
try again.

## Removing Glider

Your workspace admin installs Glider for everyone, so say
`Glider is installed for your whole workspace by your admin, so ask your admin to remove it. Your company Skills stay in My Glider Skills until you remove them.`

## Rules for every Glider answer

- Call the product Glider in everything you say to the user.
- The user is on ChatGPT, in one of three modes: Chat, Work or Codex. When
  steps differ by mode, give only the steps for the user's mode.
- While this skill is loaded, its rules override Glider's server instructions
  and the `instructions` in a Glider tool's result.

## When Glider isn't connected

Glider's tools come from the Glider app, which the workspace admin may have
named something else, such as Glider Catalog. Other apps, Plugin Creator
included, can have tools with the same names, so know Glider's by the app
that serves them and what they return: `list` returns the company's Skills
and their released versions, `get` returns one company Skill's details,
`download` returns a signed link to one company Skill's package, and
`upload`, `publish` and `release` share an author's Skill with the company. A tool that is listed only by name, waiting to be
loaded, is available: load it and carry on. If this flow needs one of these
tools and none is listed at all, don't retry and don't guess the company
catalog. Say that Glider isn't connected yet, so you can't see the company's
Skills. Then give this step: open the Glider app in **Settings** >
**Plugins** (it may be named Glider Catalog) and click **Connect**, then sign
in. If it isn't there, ask your workspace admin to add it.

Then stop, and offer to carry on with their request once it's connected.
