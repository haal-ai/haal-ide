#!/usr/bin/env sh
set -eu

REPO_URL=${REPO_URL:-"https://github.com/haal-ai/haal-ide"}
BRANCH=${BRANCH:-"main"}
TARGET_OLAF_DIR=${TARGET_OLAF_DIR:-"$HOME/.olaf"}

case "$REPO_URL" in
  https://github.com/*/*)
    OWNER_REPO=$(printf "%s" "$REPO_URL" | sed -E 's#^https://github.com/([^/]+/[^/]+)$#\1#')
    RAW_BASE="https://raw.githubusercontent.com/${OWNER_REPO}/${BRANCH}"
    ;;
  *)
    echo "Unsupported REPO_URL: $REPO_URL" >&2
    exit 1
    ;;
esac

if ! command -v python >/dev/null 2>&1; then
  echo "python not found on PATH. Install Python 3.12+ and retry." >&2
  exit 1
fi

TMP_DIR="${TMPDIR:-/tmp}/olaf-init-$$"
mkdir -p "$TMP_DIR"

cleanup() {
  rm -rf "$TMP_DIR" >/dev/null 2>&1 || true
}
trap cleanup EXIT INT TERM

INSTALLER="$TMP_DIR/install_olaf.py"
SELECT_COLLECTION="$TMP_DIR/select-collection.py"

curl -fsSL "$RAW_BASE/tools/install_olaf.py" -o "$INSTALLER"
curl -fsSL "$RAW_BASE/tools/select-collection.py" -o "$SELECT_COLLECTION"

python "$INSTALLER" --repo "$OWNER_REPO" --branch "$BRANCH" --target "$TARGET_OLAF_DIR" --local "$(pwd)"
python "$SELECT_COLLECTION"
