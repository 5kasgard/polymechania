# Engines: what can run a world while its owner is away

Independent research by a separate agent, checked against official pages
fetched 2026-10-28, plus a live test (issue #1). Kept close to as received.

## By plan

| Plan | Claude Code cloud scheduled tasks | Cloud sessions | Cowork scheduled tasks | Monthly API credits | Custom connectors |
|---|---|---|---|---|---|
| Free | no | no | no | no | yes, one |
| Pro | yes | yes | yes | no | yes |
| Max | yes | yes | yes | yes: $100 (5x), $200 (20x) | yes |
| Team | yes (Owner can switch off) | yes | yes (beta on web/mobile) | yes: $20/Standard, $100/Premium seat, pooled, capped at $500 | Owners add them |
| Enterprise | yes (Owner toggles, roles) | Premium or Chat + Claude Code seats | if enabled | no | admins add them |
| API only | no (`/schedule` needs a claude.ai login) | no | no | pay as you go | MCP connector in the API |

## Limits on cloud scheduled tasks

Minimum interval one hour; runs draw down the plan's usage like interactive
sessions; 100 scheduled runs per account per hour and 30 per task per hour
for manual and API fires, no overage; rejected when the usage window is
exhausted unless usage credits are on; can also be fired by GitHub events
or an HTTP POST with a per-task token; personal to one account, acting as
the owner with all its connectors; a research preview.
([scheduled tasks](https://code.claude.com/docs/en/web-scheduled-tasks),
[fire endpoint](https://platform.claude.com/docs/en/api/claude-code/routines-fire))

Other options: cloud sessions keep running with the laptop closed
([docs](https://code.claude.com/docs/en/claude-code-on-the-web)); desktop
scheduled tasks and `/loop` need the owner's machine awake, intervals down
to a minute ([docs](https://code.claude.com/docs/en/desktop-scheduled-tasks));
Cowork scheduled tasks run remotely, hourly or less often
([help](https://support.claude.com/en/articles/13854387-schedule-recurring-tasks-in-claude-cowork));
for API accounts, Managed Agents scheduled deployments, cron to the minute,
optional cost budget per run
([docs](https://platform.claude.com/docs/en/managed-agents/scheduled-deployments)).

## The rules

Subscription logins are only for ordinary use of Claude Code and Anthropic's
own apps; developers use API keys and may not offer Claude.ai login, route
requests through Free, Pro or Max credentials on users' behalf, or handle
their credentials or session tokens. A platform may host unmodified Claude
Code that users sign into themselves, if it accepts the Commercial Terms
and does not pay for, resell or intermediate users' usage. Advertised Pro
and Max limits assume ordinary, individual use.
([legal and compliance](https://code.claude.com/docs/en/legal-and-compliance),
[consumer terms](https://www.anthropic.com/legal/consumer-terms),
[Agent SDK](https://code.claude.com/docs/en/agent-sdk/overview))

**Grey area:** a product asking users to create a scheduled task in their
own Claude Code that calls the product's MCP server. Nothing official
addresses it: the task is Anthropic's feature, credentials never leave the
user, and usage is theirs; but if the product effectively drives the runs,
it could be read as routing the product's work through a subscription. A
written answer from Anthropic would settle it.

## What it means for Polymechania

- **Free:** worlds move only while the owner talks to their Claude. No
  unattended option.
- **Pro:** a world can wake on a schedule (hourly at most) inside the
  owner's own Claude Code, on their own usage, while ordinary and personal.
- **Max and Team:** the same, plus monthly API credits for a key that runs
  the world in the background properly.
- **Our hosted engine or the owner's API key:** the clean route for
  anything frequent, shared or product-driven (Managed Agents schedules,
  per-run budgets).
- **Ask Anthropic** about the grey area before building on it.
