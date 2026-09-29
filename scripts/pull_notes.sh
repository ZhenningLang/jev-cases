#!/usr/bin/env bash
# Pull Jev-related sections from the private RSS agent's notes into .notes/ (gitignored).
# Usage: CLAW_HOST=user@host scripts/pull_notes.sh
set -euo pipefail
: "${CLAW_HOST:?set CLAW_HOST to the ssh target of the RSS machine}"
NOTES_PATH="${NOTES_PATH:-/root/.openclaw/workspace-rss-helper/data/catchup/$(date +%Y-%m).md}"
OUT="$(dirname "$0")/../.notes"
mkdir -p "$OUT"
# Keep sections whose heading names Jev or a known Jev-family project; skip per-run log sections (their headings contain 轮).
ssh -o BatchMode=yes "$CLAW_HOST" "awk '
/^## / { p = (\$0 ~ /[Jj][Ee][Vv]|Kev|Decider|JEMM|TypeSafe|Nimble|CLM-8B|Eikos|Laya|[Tt]ev1|autorubric|DiffusionGemma/) && (\$0 !~ /轮/); n = 0 }
p && n < 22 { print; n++ }
' '$NOTES_PATH'" > "$OUT/jev_sections.md"
echo "wrote $OUT/jev_sections.md ($(grep -c '^## ' "$OUT/jev_sections.md") sections)"
