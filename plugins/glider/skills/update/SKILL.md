---
name: update
description: Update one of the user's installed company Skills, or all of them, to the released version. Use when the user asks to update, upgrade or get the latest version of a company Skill, or runs /glider:update.
argument-hint: '[name]'
---

# Update company Skills

The user asked to update: `$ARGUMENTS`

Glider hands out a signed link to the released version of each Skill. For
every installed company Skill that is behind, you fetch the file and offer it
to the user, Claude shows its update card, and one click swaps the installed
copy for the new one in place. Updates happen only when the user asks; never
check for or offer updates on your own.

## 1. Find the installed company Skills

Read the skill list you already see in this conversation: the name and
description of every Skill on the user's account. A company Skill's description
contains a version stamp `(glider <name> v<version>)`, such as
`(glider security-review v1.4.0)`. Take the name and the installed version from
the stamp, not from the Skill's listed name. If a stamp has anything after the
version, ignore it.

- **A name was given**: the first word of `$ARGUMENTS`, or the Skill the user
  named in their words, such as "the security review Skill". Pick the stamped
  Skill it means. Catalog names are lowercase words joined by hyphens.
  - If several stamped Skills could match, ask which one and stop.
  - If only a Skill without a stamp has that name, it is the user's own, not
    a company Skill: say Glider leaves it alone and stop. Do not suggest installing
    over it.
  - If nothing has that name, tell the user that company Skill is not
    installed, that `/glider:install <name>` installs it, and stop.
- **No name**: take every stamped Skill and skip the rest without mentioning
  them. If there are none, say in one sentence that the user has no company
  Skills installed yet and that `/glider:list` shows what their company
  offers, and stop.

## 2. Check the installed versions with one `list` call

Call the Glider `list` tool once, with no arguments, whether or not a name was
given. Its `entries` give each Skill's `name` and released `version`. This
skill tells you what to say, so do not repeat the result's own `instructions`
line. If `list` returns an error, follow "When a Glider tool returns an error"
below and stop.

For each Skill from step 1, find the entry whose `name` is the name in its
stamp and compare the entry's `version` with the installed version, ignoring a
leading `v`. Versions are labels compared for equality only: never call one
newer or older than another.

- **No entry**: the company no longer offers the Skill. Offer nothing for it.
- **Equal**: the Skill is up to date. Offer nothing for it.
- **Different**: the installed copy is not the released version. Go on to
  step 3 for it.

When a name was given and the Skill needs nothing, answer with one line and
stop:

- No entry: `Glider: your company no longer offers <name>, so there is nothing to update.`
- Equal: `Glider: <name> is up to date at v<version>.`

When no name was given, first list the up-to-date Skills in one line,
`Glider: already up to date: <name> v<version>, <name> v<version>.`, then the
ones with no entry in one line,
`Glider: no longer offered by your company: <name> v<installed>.`, leaving out
either line when it has no Skills. If every Skill is up to date, say
`Glider: all your company Skills are up to date.` instead and stop. If none
needs updating, stop after these lines.

## 3. Call `download` for each Skill that needs updating

Only for the Skills that differ, call the Glider `download` tool with `name`
only, never `version`, so it returns the released version. Each call asks the
company for a download, so never call it for a Skill that is up to date. A
successful result gives `name`, `version`, `download.url`,
`download.file_name` and `download.expires_at`; from here on, `<version>` is
the result's `version`. Do not repeat the result's own `instructions` line.

If `download` returns an error for a Skill, follow "When a Glider tool returns
an error" below for that Skill and carry on with the others.

## 4. Fetch each file and offer the update card

In the Claude Code terminal there is no card: follow "In the Claude
Code terminal" below instead of this step.

On the Claude app (chat on claude.ai or Claude Desktop, and Cowork), for each
Skill that needs updating, one at a time:

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
   below for that Skill and go on to the next.

3. Share the file with the user the way you share any output file, so Claude
   shows its card.
   Because the Skill is already installed, the card's button
   reads `Update <name>`. Put this one line with it, word for word, including
   the `Glider:` prefix:
   `Glider: <name> v<version> is ready. Click Update <name> to swap it for your installed v<installed>.`

One card per Skill: never bundle several Skills into one file.

## 5. After the cards

In the same reply, after the last card, add these two lines and stop:

- `If Claude says it couldn't load the existing skill to update it, click Update on that Skill's card again.`
- On chat: `Once updated, every new conversation uses the new version.` On
  Cowork: `Once updated, every new Cowork task uses the new version.`

Do not ask whether the user updated it, and do not offer a card again unless
they ask.

## When a Glider tool returns an error

- `retry_later`: call the tool once more with the same arguments. If it
  fails again, tell the user Glider is busy and to try updating that Skill
  again shortly.
- Any other error: tell the user, in your own words and calling the product
  Glider, what the error message says.

## When the fetch fails

The sandbox often cannot reach the download host, because Claude's network
access for code execution does not allow it. Do not retry in a loop and do not
try other ways to fetch it. For that Skill, tell the user:

- Glider could not fetch the file here, and the link below lasts until
  `download.expires_at`, given as a clock time.
- The link, as a Markdown link named `<file_name>`.
- To download it, then upload it on the **Plugins** page (older builds:
  **Customize** > **Skills**).

## In the Claude Code terminal

Write no file. For each Skill that needs updating, give the user one line,
`Glider: <name> v<version> is ready to replace your installed v<installed>.`,
then the link as a Markdown link named `<file_name>`. Say the links last until
`download.expires_at`, given as a clock time, and tell the user to
download each file and upload it on claude.ai's **Plugins** page (older
builds: **Customize** > **Skills**). The new version reaches Claude Code the next time Claude Code starts.

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
