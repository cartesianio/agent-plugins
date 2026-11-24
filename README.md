# Glider

Glider by [Cartesian](https://cartesian.io) brings your team's agents into the AI
assistant you already use. It connects your assistant to the Cartesian MCP
service, so you can search the Glider catalog of skills and plugins and
install them with `/glider`.

## Install

- **Claude (individual account):** open Customize → Plugins → Add marketplace,
  enter `cartesianio/agent-plugins`, then install **glider**.
- **Claude Code:** run `claude plugin marketplace add cartesianio/agent-plugins`,
  then `claude plugin install glider@agent-plugins`.
- **ChatGPT (workspace admin):** add the Glider MCP server first, then import
  the `chatgpt` folder:
  1. In Plugins, select + → Add custom MCP server. Enter the URL
     `https://mcp.cartesian.io/mcp`, choose OAuth, tick "I understand and want
     to continue", select Create as a plugin, then install it.
  2. If the Glider MCP server lists no tools, open it in ChatGPT Settings →
     Plugins, click Connect and sign in.
  3. Plugins → Add → Import marketplace from
     `https://github.com/cartesianio/agent-plugins` with Path set to
     `chatgpt`, then set Glider to Installed. The import needs MFA on your
     ChatGPT account and a GitHub login.

On first use, sign in to Cartesian when the assistant asks you to.

## License

Glider is licensed under the [Apache License 2.0](LICENSE).
