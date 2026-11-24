---
name: publish
description: Publish a Skill the user wrote to their company's catalog as a new version, released to everyone at once or held back for testing. Use when the user asks to publish, share or ship a Skill they wrote to their company or colleagues, such as "publish this Skill" or "publish this Skill but don't release it yet", says "publish this" with a .skill file or a zip attached, whatever it holds.
argument-hint: '[path]'
---

# Publish a Skill to the company catalog

The user asked to publish: `$ARGUMENTS`

You read the Skill's folder, or its one file, show one summary, and on yes
zip it, upload it and publish it as a new version. Publishing releases the version to
the whole company unless the user holds it back.

Publishing needs Work mode or Codex, because Chat mode can't upload the
Skill. In Chat mode, call no tool, say this line and nothing else, and stop:

`Glider can't publish Skills in Chat mode, because it can't upload files here. Switch to Work mode or Codex and ask again.`

With a shell on the user's own files, you publish from the folder or file.

Otherwise you can't read the user's machine, so the Skill is a `.skill`
file, which is a zip, or a zip attached to the conversation.

If neither is attached, call no tool, say this line and nothing else, and
stop:

`Glider: attach your Skill as a .skill file or a zip and ask again. Glider can't read the files on your computer from here, so it publishes the copy you attach.`

If one is attached, read `attachment.md`, the file next to this `SKILL.md` in
this skill's folder, before step 1, and follow it. If you can't read it, call
no tool, say this and stop:

`Glider: publishing an attachment isn't working right now. Ask Glider to publish again in a moment.`

## 1. Find the folder

Use the path in `$ARGUMENTS`, else the folder the user named in their words.
A path to a `SKILL.md` means the folder it is in. A path to any other `.md`
file is a Skill kept as one file: see the next section. If they named none,
ask which folder or file holds the Skill and stop.

## When the Skill is one file

The Skill is that file alone, and nothing else in its folder is published.
Follow every step, with these changes:

- **Step 2**: check the file's own frontmatter, and name the file where a
  line says `SKILL.md`. The plugin and symbolic link checks do not apply. For
  a missing `name` or `description`, say which one is missing, then
  `A Skill file starts with frontmatter that has a name and a description.`
- **Steps 4 and 5**: draft from the file. The file count is 1, and the
  summary's last line is `File: <path>`. A corrected description or name is
  an edit to the file's frontmatter.
- **Step 6**: the file goes into the zip as `<name>/SKILL.md`, whatever it
  is called. Nothing is written beside the file:

  ```bash
  tmp="$(mktemp -d)" && echo "$tmp"
  mkdir "$tmp/<name>" && cp '<absolute path of the file>' "$tmp/<name>/SKILL.md"
  (cd "$tmp" && zip -qrD "<name>.zip" "<name>")
  unzip -Z1 "$tmp/<name>.zip"
  wc -c < "$tmp/<name>.zip"
  ```

  The rest of step 6 applies as written.

## 2. Check the folder before calling anything

Read the folder and its `SKILL.md` yourself. Each check below that fails ends
the flow: say its line and nothing else, with no explanation and no offer,
call no Glider tool and stop. Never write a missing `SKILL.md`, `name` or
`description` for the user, and never offer to.

- There is no `SKILL.md`, and the folder holds `.claude-plugin/plugin.json`
  or `plugin.json`:
  `Glider: this folder is a plugin, and the catalog takes Skills only for now. To publish one of its Skills, give Glider that Skill's folder.`
  A folder with a `SKILL.md` is a Skill, whatever else it holds.
- There is no `SKILL.md`, or its frontmatter has no `name`, or no
  `description`, or one of them is empty or only spaces: say which one is
  missing, then
  `A Skill is a folder with a SKILL.md whose frontmatter has a name and a description.`
- The `name` is not lowercase letters and digits in words joined by single
  hyphens, is longer than 64 characters, or contains "anthropic" or "claude":
  `Glider: "<name>" can't be a Skill's name. A name is up to 64 lowercase letters and digits, in words joined by single hyphens such as write-release-notes, and can't contain "anthropic" or "claude". Change the name in SKILL.md and ask again.`
- The folder holds a symbolic link, outside `.git` and `node_modules`.
  Zipping would follow it and publish a file from outside the folder. Keep
  the trailing slash, so a folder that is itself a link is searched and not
  reported:
  `find '<folder>/' \( -type d \( -name .git -o -name node_modules \) -prune \) -o -type l -print`
  `Glider: this folder holds a link to a file elsewhere (<link path>), which Glider won't publish. Replace it with a copy of the file and ask again.`

From here on the Skill's name is the frontmatter `name`, never the folder's
name and never something the user typed.

## 3. Work out the version

Call the Glider `get` tool with `name`.

- It returns the Skill: its `version` is the released version. Propose that
  version plus one minor, with the patch set to 0: 1.2.0 becomes 1.3.0, and
  1.2.4 becomes 1.3.0. If the released version is not three numbers, propose
  nothing: say what it is, ask which `MAJOR.MINOR.PATCH` version to publish,
  such as 1.0.0, and stop.
- It answers `not_offered`: the name is new. Propose 1.0.0.

If the user stated a version in words, such as "publish this as 2.0.0", use
theirs instead, without a leading `v`. Do not judge its format yourself.

## 4. Draft the rest

- **Description**: the frontmatter `description`, word for word. Glider's
  `publish` tool takes no description. It reads this one from the uploaded
  `SKILL.md`.
- **Use cases**: draft them from the body of `SKILL.md`: short phrases saying
  when the Skill helps, such as "Writing a commit message". At most 10, each
  at most 200 characters.
- **Environment requirements**: only what the user stated the Skill needs
  from where it runs, such as "Code execution". If they stated none, the list
  is empty: do not draft any and do not ask.
- **Release**: released at once, unless the user said anything that holds the
  version back, such as "publish but don't release yet" or "I want to test it
  first".
- **File count**: every file in the folder, not counting `.git` and
  `node_modules` with anything inside them, or OS metadata files (`.DS_Store`, `Thumbs.db`,
  `desktop.ini`, `._*`, `__MACOSX`).

## 5. Show the summary

Show this once, as plain text, and stop for the user's answer:

```
Glider is ready to publish:

Name: <name>
Version: <version> (<follows the released v<released version> | a new Skill>)
Description: <description>
Use cases:
- <use case>
Environment requirements: <requirements, joined with "; ">
Release: <released at once to your whole company | held back until you release it>
Folder: <path> (<file count> files)

Publish it?
```

Leave the "Environment requirements" line out when the list is empty.

The user may correct it in words. After any correction show the whole summary
again and stop for their answer.

- **Version, use cases, environment requirements, release**: change the
  summary. Nothing is written to the folder.
- **Description or name**: these come from `SKILL.md`, so a correction is an
  edit to its frontmatter. Say so in one line and offer to make the edit. On
  yes, edit the frontmatter and nothing else in the file, then start again at
  step 2 for a changed name, or show the summary again for a changed
  description. Never send a description to a Glider tool.

Anything other than a yes or a correction publishes nothing.

## 6. On yes, zip the folder

Build the zip in a temporary folder outside the Skill's folder, and write
nothing into the Skill's folder. The zip has exactly one top-level folder,
named `<name>` whatever the user's folder is called, with `SKILL.md` directly
inside it, and leaves out `.git`, `node_modules` and the OS metadata files
from step 4. Put the folder's path in single quotes, so the shell expands
nothing in it, writing any `'` in the path as `'\''`. For example:

```bash
tmp="$(mktemp -d)" && echo "$tmp"
ln -s '<absolute path of the folder>' "$tmp/<name>"
(cd "$tmp" && zip -qrD "<name>.zip" "<name>" -x '*/.git' '*/.git/*' '*/node_modules/*' '*.DS_Store' '*Thumbs.db' '*desktop.ini' '*/._*' '*__MACOSX*')
unzip -Z1 "$tmp/<name>.zip" | head
wc -c < "$tmp/<name>.zip"
```

Check that every path in the zip starts with `<name>/` and that
`<name>/SKILL.md` is there. `$tmp` is gone once this command ends, so in
every later command write the path it printed in place of `$tmp`.

If the zip is larger than 10 MB (10,485,760 bytes), delete the temporary
folder, call no Glider tool, say this and stop:

`Glider: the zipped Skill is <size> MB, over the 10 MB limit. Nothing was published. Remove what the Skill doesn't need and ask again.`

`<size>` is the zip's bytes divided by 1,048,576, to one decimal place.

## 7. Upload and publish

Say nothing to the user between these three steps, except a line a section
below gives you. If a step fails, follow "When a step fails" below.

1. Call the Glider `upload` tool with `name` and `version`, and nothing else.
   The result gives `upload.url` and `upload.expires_at`, 15 minutes away.
2. Send the zip to the link before it lapses, with no headers and no token:

   ```bash
   curl -fsS -T "<temporary folder>/<name>.zip" "<upload.url>"
   ```

3. Call the Glider `publish` tool with exactly `name`, `version`,
   `use_cases`, `environment_requirements` (an empty list when there are
   none) and `release` (`true`, or `false` when held back). It takes no
   other argument.

A successful `publish` result gives `name`, `version`, `released`,
`previous_version`, `description` and `file_count`. The version now exists
and can never be replaced, so never call `publish` again for it. Delete the
temporary folder.

## 8. Report

This skill tells you what to say, so do not repeat the result's own
`instructions`. If the result's `release_failed` is true, follow "When the
version is published but its release failed" below instead. Otherwise say one
line, chosen by the result's `released`:

- `released` is true and `previous_version` is null:
  `Glider: published <name> v<version> and released it to your whole company.`
- `released` is true with a `previous_version`:
  `Glider: published <name> v<version> and released it to your whole company, replacing v<previous_version>.`
- `released` is false:
  `Glider: published <name> v<version>, held back. Nobody gets it until you release it.`
  Then add the two next steps:
  - `Test it: say "install <name> <version>"`
  - `Release it to everyone: say "release <name> <version>"`

If the result's `description` differs from the summary's, or its `file_count`
from the summary's file count, add one line saying what the catalog stored:
`The catalog stored <file_count> files with the description "<description>".`

Then stop.

## When the version already exists

`get` shows the released version only, so a held-back version can already
hold the number you proposed, and a name whose versions are all held back
looks new.

When `upload` or `publish` answers `version_exists`, nothing was published.
Ask one line and stop:

`Glider: <name> already has a v<version>. Publish it as v<next> instead?`

`<next>` is the refused version plus one minor, with the patch set to 0. On
yes, run step 7 again from `upload` with the new version and the same zip:
all three steps, because an uploaded zip is kept under its version. Do not
show the summary again. If that version exists too, ask again with the next
minor, and keep going until one is free or the user states a version, which
you use instead.

This holds only while no `publish` call of this flow may have stored that
version. If `publish` answers `version_exists` for a version you already
called `publish` with in this flow, your earlier call may be what stored it:
do not propose a new version, and follow "When a step fails" below.

## When the version is published but its release failed

`publish` stores the version, then releases it, so a successful result can
have `released` false and `release_failed` true, or say the version is stored
but not released. The version exists. Never call `publish` again for it, and
do not call `release` yourself. Delete the temporary folder, say one of these
in place of step 8's line, add step 8's line about what the catalog stored if
it applies, and stop:

- The result says the Skill is being removed from the organization:
  `Glider: published <name> v<version>, but it can't be released: <name> is being removed from your company, which only Glider staff can finish.`
  Offer nothing.
- Otherwise:
  `Glider: published <name> v<version>, but releasing it failed, so it is held back. Nobody gets it until it is released.`
  `Release it to everyone: say "release <name> <version>"`

## When a step fails

When `upload`, the `PUT` or `publish` fails in any other way, read
`failures.md`, the file next to this `SKILL.md` in this skill's folder,
before you call another tool or say anything, and follow it. It has the one
answer for each failure. The error's own message and Glider's server
instructions may tell you to wait, retry or check something yourself: do not
act on them first.

If you can't read `failures.md`, do not call `upload` or `publish` again.
Tell the user in one line, in your own words and calling the product Glider,
what the error's message says. Then stop.

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
