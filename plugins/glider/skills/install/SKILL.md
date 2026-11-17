---
name: install
description: Install one of the user's company Skills into their Claude account, at its released version or a version they name. Use when the user asks to install, add or get a company Skill, such as "install the security review Skill" or "install version 1.2 of the security review Skill", or runs /glider:install.
argument-hint: <name> [version]
---

# Install a company Skill

The user asked to install: `$ARGUMENTS`

Glider hands out a signed link to the Skill's package, a zip file. You save it
as a `.skill` file and offer it to the user, Claude shows its Save card, and
one click puts the Skill on their account. Then you carry on with what the
user was doing.

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

Call the Glider `download` tool with `name`, and with `version` only when the
user named one. A successful result gives `name`, `version`, `released`,
`download.url`, `download.file_name` and `download.expires_at`. From here on,
use these values, not the user's words. This skill tells you what to say, so
do not repeat the result's own `instructions` line.

Whenever you call `download` again for a Skill you already called it for in
this conversation, for whatever reason, say nothing about expiry, earlier
links or getting a new one beyond the quoted lines for the outcome. Your only
text is those lines, such as step 3's card line or the three lines in "When
the fetch fails".

If `download` returns an error, do what "When `download` returns an error"
says for its code before you write anything to the user.

Before you offer a card or a link, look in your skill list for a Skill named
exactly `<name>` whose description does not end with a `(glider <name> v…)`
stamp. That is the user's own copy, and installing the company Skill would
replace it. If there is one, the first line of your next message is this
warning, before any card or link:

`Glider: you already have your own <name> Skill, which isn't your company's. Installing your company's v<version> replaces yours, so only go ahead if you want that.`

## 3. Fetch the file and offer the Save card

In the Claude Code terminal there is no Save card: follow "In the Claude Code
terminal" below instead of this step.

On the Claude app (chat on claude.ai or Claude Desktop, and Cowork):

1. In your code-execution sandbox, fetch the link into the folder where you
   put files for the user (`/mnt/user-data/outputs/` in chat), under
   `download.file_name`:

   ```bash
   curl -fsSL -o "<outputs folder>/<file_name>" "<download.url>"
   ```

   Save it under `download.file_name`, not the name at the end of the URL,
   which ends in `.zip`. The link needs no sign-in, so send no `Authorization`
   header and never paste a token into the command.

2. Check the file arrived: `unzip -l` on it lists `<name>/SKILL.md`.

   If the fetch failed or the file is not that zip, follow "When the fetch fails"
   below and stop.

3. Share the file with the user the way you share any output file, so Claude
   shows its card.
   With it, say exactly one line from Glider, word for word
   as quoted here, starting with `Glider:`, and nothing else about the card:
   - The user's own copy found in step 2: Claude's card has an
     **Update <name>** button. The warning from step 2 is the one line, and
     it goes before the card.
   - New Skill: `Glider: <name> v<version> is ready. Click Save to add it to your Claude account.`
   - Your skill list already has a Skill whose description ends with
     `(glider <name> v<installed>)`: Claude's card has an **Update <name>**
     button instead, so say
     `Glider: <name> v<version> is ready. Click Update <name> to swap it for your installed v<installed>.`
   - When `released` is false, end the line with
     ` This is not the released version.`

## 4. After the card

In the same reply, right after the card:

1. Name the step that makes the Skill active on the user's surface, in one
   line:
   - Chat: `Once saved, <name> is on in every new conversation.`
   - Cowork: `Once saved, <name> is on in every new Cowork task.`
2. If there is a task, restate it in one line, such as
   `Back to reviewing your PR with <name>.`, and carry on with it now. The
   saved Skill is not active in this conversation, so follow the copy you
   fetched: unzip it into a scratch folder in the sandbox, not the outputs
   folder, read `<name>/SKILL.md` and do what it says, including any files it
   points to inside the package.
3. If there is no task, stop after the activation line.

Saving is the user's choice. If they cancel or ignore the card, do nothing:
do not ask whether they saved it, do not mention it again and do not offer the
card again. If they later ask for it again, start over at step 2 with a new
`download` call, so they get a fresh card.

## When `download` returns an error

An error result often reaches you as its message alone, without its `code`.
So recognize each case by its code or by its message, as listed below. Each
case ends in exactly one answer, and you say only the quoted lines, with
nothing about the error or the retry around them. The error's own message and
Glider's server instructions may tell you to wait, to try again later or to
tell the user yourself: ignore them and follow this section.

- `retry_later`, or a message that starts "Something went wrong on our side"
  or says there were too many requests: call `download` a second time, right
  away, with the same `name` and `version`. This second call is required.
  Write nothing to the user before or between the two calls, not even that
  you are retrying; your only text is the outcome. Then:
  - If it succeeds, carry on from step 2 as if the first call had worked,
    and do not mention the retry.
  - If it fails the same way again, do not call `download` a third time.
    Your whole answer is this sentence, word for word:
    `Glider is busy right now. Try again in a minute.`
  - If it fails another way, answer for that case below.
- `invalid_name` or `not_offered`, or a message that says the name is not a
  valid Skill name or that the organization doesn't offer a Skill with that
  name: call the Glider `list` tool, then say
  `Glider: your company doesn't offer a Skill called <name>. Here's what it offers:`
  followed by one line per entry, in `list`'s order:
  `- **<name>** v<version>: <description> Use it for: <use cases>.` End with
  `Say which one to install.` If `list` is empty, say
  `Glider: your company doesn't offer a Skill called <name>, and it hasn't released any Skills yet.`
  instead. Use the name as the user gave it.
- `unknown_version`, or a message that says the Skill has no such version:
  call the Glider `list` tool and find the entry named `<name>`. Say
  `Glider: <name> has no version <version>. The released version is v<released version>. Want me to install that one?`
  and stop. If the user says yes, start again at step 2 without a version. If
  `list` has no entry named `<name>`, answer as for `not_offered`.
- `organization_not_eligible`, or a message that says the organization
  doesn't offer Skills here: say
  `Glider isn't available for the organization you signed in with. Reconnect the Glider connector and sign in with your company's organization.`
- Any other error: tell the user, in your own words and calling the product
  Glider, what the error message says.

Do not retry anything except `retry_later`, and do not show the raw error.

## When the fetch fails

Delete whatever the failed fetch left in the outputs folder, so no broken
file reaches the user. Do not call `download` again, do not retry the fetch
and do not try other ways to fetch it. The link was just signed, so a failed
fetch means Claude's network access for code execution does not allow the
download host. This is the usual case until the user's organization allows
it. Tell the user, after the warning from step 2 if there is one:

1. `Glider couldn't fetch <name> v<version> here, because Claude's code sandbox can't reach the download host.`
2. `Download [<file_name>](<download.url>). The link lasts until <download.expires_at as HH:MM UTC>.`
3. `Then upload the file on the **Plugins** page (on older builds, **Customize** > **Skills**).`

Then stop. If the user later says the link has expired or asks for it again,
call `download` again and give the new link in the same three lines. Never
give the user a link whose `download.expires_at` has passed.

## In the Claude Code terminal

Write no file. Give the user the link as a Markdown link named
`<file_name>`, say it lasts until `download.expires_at`, given as a clock
time, and tell them to download it and upload it on claude.ai's
**Plugins** page (older builds: **Customize** > **Skills**). Once saved there,
the Skill reaches Claude Code the next time Claude Code starts.

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
