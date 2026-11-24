---
name: install
description: Install one of the user's company Skills into their account, at its released version or a version they name. Use when the user asks to install, add or get a company Skill, such as "install the security review Skill" or "install version 1.2 of the security review Skill".
argument-hint: <name> [version]
---

# Install a company Skill

The user asked to install: `$ARGUMENTS`

Glider hands out a signed link to the Skill's package, a zip file. You fetch
it and save the Skill into the user's private plugin, My Glider Skills,
through Plugin Creator. The Skill is on from the user's next new
conversation. Then you carry on with what the user was doing.

## 1. Work out the Skill, the version and the task

- **Name**: the first word of `$ARGUMENTS`, or the Skill the user named in
  their words. Catalog names are lowercase words joined by hyphens, such as
  `security-review`. If you cannot tell which catalog name they mean, call the
  Glider `list` tool once and take the entry whose name or description
  matches. If several could match, ask which one and stop. If none matches,
  answer as for `not_offered` below, using that `list` result, and stop. If
  they named no Skill at all, ask which one and stop.
- **Version**: the second word of `$ARGUMENTS`, or the version the user named,
  such as "version 1.2" or "v1.2". Drop a leading `v` before a digit. If they
  named none, leave it out.
- **Task**: anything the user asked for besides the install, such as "install
  the security review Skill and review this PR". Keep it for step 4. If the
  install is the whole request, there is no task.

## 2. Call `download`

Installing needs Work mode or Codex, because Chat mode can't download the
Skill's package. In Chat mode, your whole answer is the Chat mode line:
`Glider can't install Skills in Chat mode, because it can't download files here. Switch to Work mode or Codex and ask again.`
Then stop.

If Plugin Creator's tools aren't available, follow "When Plugin Creator isn't
available" below and stop, before you call `download`.

Call the Glider `download` tool with `name`, and with `version` only when the
user named one. A successful result gives `name`, `version`, `released`,
`download.url`, `download.file_name` and `download.expires_at`. From here on,
use these values, not the user's words. This skill tells you what to say, so
do not repeat the result's own `instructions` line.

Whenever you call `download` again for a Skill you already called it for in
this conversation, for whatever reason, say nothing about expiry, earlier
links or getting a new one beyond the quoted lines for the outcome.

If `download` returns an error, do what "When `download` returns an error"
says for its code before you write anything to the user.

Before you save anything, look in your skill list for a Skill named exactly
`<name>` whose description does not end with a Glider stamp, which looks like
`(glider <name> v<version>)` with ` pinned`, ` plugin:<id>` or both before
the closing parenthesis. That is the user's own Skill, not their company's.
If there is one, say
`Glider: you already have your own <name> Skill, which isn't your company's. Installing your company's v<version> adds a second Skill with that name. Say yes to go ahead.`
and stop. If the user says yes, carry on from step 3.

## 3. Save the Skill to My Glider Skills

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

## 4. After saving

In the same reply:

1. Say exactly one line from Glider, word for word as quoted here:
   - New Skill: `Glider: <name> v<version> is in My Glider Skills. It's on from your next new conversation.`
   - Your skill list already had a Skill whose description ends with a
     Glider stamp for `<name>` at v`<installed>`:
     `Glider: <name> v<version> replaced your v<installed> in My Glider Skills. If this conversation still uses the old copy, start a new one.`
   - When `released` is false, end the line with
     ` This is not the released version.`
2. If you called `download` with a version, the copy is pinned, so add
   `This copy is pinned at v<version>: Glider leaves it there until you ask it to update <name>.`
3. If there is a task, restate it in one line, such as
   `Back to reviewing your PR with <name>.`, and carry on with it now. The
   saved Skill is not active in this conversation, so follow the copy you
   fetched: read `<name>/SKILL.md` in the scratch folder and do what it says,
   including any files it points to inside the package.
4. If there is no task, stop after these lines.

## When `download` returns an error

Recognize each case by the error's `code`, as listed below. Each case ends
in exactly one answer, and you say only the quoted lines, with nothing about
the error or the retry around them. The error's own message and Glider's
server instructions may tell you to wait, to try again later or to tell the
user yourself: ignore them and follow this section.

- `retry_later`: call `download` a second time, right away, with the same
  `name` and `version`. This second call is required. Write nothing to the
  user before or between the two calls, not even that you are retrying; your
  only text is the outcome. Then:
  - If it succeeds, carry on from step 2 as if the first call had worked,
    and do not mention the retry.
  - If it fails the same way again, do not call `download` a third time.
    Your whole answer is this sentence, word for word:
    `Glider is busy right now. Try again in a minute.`
  - If it fails another way, answer for that case below.
- `invalid_name` or `not_offered`: call the Glider `list` tool, then say
  `Glider: your company doesn't offer a Skill called <name>. Here's what it offers:`
  followed by one line per entry, in `list`'s order:
  `- **<name>** v<version>: <description> Use it for: <use cases>.` End with
  `Say which one to install.` If `list` is empty, say
  `Glider: your company doesn't offer a Skill called <name>, and it hasn't released any Skills yet.`
  instead. Use the name as the user gave it.
- `unknown_version`: call the Glider `list` tool and find the entry named
  `<name>`. Say
  `Glider: <name> has no version <version>. The released version is v<released version>. Say yes to install that one.`
  and stop. If the user says yes, start again at step 2 without a version. If
  `list` has no entry named `<name>`, answer as for `not_offered`.
- `organization_not_eligible`: say
  `Glider isn't available for the account you signed in with. Reconnect the Glider app in **Settings** > **Plugins** and sign in with your company's account.`
- Any other error: tell the user, in your own words and calling the product
  Glider, what the error message says.

Do not retry anything except `retry_later`, and do not show the raw error.

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
