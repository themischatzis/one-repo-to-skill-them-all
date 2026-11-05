#!/bin/bash
# Append one line per Copilot session to the private journal repo, then push.
# Reads the local session store, so sessions from closed tabs/windows are still caught.
set -euo pipefail
JOURNAL="${SKILL_JOURNAL_DIR:-$HOME/Projects/skill-journal}"
DB="$HOME/.copilot/session-store.db"
OUT="$JOURNAL/sessions/$(date +%Y-%m).md"
[ -d "$JOURNAL/.git" ] && [ -f "$DB" ] || { echo "journal or session store missing" >&2; exit 1; }

git -C "$JOURNAL" pull -q --rebase --autostash
mkdir -p "$JOURNAL/sessions"; touch "$OUT"
added=0
while IFS=$'\t' read -r id day repo branch summary; do
  short="${id:0:8}"
  grep -rqs "id:$short" "$JOURNAL/sessions" && continue
  echo "- $day [session] ${repo:-no-repo}${branch:+ ($branch)}: ${summary:-no summary} (id:$short)" >> "$OUT"
  added=$((added+1))
done < <(sqlite3 -readonly -separator $'\t' "$DB" \
  "select id, substr(updated_at,1,10), coalesce(repository,''), coalesce(branch,''), replace(coalesce(summary,''),char(10),' ')
   from sessions where updated_at >= date('now','-3 days') order by updated_at")

[ "$added" -gt 0 ] || exit 0
git -C "$JOURNAL" add sessions
git -C "$JOURNAL" commit -qm "feat: Log $added Copilot sessions on $(date +%F)" \
  -m "Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"
git -C "$JOURNAL" push -q
