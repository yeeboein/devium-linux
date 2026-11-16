#!/usr/bin/env bash
# Devium's code checks (run on every push by .github/workflows/checks.yml, or locally: tools/check-code.sh)
set -uo pipefail
cd "$(dirname "$0")/.."
fail=0
bad() { echo "FAIL  $*"; fail=1; }
roots=(profile/airootfs build.sh tools editions)

echo "== Shell scripts (syntax, shellcheck errors)"
mapfile -t sh < <(grep -rlIE '^#!.*\b(bash|sh)\b' "${roots[@]}" 2>/dev/null | grep -v '\.py$' | sort)
for f in "${sh[@]}"; do bash -n "$f" 2>/dev/null || bad "$f: $(bash -n "$f" 2>&1 | head -1)"; done
if command -v shellcheck >/dev/null; then
    shellcheck -S error "${sh[@]}" || bad "shellcheck found errors"
fi
echo "   ${#sh[@]} scripts"

echo "== Python (syntax)"
mapfile -t py < <({ find "${roots[@]}" -name '*.py' 2>/dev/null; grep -rlIE '^#!.*python' "${roots[@]}" 2>/dev/null; } | sort -u)
for f in "${py[@]}"; do
    python3 -c 'import ast,sys; ast.parse(open(sys.argv[1]).read(), sys.argv[1])' "$f" 2>/dev/null || \
        bad "$f: $(python3 -c 'import ast,sys; ast.parse(open(sys.argv[1]).read(), sys.argv[1])' "$f" 2>&1 | tail -1)"
done
echo "   ${#py[@]} files"

echo "== JSON"
mapfile -t js < <(find "${roots[@]}" -name '*.json' 2>/dev/null | sort)
for f in "${js[@]}"; do python3 -m json.tool "$f" >/dev/null 2>&1 || bad "$f is not valid JSON"; done
# fastfetch's .jsonc: valid once // comments are removed
for f in $(find "${roots[@]}" -name '*.jsonc' 2>/dev/null); do
    python3 - "$f" <<'PY' || bad "$f is not valid JSONC"
import json, re, sys
text = open(sys.argv[1]).read()
text = re.sub(r'^\s*//.*$', '', text, flags=re.M)
json.loads(text)
PY
done
echo "   ${#js[@]} files"

echo "== JavaScript (KWin scripts and effects)"
if command -v node >/dev/null; then
    n=0
    while IFS= read -r f; do node --check "$f" 2>/dev/null || bad "$f: $(node --check "$f" 2>&1 | grep -m1 Error)"; n=$((n+1)); done \
        < <(find profile/airootfs/usr/share/kwin -name '*.js' 2>/dev/null)
    echo "   $n files"
fi

echo "== Desktop files"
if command -v desktop-file-validate >/dev/null; then
    while IFS= read -r f; do
        out=$(desktop-file-validate "$f" 2>&1 | grep -E ' error: ' | grep -v 'X-' ) && [[ -n $out ]] && bad "$f: $out"
    done < <(find profile/airootfs -name '*.desktop' 2>/dev/null)
fi

echo "== Every file in profiledef.sh permissions exists"
while IFS= read -r p; do
    [[ -e profile/airootfs$p ]] || bad "profiledef.sh lists $p but it doesn't exist"
done < <(grep -oE '\["/[^"]+"\]' profile/profiledef.sh | tr -d '[]"')

(( fail )) && { echo; echo "Some checks failed."; exit 1; }
echo; echo "All checks passed."
