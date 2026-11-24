---
name: status
description: Show which of their company's Skills the user has installed, at which versions, and whether each is current, has an update available, is pinned or is no longer offered. Use when the user asks which company Skills they have, what version of a Skill they are on, whether their company Skills are up to date.
---

# Installed company Skills

The versions and pins come from the skill list you already see in this
conversation: the name and description of every Skill installed on the user's
account. One call to the Glider `list` tool adds each Skill's state. This skill
only reports: call no other tool, read no file, and never offer a Save or
Update card from it.

## 1. Find the company Skills

A company Skill's description ends with a version stamp,
`(glider <name> v<version>)` or `(glider <name> v<version> pinned)`, such as
`(glider security-review v1.4.0)`. A stamp may carry more after these, such
as ` plugin:<id>`; ignore it.

- Take the name and the installed version from the stamp, not from the Skill's
  listed name. A stamp with `pinned` after the version marks a pinned Skill.
- Skip every Skill whose description has no stamp. It is the user's own, not
  one of their company's Skills, so leave it out without mentioning it.

When you found none, call no tool. Answer with one sentence and stop: the user
has none of their company's Skills installed yet, and they can ask Glider what
their company offers.

## 2. Learn each Skill's state with one `list` call

Call the Glider `list` tool once, with `installed` set to one
`{ name, version, pinned }` item for every stamp you found: the name and the
version from the stamp, the version without its leading `v`, and `pinned` true
only when the stamp has `pinned` after the version. Pass every stamp even when the user
asked about one Skill.

This skill tells you what to say, so do not follow or repeat the result's own
`instructions`, including one that says an update check ran recently: the user
asked, so answer. Call `download` for nothing.

Read each installed Skill's state from the result:

- Its name is in `not_offered`: the company no longer offers it.
- Otherwise find the entry whose `name` is the name in its stamp. The entry's
  `version` is the released version, and its `state` is `installed` (the
  installed copy is the released version), `update_available` (an unpinned
  copy that is not the released version) or `pinned` (a pinned copy that is
  not the released version).

Versions are labels compared for equality only: never call one newer or older
than another.

If you cannot get a result, follow "When Glider cannot check" below.

## 3. Answer

List every company Skill you found, one per line, sorted by name. Use the line
for its state, word for word, where `<version>` is the installed version from the stamp and
`<released>` is the entry's `version`:

- `installed`, stamp not pinned: `- <name> v<version>: current`
- `installed`, stamp pinned: `- <name> v<version>, pinned: current`
- `update_available`:
  `- <name> v<version>: update available, v<released> is the released version. Say "update <name>" to get it.`
- `pinned`:
  `- <name> v<version>, pinned: v<released> is the released version. Say "update <name>" to move to it.`
- In `not_offered`, adding `, pinned` after the version when the stamp is
  pinned:
  `- <name> v<version>: no longer offered by your company. Ask Glider to remove <name> to take it out of My Glider Skills.`

Say nothing else about each Skill, and remove nothing yourself.

When the user asked about one Skill, answer with that Skill's line only, worded
as above. If it has no stamp, say it is not installed as one of their company's Skills; when an
entry in the result has that name, add that their company offers it at
v`<released>` and they can ask Glider to install it.

## When Glider cannot check

The user still gets their versions and pins. This applies when:

- `list` returns `retry_later`: call it once more with the same arguments
  first, and come here only if it fails again.
- `list` returns any other error, or the call itself fails.
- No Glider tool is listed at all.

List every company Skill from the stamps alone, one per line, sorted by name,
or only the Skill the user asked about:

```
- <name> v<version>
- <name> v<version>, pinned
```

Then add this line, word for word:
`Glider could not check for updates just now, so these are the versions you have installed.`

When the user asked about one Skill and it has no stamp, give no version line.
Say it is not installed as one of their company's Skills, and that Glider
could not check just now whether their company offers it.

When no Glider tool is listed at all, do not stop before answering: give the
lines above first, then the step for the user's surface from "When Glider
isn't connected" below.

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
