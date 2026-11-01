"""Gabungkan artemis-openai.jsonc ke config ARTEMIS (backup dulu file lamanya).

Pemakaian (dari folder artemis-suara):
    uv run --project <folder-artemis> python pasang_config_openai.py <folder-artemis>

Komentar di file config lama akan hilang (isinya tetap); backup disimpan sebagai
config/artemis.jsonc.bak-YYYYmmdd-HHMMSS. Untuk kembali ke Gemini: kembalikan file backup itu.
"""

from __future__ import annotations

import json
import shutil
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent


def deep_merge(base: dict, override: dict) -> dict:
    out = dict(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(out.get(key), dict):
            out[key] = deep_merge(out[key], value)
        else:
            out[key] = value
    return out


def main() -> None:
    if len(sys.argv) != 2:
        sys.exit("Pakai: python pasang_config_openai.py <folder-artemis>")
    artemis_dir = Path(sys.argv[1]).resolve()
    target = artemis_dir / "config" / "artemis.jsonc"
    if not target.exists():
        sys.exit(f"Tidak ketemu {target}. Pastikan folder ARTEMIS benar.")

    sys.path.insert(0, str(artemis_dir))
    # Pakai pembersih komentar milik ARTEMIS sendiri supaya aman terhadap "//" di dalam string.
    from artemis.config.core.engine import _strip_json_comments

    original = json.loads(_strip_json_comments(target.read_text(encoding="utf-8")))
    override = json.loads(_strip_json_comments((HERE / "artemis-openai.jsonc").read_text(encoding="utf-8")))

    backup = target.with_name(f"artemis.jsonc.bak-{time.strftime('%Y%m%d-%H%M%S')}")
    shutil.copy2(target, backup)
    merged = deep_merge(original, override)
    target.write_text(json.dumps(merged, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"OK. Config OpenAI terpasang di {target}\nBackup: {backup}")


if __name__ == "__main__":
    main()
