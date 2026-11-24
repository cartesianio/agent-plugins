---
name: pin
description: Pin one of the user's installed company Skills at the version they have, so Glider stops offering updates for it. Use when the user asks to pin, freeze, lock or keep a company Skill at its version, such as "pin the security review Skill".
argument-hint: <name>
---

# Pin a company Skill

The user asked to pin: `$ARGUMENTS`

A pinned Skill stays at its version: Glider mentions a different released
version but never offers it until the user asks to update that Skill by name.
The pin lives in the installed copy's stamp, so pinning means saving the same
version again, stamped `pinned`, into the user's private plugin, My Glider
Skills, through Plugin Creator, in place of the copy they have.

Pinning needs Work mode or Codex, because Chat mode can't download the
Skill's package. Before any `download` call, in Chat mode, your whole answer
is the Chat mode line:
`Glider can't pin Skills in Chat mode, because it can't download files here. Switch to Work mode or Codex and ask again.`
Then stop. If Plugin Creator's tools aren't available, follow "When Plugin
Creator isn't available" below and stop, before you call `download`.

If Glider saved the Skill in My Glider Skills earlier in this conversation,
your skill list may still show its stamp from before that save. Go by that
save instead: it is in My Glider Skills, `<installed>` is the version Glider
saved, and it is pinned only if Glider saved it pinned.

Otherwise, if the Skill is installed and its stamp has no `plugin:<id>`, it
isn't in My Glider Skills, so saving there would add a second copy. Say
`Glider: <name> isn't in My Glider Skills, so Glider can't pin it here.`
and stop, before you call `download`.

## 1. Find the Skill

Read the skill list you already see in this conversation. A company Skill's
description ends with a version stamp, `(glider <name> v<version>)` or
`(glider <name> v<version> pinned)`. A stamp may carry more after these, such
as ` plugin:<id>`; ignore it. Take the name and the installed version,
`<installed>` below, from the stamp, not from the Skill's listed name.

The name is the first word of `$ARGUMENTS`, or the Skill the user named in
their words, such as "the security review Skill". Catalog names are lowercase
words joined by hyphens.

- No Skill named: ask which one and stop.
- Several stamped Skills could match: ask which one and stop.
- Only a Skill without a stamp has that name: it is the user's own, not a
  company Skill. Say Glider can only pin company Skills and stop.
- Its stamp has `pinned` after the version: follow "Already pinned" below.
- No Skill has that name: follow "Not installed" below.
- Otherwise go on to step 2.

Pin one Skill per request. If the user asks to pin all their Skills, ask
which one to start with.

## 2. Call `download` with the installed version

Call the Glider `download` tool with `name` and `version` set to
`<installed>` without its leading `v`. Naming the version is what makes
Glider stamp the copy `pinned`. A successful result gives `name`, `version`,
`download.url`, `download.file_name` and `download.expires_at`. Do not repeat
the result's own `instructions` line.

If `download` returns an error, follow "When a Glider tool returns an error"
below and stop.

## 3. Save the pinned copy to My Glider Skills

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

In the same reply, after saving, say this line, word for word, and stop:
`Glider: <name> v<version> is pinned in My Glider Skills. Glider leaves it there until you ask it to update <name>. If this conversation still uses the old copy, start a new one.`

## Already pinned

Change nothing and do not call `download`. Call the Glider `list` tool once,
with no arguments, and find the entry whose `name` is the name in the stamp.
Versions are labels, so never call one newer or older than another. Answer
with one line and stop:

- The entry's `version` equals `<installed>`, or `list` returned an error:
  `Glider: <name> is already pinned at v<installed>.`
- It differs:
  `Glider: <name> is already pinned at v<installed>. The released version is v<released>, and saying "update <name>" moves you to it.`
- No entry:
  `Glider: <name> is already pinned at v<installed>. Your company no longer offers it.`

## Not installed

Call the Glider `list` tool once, with no arguments, and find the entry the
user means by its name or description.

- No entry matches: say
  `Glider: you don't have a company Skill called <name>, and your company doesn't offer one.`
  and stop.
- Several could match: ask which one and stop.
- One matches: say
  `Glider: <name> isn't installed, so there is nothing to pin yet. Say yes to install the released v<released>, pinned.`
  and stop. If the user says yes, call `download` once with `name` and
  `version` set to `<released>`, then carry on from step 3.
  The Skill is new in My Glider Skills, so after saving, say
  `Glider: <name> v<version> is in My Glider Skills, pinned at that version. It's on from your next new conversation.`
  in place of step 3's line.

## When a Glider tool returns an error

- `retry_later`: call the tool once more with the same arguments. If it
  fails again, tell the user Glider is busy and to try again in a minute.
- `unknown_version`:
  - The Skill is installed: say
    `Glider: your company no longer keeps v<installed> of <name>, so Glider can't pin it. Say "update <name>" to move to the released version.`
  - You came from "Not installed": say
    `Glider: your company just changed <name>, so v<released> is no longer there to install. Ask to pin <name> again to get the version it releases now.`
- `not_offered`:
  - The Skill is installed: say
    `Glider: your company no longer offers <name>, so Glider can't pin it. Your installed copy keeps working.`
  - You came from "Not installed": say
    `Glider: your company no longer offers <name>, so there is nothing to install or pin.`
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
