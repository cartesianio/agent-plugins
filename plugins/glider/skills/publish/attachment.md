# Publish: when the Skill is an attachment

Read from `SKILL.md` when the Skill is a `.skill` file or a zip attached to
the conversation. Step numbers are `SKILL.md`'s.

## Unzip the attachment with the check

Unzipping must write only inside a new folder, and only so much. In your
sandbox, never on the user's machine, run `unpack_zip.py`, the file next to
this one in this skill's folder. It checks
the zip's entry list, then unzips into a folder it creates, which must not
exist yet, and removes that folder if it has to stop. Put each path in single
quotes, writing any `'` in it as `'\''`:

```bash
python3 '<path of unpack_zip.py>' '<path of the attachment>' '<path of a new folder>'
```

It prints `ok`, or which check failed. If it says the folder exists, run it
again with another path. If it says it cannot write, treat it as a script you
can't run.

Only this script unzips the attachment, because it stops at the size limit
as it writes. Never unzip it any other way. If you can't find the script or
can't run it, unzip nothing, call no Glider tool, say this and stop:

`Glider: this attachment couldn't be unpacked safely here, so nothing was published. Ask Glider to publish again in a moment.`

Each check below that fails ends the flow: nothing is left unzipped, you
call no Glider tool, say its line, word for word, and nothing else, and stop.

- It can't be read as a zip, or unzipping fails part way:
  `Glider: this attachment isn't a zip Glider can open. Zip the Skill's folder and attach it again.`
- An entry's path is absolute or has a `..` part, so it would land outside
  the folder:
  `Glider: this attachment holds a path that leads outside it (<entry>), which Glider won't unpack. Zip the Skill's folder again and attach it.`
- An entry is neither a regular file nor a folder, such as a symbolic link,
  or is a file named like a folder:
  `Glider: this attachment holds something that isn't a file or a folder (<entry>), which Glider won't publish. Replace it with a copy of the file and attach it again.`
- It holds more than 1,000 files, not counting OS metadata files, or more
  than 10,000 files and folders:
  `Glider: this attachment holds too many files (<count>), over what Glider will unpack. Remove what the Skill doesn't need and attach it again.`
- It unzips to more than 30 MB (31,457,280 bytes), the most the catalog
  takes:
  `Glider: this attachment unpacks to more than 30 MB, the most the catalog takes. Remove what the Skill doesn't need and attach it again.`

## Then follow SKILL.md's steps on what you unzipped

The unzipped folder is temporary, like the folder `SKILL.md`'s step 6 makes
for the zip. Keep it while you wait for the user's answer to the summary or
to a correction. Delete it whenever the flow ends: a check that fails,
anything other than a yes, a failure that ends the flow, or the report.
Wherever `SKILL.md` or `failures.md` says to delete the temporary folder,
delete this one too.

Follow every step of `SKILL.md` on what was unzipped, with these changes:

- **Step 1**: the folder is the unzipped one that holds `SKILL.md`: the top
  of the zip, or its one top-level folder. Ask for no path. If `SKILL.md` is
  in a top-level folder and the zip holds anything else at its top, other
  than step 4's OS metadata files, publishing would drop it. Call no tool,
  say this line and nothing else, and stop:
  `Glider: this attachment has files next to the Skill's folder (<the other entries>) that Glider would leave out. Zip just the Skill's folder and attach it again.`
- **Step 2**: in the plugin line and the link line, say `this attachment`
  in place of `this folder`.
- **Step 5**: the summary's last line is
  `Attachment: <the attachment's file name> (<file count> files)`, with the
  name the user gave the file: leave out any id your sandbox put in front of
  it. Never show a sandbox path. A corrected description or name is an edit to the unzipped
  `SKILL.md`, which is what gets published: when you offer it, say that the
  user's own copy stays as it is.
- **Step 6**: always build the zip again from the unzipped folder, under
  `<name>` whatever the attachment's folder is called, and never upload the
  attachment itself. Use step 6's commands, or your sandbox's own zip library
  if it has no `zip`.
- **Step 7**: send the zip from your sandbox, with step 7's `curl` or, if
  there is none, an HTTP `PUT` whose body is the zip's bytes. Add no headers
  and no token. If the `PUT` can't reach the link's host, follow "When the
  sandbox can't reach the upload link" below.

## When the sandbox can't reach the upload link

The `PUT` never reached the link's host
when it fails with a connection, DNS or proxy error, or with a refusal that
says the host is not allowed. A 403 from the host itself is a lapsed link,
which `failures.md` answers. Do not retry the `PUT`, here or later in this
flow. It does not count as a failed step. The user sends the zip instead:

1. Give the user the zip you built, `<name>.zip`, as a file to save: copy
   it out of the temporary folder to where your sandbox keeps files for the
   user to download, and present it under that name.
2. Say this, with the link you already have, and stop for their answer:

   `Glider: the upload can't be sent from here, so you'll need to send it yourself. Save <name>.zip, then within 15 minutes run this in a terminal, in the folder you saved it to:`

   ```bash
   curl -fsS -T "<name>.zip" "<upload.url>"
   ```

   `In Windows PowerShell, type curl.exe in place of curl. Tell Glider when it has run.`

3. When they say it ran, call `publish` as in `SKILL.md`'s step 7 and carry on
   from there.

A version gets two links at most: the one above and one more. Call `upload`
and say the lines of item 2 in the list above again with the new link, in
place of a `PUT` of your own, the first time one of these happens for a
version:

- The user says the command failed or the 15 minutes ran out.
- `publish` answers `upload_missing`. Start with
  `Glider: the upload didn't arrive, so here is a new link.`

When one of these happens after the second link, call `upload` no more, hand
over no link, say this and stop:

`Glider: the upload still didn't arrive, so nothing was published. Ask Glider to publish again in a few minutes.`

A new version after `version_exists` starts again with two links. Handing
over a link is not a failed step, but every failed `publish` still counts
towards `failures.md`'s limit of two.
