#!/usr/bin/env bash
# HyperFrames CLI wrapper (it is a Claude Code plugin, not an npm global).
#   bash hf.sh lint public | bash hf.sh snapshot public --at 3.2 | bash hf.sh render public -o out.mp4 --fps 30 --low-memory-mode
#   bash hf.sh remove-background seg.mp4 -o m.mov --device cpu
CLI=$(ls -d "$HOME"/.claude/plugins/cache/hyperframes/hyperframes/*/skills/hyperframes/scripts/plugin-cli.mjs 2>/dev/null | sort -V | tail -1)
[ -z "$CLI" ] && { echo "HyperFrames plugin not found" >&2; exit 1; }
exec node "$CLI" "$@"
