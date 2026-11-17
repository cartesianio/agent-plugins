# Glider

Glider by [Cartesian](https://cartesian.io) brings your team's agents into the AI
assistant you already use. It connects your assistant to the Cartesian MCP
service, so you can search the Glider catalogue of skills and plugins and
install them with `/glider`.

## Install

- **Claude (individual account):** open Customize → Plugins → Add marketplace,
  enter `cartesianio/agent-plugins`, then install **glider**.
- **Claude Code:** run `claude plugin marketplace add cartesianio/agent-plugins`,
  then `claude plugin install glider@agent-plugins`.
- **ChatGPT (workspace admin):** open Admin Console → Plugins → Import
  marketplace and enter `https://github.com/cartesianio/agent-plugins`.

On first use, sign in to Cartesian when the assistant asks you to.

## License

Glider is licensed under the [Apache License 2.0](LICENSE).
