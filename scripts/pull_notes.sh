#!/usr/bin/env bash
# Pull Jev-related notes from the private RSS agent into .notes/ (gitignored).
# Usage: CLAW_HOST=user@host scripts/pull_notes.sh
# Writes two files:
#   jev_sections.md  whole sections whose heading names Jev or a Jev-family project (incl. 增量 lines appended later)
#   jev_mentions.md  lines in other sections that mention them (the agent often files a Jev test under an unrelated item)
set -euo pipefail
: "${CLAW_HOST:?set CLAW_HOST to the ssh target of the RSS machine}"
NOTES_PATH="${NOTES_PATH:-/root/.openclaw/workspace-rss-helper/data/catchup/$(date +%Y-%m).md}"
OUT="$(dirname "$0")/../.notes"
mkdir -p "$OUT"
RAW="$(mktemp)"
trap 'rm -f "$RAW"' EXIT
ssh -o BatchMode=yes -o ServerAliveInterval=30 "$CLAW_HOST" "cat '$NOTES_PATH'" > "$RAW"

# Jev itself, followers/clones, and the product category name.
KEYS='[Jj][Ee][Vv]|Kev|Decider|JEMM|TypeSafe|Nimble|CLM-8B|Eikos|Laya|[Tt]ev1|autorubric|DiffusionGemma|SemIf|Julia-1|LiquidAI|Decisions API|决策模型|[Dd]ecision model'
# Per-run log sections (headings with 轮/run/记录) are mostly skip lists; their bookkeeping lines are dropped too.
awk -v K="$KEYS" '/^## / { p = ($0 ~ K) && ($0 !~ /轮/) } p' "$RAW" > "$OUT/jev_sections.md"
awk -v K="$KEYS" '
/^## / { h = $0; p = ($0 ~ K) && ($0 !~ /轮/); runlog = ($0 ~ /轮|[Rr]un|记录/); shown = 0; next }
!p && !runlog && $0 ~ K && !/^- (查重|跳过|回声|核实|沉淀|筛过|count|本轮|投递|失败源)/ {
  if (!shown) { print ""; print h; shown = 1 }
  print
}' "$RAW" > "$OUT/jev_mentions.md"

echo "wrote $OUT/jev_sections.md ($(grep -c '^## ' "$OUT/jev_sections.md") sections), $OUT/jev_mentions.md ($(grep -c '^## ' "$OUT/jev_mentions.md") sections)"
