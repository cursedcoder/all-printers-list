import json
import yaml
import sys
from pathlib import Path
from collections import defaultdict

src_dir = Path(sys.argv[1])
out_dir = Path(sys.argv[2])
vendor_map = defaultdict(list)

for json_file in sorted(src_dir.glob("*.json")):
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    for fw_ver, meta in data.items():
        printer = {
            "firmware": fw_ver,
            "model_id": meta.get("model_id"),
            "display_name": meta.get("display_name"),
            "printer_type": meta.get("printer_type"),
            "slug": meta.get("printer_type", "").lower().replace(" ", "-"),
            "thumbnail": f"icons/bambulab/{meta.get('printer_thumbnail_image', '')}.webp",
            "arch": meta.get("printer_arch"),
            "series": meta.get("printer_series"),
            "enclosed": meta.get("printer_is_enclosed"),
            "features": meta.get("print", {}),
        }
        vendor = meta.get("display_name", "Unknown").split()[0].lower()
        vendor_map[vendor].append(printer)

# Write by-vendor YAML
vendor_dir = out_dir / "by-vendor"
vendor_dir.mkdir(parents=True, exist_ok=True)

for vendor, printers in vendor_map.items():
    with open(vendor_dir / f"{vendor}.yaml", "w", encoding="utf-8") as f:
        yaml.dump({ "vendor": vendor, "printers": printers }, f, sort_keys=False)

# Write root all.yaml
all_data = []
for printers in vendor_map.values():
    all_data.extend(printers)

with open(out_dir / "all.yaml", "w", encoding="utf-8") as f:
    yaml.dump({ "all_printers": all_data }, f, sort_keys=False)
