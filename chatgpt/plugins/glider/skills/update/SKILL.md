---
name: update
description: Update one of the user's installed company Skills, or all of them, to the released version, or remove the pin from a pinned one. Use when the user asks to update, upgrade, unpin or get the latest version of a company Skill.
argument-hint: '[name]'
---

# Update company Skills

The user asked to update: `$ARGUMENTS`

Glider hands out a signed link to the released version of each Skill. For
every installed company Skill that is behind, you fetch the package and save
it into the user's private plugin, My Glider Skills, through Plugin Creator,
in place of the installed copy. The new version may only be on from the
user's next new conversation.

A pinned Skill is one the user froze at its version: only an update that
names it moves it, and that removes the pin.

## 1. Find the installed company Skills

Read the skill list you already see in this conversation: the name and
description of every Skill on the user's account. A company Skill's description
ends with a version stamp, `(glider <name> v<version>)` or
`(glider <name> v<version> pinned)`, such as `(glider security-review v1.4.0)`.
A stamp may carry more after these, such as ` plugin:<id>`; ignore it. Take
the name and the installed version from the stamp, not from the Skill's
listed name. A stamp with `pinned` after the version marks a pinned Skill.

- **A name was given**: the first word of `$ARGUMENTS`, or the Skill the user
  named in their words, such as "the security review Skill". Pick the stamped
  Skill it means. Catalog names are lowercase words joined by hyphens.
  - If several stamped Skills could match, ask which one and stop.
  - If only a Skill without a stamp has that name, it is the user's own, not
    a company Skill: say Glider leaves it alone and stop. Do not suggest installing
    over it.
  - If nothing has that name, tell the user that company Skill is not
    installed, that they can ask Glider to install it, and stop.
- **No name**: take every stamped Skill and skip the rest without mentioning
  them. If there are no stamped Skills, say in one sentence that the user has
  no company Skills installed yet and that they can ask Glider what their
  company offers, and stop.
- **"Update the rest"** after a reply that ended with a `still to update`
  line: take only the Skills that line named, not every stamped Skill. Treat
  it as no name, but in step 2 say none of the summary lines again, and send
  on to step 3 only the Skills on that line that are still
  `update_available`.

## 2. Learn each Skill's state with one `list` call

Call the Glider `list` tool once, whether or not a name was given, with
`installed` set to one `{ name, version, pinned }` item for every stamp in
your skill list: the name and the version from the stamp, the version without
its leading `v`, and `pinned` true only when the stamp has `pinned` after the version.
This skill tells you what to say, so do not follow or repeat the result's own
`instructions`, including one that says an update check ran recently: the
user asked, so answer. If `list` returns an error, follow "When a Glider tool
returns an error" below and stop.

For each Skill from step 1, find the entry whose `name` is the name in its
stamp. The entry's `version` is the released version, `<released>` below, and
its `state` says where the installed copy stands. Versions are labels, so
never call one newer or older than another.

- **Named in `not_offered`, with no entry**: the company no longer offers the
  Skill. Offer nothing for it.
- **`installed`**: the copy is the released version.
- **`update_available`**: an unpinned copy that is not the released version.
- **`pinned`**: a pinned copy that is not the released version.

### When a name was given

- No longer offered: say
  `Glider: your company no longer offers <name>, so there is nothing to update.`
  and stop.
- `installed`, and the stamp is not pinned: say
  `Glider: <name> is up to date at v<released>.` and stop.
- Anything else, including a pinned copy that is already the released
  version: go on to step 3 for it. Naming a pinned Skill is how the user
  removes its pin.

### When no name was given

Only the `update_available` Skills go on to step 3. Never update or unpin a
pinned Skill here. Say these lines, each only when it has Skills, before
anything from step 4:

- `Glider: already up to date: <name> v<installed>, <name> v<installed>.` for
  the unpinned `installed` Skills.
- One line for each pinned Skill:
  - state `pinned`:
    `Glider: <name> is pinned at v<installed>. Say "update <name>" to move it to the released v<released>.`
  - state `installed`:
    `Glider: <name> is pinned at v<installed>, the released version. Say "update <name>" to remove the pin.`
- `Glider: no longer offered by your company: <name> v<installed>.`

If no Skill is `update_available`, stop after these lines. If every Skill is
unpinned and `installed`, say `Glider: all your company Skills are up to date.`
instead of the first line and stop.

## 3. Call `download` for each Skill that needs updating

Updating needs Work mode or Codex, because Chat mode can't download the
Skill's package. In Chat mode, your whole answer after step 2's lines is the
Chat mode line:
`Glider can't update Skills in Chat mode, because it can't download files here. Switch to Work mode or Codex and ask again.`
Then stop. If Plugin Creator's tools aren't available, follow "When Plugin
Creator isn't available" below and stop, before you call `download`.

Leave out every Skill that Glider already saved at `<released>` in My Glider
Skills earlier in this conversation: your skill list may keep the old stamp
until the next new conversation. Do not call `download` for it again. Say
`Glider: <name> v<released> is already in My Glider Skills. If this conversation still uses the old copy, start a new one.`
The exception is a user who says that save failed or asks for it again.

Then leave out every Skill whose own stamp has no `plugin:<id>`, unless
Glider saved it in My Glider Skills earlier in this conversation: it isn't in
My Glider Skills, so saving there would add a second copy. Say
`Glider: <name> isn't in My Glider Skills, so Glider can't update it here.`

For the Skills that remain, call the Glider `download` tool with `name` only,
never `version`, so it returns the released version, unpinned. A successful
result gives `name`, `version`, `download.url`, `download.file_name` and
`download.expires_at`; from here on, `<version>` is the result's `version`.
Do not repeat the result's own `instructions` line.

Glider allows one user five `download` calls a minute, so make at most five
in one reply, retries included. When `download` answers `retry_later`, call
it once more for that Skill only if that is not a sixth call. If Skills
remain after the fifth call, or the second try answers `retry_later` too,
stop calling `download`, carry on to step 4 with the Skills you have, and
after the last Skill in step 4 say
`Glider: still to update: <name> v<released>, <name> v<released>. Say "update the rest" in a minute.`

If `download` returns any other error for a Skill, follow "When a Glider tool
returns an error" below for that Skill and carry on with the others.

## 4. Save each update to My Glider Skills

For each Skill that needs updating, one at a time, save it with the steps
below. Where they say to stop, stop for that Skill only: say its line and go
on to the next. Send Plugin Creator one Skill at a time, never several in one
request.

This step is the only place Glider writes to the user's account. Use Plugin
Creator for every write and every read of My Glider Skills, and never send
it a version: Plugin Creator sets the plugin's version itself.

1. **Fetch.** In your shell, fetch the link into a scratch folder and unzip
   it into an empty `package` folder there. `unzip` keeps files already in
   the folder, so an earlier save of the same Skill in this conversation
   would otherwise be saved again:

   ```bash
   curl -fsSL -o "<scratch folder>/<file_name>" "<download.url>"
   rm -rf "<scratch folder>/package" "<scratch folder>/saved"
   unzip -q "<scratch folder>/<file_name>" -d "<scratch folder>/package"
   ```

   The link needs no sign-in, so send no `Authorization` header and never
   paste a token into the command. The package holds one folder, `<name>/`,
   with `<name>/SKILL.md` in it. If the fetch failed or the package is not
   that, follow "When the fetch fails" below and stop.

2. **Find My Glider Skills.** ChatGPT can't list a user's private plugins, so
   Glider keeps My Glider Skills' plugin ID in each Skill's stamp. Look in
   your skill list for a description ending with a stamp that holds
   `plugin:<id>`, and ask Plugin Creator for the private plugin with that
   ID. If there is no such stamp, or Plugin Creator has no plugin with that
   ID (a workspace admin can delete it), ask Plugin Creator for the user's
   private plugin named `my-glider-skills`. If they have none by that name,
   ask Plugin Creator to create it, with the display name `My Glider Skills`
   and no Skills. Keep the plugin's ID, whether you created it now, and the
   link to its page if Plugin Creator gives one.

3. **Stamp.** The description in `<scratch folder>/package/<name>/SKILL.md`
   ends with the stamp Glider's service wrote: `(glider <name> v<version>)`
   or `(glider <name> v<version> pinned)`. Add ` plugin:<id>` before its
   closing parenthesis, such as `(glider <name> v<version> plugin:<id>)`.
   Change nothing else in any file.

4. **Save.** Ask Plugin Creator to save `<scratch folder>/package/<name>/`
   into My Glider Skills as `skills/<name>/`, replacing that folder if it is
   already there, with every file exactly as it is in the scratch folder.
   Leave every other Skill in the plugin as it is. If Plugin Creator fails,
   follow "When Plugin Creator fails" below and stop.

5. **Read back.** Ask Plugin Creator for every file in the saved
   `skills/<name>/`, write each one into `<scratch folder>/saved/<name>/` at
   the same path, and compare the two folders:

   ```bash
   diff -r "<scratch folder>/package/<name>" "<scratch folder>/saved/<name>"
   ```

   Any difference, the stamp included, means Plugin Creator saved something
   else: it has turned a URL inside a file into a markdown link before. Then
   follow "When Plugin Creator saved something else" below and stop.

If you created My Glider Skills here, Plugin Creator left it uninstalled. So
when you tell the user the Skill is saved, add, right after Glider's line,
`One more click: open My Glider Skills and click **Install plugin**, so its Skills turn on.`
followed by the link to its page as `[My Glider Skills](<link>)` if Plugin
Creator gave one, or else
`You'll find it under **Plugins** > **Personal** > **Created by you**.`

## 5. After saving

In the same reply, say one line for each Skill Glider saved, word for word,
including the `Glider:` prefix:

- The installed copy was not pinned:
  `Glider: <name> v<version> replaced your v<installed> in My Glider Skills. If this conversation still uses the old copy, start a new one.`
- It was pinned at another version:
  `Glider: <name> v<version> replaced your pinned v<installed> in My Glider Skills, which removes the pin. If this conversation still uses the old copy, start a new one.`
- It was pinned at this version:
  `Glider: the pin is removed from <name> v<version> in My Glider Skills. If this conversation still uses the old copy, start a new one.`

Then stop.

## When a Glider tool returns an error

- `retry_later` from `download`: step 3 says when to retry and what to do
  after.
- `retry_later` from `list`: call it once more with the same arguments. If
  it fails again, tell the user Glider is busy and to try again shortly.
- Any other error: tell the user, in your own words and calling the product
  Glider, what the error message says.

## When Plugin Creator isn't available

Glider saves Skills only through Plugin Creator. Without its tools, nothing is
saved:

- If ChatGPT offers its own card to install Plugin Creator, that card is the
  step. Say only
  `Glider saves Skills through Plugin Creator. Install it on the card, then click **Connect** on Plugin Creator in **Settings** > **Plugins**, so its tools load. Then ask Glider again.`
  and stop.
- Otherwise your whole answer is the connect hint:
  `Glider saves Skills through Plugin Creator, which isn't available here. Connect Plugin Creator in **Settings** > **Plugins**, or ask your admin to add it.`

## When the fetch fails

Delete whatever the failed fetch left in the scratch folder. Do not call
`download` again, do not retry the fetch and do not try other ways to fetch
it. Say:

- In Codex, where the sandbox may not reach the download host:
  `Glider couldn't fetch <name> v<version>, because Codex can't reach the download host. Allow network access when Codex asks, or ask your admin to allow the download host, then ask Glider again.`
- In Chat mode: the Chat mode line above.
- Otherwise:
  `Glider couldn't fetch <name> v<version>. Ask Glider again.`

## When Plugin Creator fails

If Plugin Creator rejected the package as invalid, save once more: change
only how the files are laid out, keep every file exactly as it is in the
scratch folder, and if that save works, go on with the read-back. Otherwise,
and after a second failure, do not retry. Say what happened in one line, and
nothing about how to fix Plugin Creator:

- "Plugin release changed": My Glider Skills changed while Glider was saving,
  for example from another conversation. Say
  `Glider couldn't save <name>, because My Glider Skills changed at the same time. Ask Glider again.`
- Any other failure: tell the user, in your own words and calling the product
  Glider, what Plugin Creator said, and that they can ask Glider to try
  again.

## When Plugin Creator saved something else

Say
`Glider: Plugin Creator saved <name> differently from your company's v<version>, so it may not work as your company intended. Ask Glider again, and tell your admin if it happens again.`
Do not retry and do not change the saved copy yourself.

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
