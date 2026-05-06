#!/usr/bin/env bash
# AI Designer Stack — install helper
#
# This script PRINTS the Claude Code commands you need to paste.
# Plugins in Claude Code are installed via slash commands inside the IDE,
# not via shell — so we just hand you the exact lines to copy.

set -e

cat <<'EOF'

╔════════════════════════════════════════════════════════════╗
║                  AI DESIGNER STACK                         ║
║          Curated Claude Code skills for designers          ║
╚════════════════════════════════════════════════════════════╝

📋 STEP 1 — Open Claude Code and run these commands one by one:

  /plugin marketplace add anthropics/skills
  /plugin marketplace add yahav123147/paid-ads-cro-skills
  /plugin marketplace add obra/superpowers
  /plugin marketplace add dangogit/workshop-setup-plugin

📦 STEP 2 — Install the plugins:

  /plugin install skills@anthropics
  /plugin install paid-ads-cro-skills@yahav123147
  /plugin install superpowers@obra
  /plugin install workshop-setup@dangogit

✅ STEP 3 — Try it:

  /design-shotgun
  /framer-motion-animator
  /taste-skill

That's it. See README.md for the full skill list and recommended workflow.

EOF
