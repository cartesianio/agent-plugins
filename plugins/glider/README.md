# Glider

Find, install, update, pin and remove the Skills your company offers through
Glider, and publish your own, without leaving Claude. Ask in plain words, or use a command:

- `/glider:list` shows every Skill your company has released.
- `/glider:search <phrase>` finds the Skills that fit one need.
- `/glider:install <name> [version]` installs one, at its released version or
  the version you name.
- `/glider:update [name]` updates one installed Skill, or all of them, to the
  released version. Naming a pinned Skill removes its pin; updating all of
  them leaves pinned Skills alone.
- `/glider:pin <name>` pins an installed Skill at the version you have, so
  Glider stops offering updates for it.
- `/glider:status` shows which of your company's Skills you have, at which
  versions, and whether each is current, has an update, is pinned or is no
  longer offered.
- `/glider:remove <name>` gives the steps to remove a Skill on the surface you
  are using.
- `/glider:publish [path]` publishes a Skill you wrote as a new version,
  released to your whole company at once or held back for testing.
- `/glider:release <name> <version>` releases a version of a Skill you
  authored to everyone in your company, or rolls back to an earlier one.
