# Publish: when a step fails

Read from `SKILL.md` when `upload`, the `PUT` or `publish` fails. Step
numbers are `SKILL.md`'s.

Recognize each case by the error's `code`. A case gets the same answer
whichever tool returned it. The error's message may tell you to wait, retry
or check something: do only what this file says. Never show the raw error.
Delete the temporary folder whenever you stop, unless you are waiting for the
user's answer.

If the user is sending the zip themselves, under `attachment.md`'s "When the
sandbox can't reach the upload link", that section answers every case below
that would `PUT` again: you call `upload` and hand over the new link. The
limit of two failures for `publish` still holds, as that section says.

## Two failures end the flow

Each of `upload`, the `PUT` and `publish` gets one more attempt per version,
whatever the two errors were. When a step fails a second time, make no
further call for it, not even a fresh `upload` or corrected metadata, and say

`Glider: <the upload | publishing> failed twice, so nothing was published. Ask Glider to publish again in a few minutes.`

Three second failures are answered differently:

- Both failures were a plain `retry_later`: say the busy line under
  `retry_later` below instead.
- The error's answer below makes no further call, or waits for the user
  (`not_owner`, a bad package, a bad version): give that answer.
- `publish` has an unknown outcome, or answers `version_exists` for a version
  you already called `publish` with: the version may exist, so follow "Check
  whether the version was stored" and never propose a new version first.

## The upload

- **The link lapsed**: `upload.expires_at` passed before the `PUT`, or the
  `PUT` is refused with 403. Say
  `Glider: the upload link ran out, so Glider is getting a new one.`
  Call `upload` again with the same `name` and `version`, `PUT` the same zip
  to the new link and carry on to `publish`.
- **The `PUT` fails with time left**: run the same `curl` once more, saying
  nothing.
- **`upload_missing`** from `publish`: say
  `Glider: the upload didn't arrive, so Glider is sending it again.`
  Run step 7 again from `upload` with the same version and zip.

Once a `PUT` has succeeded, `publish` reads the zip without the link, and the
zip is kept for at least a day: a lapsed link needs no new `upload`.

## Refusals

- **`invalid_name`**: say `Glider: "<name>" can't be a Skill's name.`, then
  in your own words what the message says a valid name looks like, then
  `Nothing was published. Change the name in the Skill's frontmatter and ask again.`
- **`not_owner`**. Never name or guess the owner:
  `Glider: <name> belongs to someone else in your company, so you can't publish a version of it. Nothing was published. Change the name in the Skill's frontmatter to publish it as your own Skill, or ask its owner to publish this version.`
- **`invalid_package`** is one of three cases, told apart by the message:
  - **Bad version** (the version is not a valid version): keep the temporary
    folder, ask and wait:
    `Glider: "<version>" isn't a version Glider can publish. A version is three numbers such as 1.2.0, with no leading zeros and no suffix. Nothing was published. Which version should it be?`
    With the answer, run step 7 again from `upload` with that version and the
    same zip, without showing the summary again.
  - **Bad metadata** (too many use cases or environment requirements, or one
    too long; the uploaded zip is kept): shorten each entry over 200
    characters and keep the first 10, then call `publish` alone, once, with
    the corrected lists. Do not `upload` or `PUT` again. On success, report
    as in step 8 and add one line saying what you changed.
  - **Bad package** (the uploaded package can't be published; the uploaded
    zip has been removed): do not retry. Put what was wrong in your own words
    from the message:
    `Glider: the catalog refused the package: <what was wrong>. Nothing was published. Fix the Skill and ask Glider to publish again.`
- **`retry_later`** is one of three cases, told apart by the message:
  - **The Skill is being removed from the organization**: do not retry.
    `Glider: <name> is being removed from your company, so nothing was published. Only Glider staff can finish removing it.`
  - **The version may have been stored**: do not call `publish`. Follow
    "Check whether the version was stored".
  - **Otherwise** nothing was published. If this is the step's first
    failure, call the same tool once more, right away, with the same
    arguments, saying nothing. For `publish` that is `publish` alone, since
    the uploaded zip is kept. If it fails the same way, say only
    `Glider is busy right now and nothing was published. Ask Glider to publish again shortly.`
    If it fails another way, or the step had already failed once, "Two
    failures end the flow" applies.
- **Any other error**: say in one line, in your own words, what the error's
  message says, and that nothing was published.

Each of these ends the flow unless it says to call or ask again.

## Check whether the version was stored

Call the Glider `download` tool with `name` and `version`, before any other
`publish`. It is only a check: do not fetch its link or repeat its
`instructions`. Whatever it finds, the flow ends in one of these.

- **It hands the version out**: the version is published. Never call
  `publish` again for it. Say one of:
  - `released` is true:
    `Glider: published <name> v<version> and released it to your whole company.`
  - `released` is false and the summary held the version back: step 8's
    held-back line and its two next steps.
  - `released` is false and the summary released at once:
    `Glider: published <name> v<version>, but it wasn't released, so it is held back. Nobody gets it until it is released.`
    `Release it to everyone: /glider:release <name> <version>`
- **`unknown_version` or `not_offered`**: the version was not stored and the
  uploaded zip is kept. If `publish` has failed once for this version, call it
  again, once, with the same arguments. If it has failed twice, say the
  failed-twice line above.
- **Anything else**: you can't tell, so never say nothing was published and
  do not call `publish`. For `retry_later`, call `download` once more first.
  Then say
  `Glider couldn't tell whether <name> v<version> was published. Ask again in a moment: if Glider says v<version> already exists, it went through.`
  `If it did, release it to everyone: /glider:release <name> <version>`
