"""Vérifie le catalogue : manifestes JSON, skills (frontmatter), absence de secrets et de fichiers interdits.

Usage : python tools/validate.py   (depuis la racine du dépôt ; lancé aussi par la CI sur chaque PR)
Code de retour 0 = tout est bon.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NAME = re.compile(r"^[a-z0-9][a-z0-9-]{1,63}$")
SECRETS = [
    (re.compile(r"discord(app)?\.com/api/webhooks/\d+/[\w-]+"), "webhook Discord"),
    (re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"), "clé privée"),
    (re.compile(r"\b(ghp|gho|ghs|github_pat)_[A-Za-z0-9_]{20,}"), "jeton GitHub"),
    (re.compile(r"\bsk-ant-[A-Za-z0-9_-]{20,}"), "clé API Anthropic"),
    (re.compile(r"\bsk-[A-Za-z0-9]{32,}"), "clé API"),
    (re.compile(r"\bAKIA[0-9A-Z]{16}\b"), "clé AWS"),
    (re.compile(r"\bxox[abpr]-[A-Za-z0-9-]{10,}"), "jeton Slack"),
    (re.compile(r"[MN][A-Za-z\d]{23,25}\.[\w-]{6}\.[\w-]{27,}"), "jeton de bot Discord"),
]
FORBIDDEN_SUFFIXES = {".exe", ".dll", ".so", ".dylib", ".bat", ".cmd", ".ps1", ".scr", ".msi", ".jar", ".zip", ".7z", ".rar"}
TEXT_SUFFIXES = {".md", ".json", ".py", ".js", ".mjs", ".ts", ".sh", ".txt", ".yml", ".yaml", ".toml", ".cfg"}

errors: list[str] = []


def err(msg: str) -> None:
    errors.append(msg)


def frontmatter(text: str) -> dict:
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end < 0:
        return {}
    data = {}
    for line in text[3:end].splitlines():
        if ":" in line and not line.startswith(" "):
            key, _, value = line.partition(":")
            data[key.strip()] = value.strip()
    return data


def check_marketplace() -> list[str]:
    path = ROOT / ".claude-plugin" / "marketplace.json"
    try:
        market = json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        err(f"{path.name} illisible : {e}")
        return []
    names = []
    for p in market.get("plugins", []):
        name = p.get("name", "")
        if not NAME.match(name):
            err(f"marketplace : nom de plugin invalide « {name} » (minuscules, chiffres, tirets)")
        if re.match(r"^(claude|anthropic|anthropics|cc-plugin)(-|$)", name) or name == "claude-mods":
            err(f"marketplace : « {name} » est un nom réservé à Anthropic (ne pas commencer par claude-, anthropic-…)")
        if name in names:
            err(f"marketplace : plugin « {name} » en double")
        names.append(name)
        src = p.get("source")
        if not isinstance(src, str) or not src.startswith("./plugins/"):
            err(f"marketplace : « {name} » doit avoir une source locale ./plugins/<nom> (pas de dépôt externe)")
        elif src != f"./plugins/{name}":
            err(f"marketplace : la source de « {name} » doit être ./plugins/{name}")
        if not p.get("description"):
            err(f"marketplace : « {name} » sans description")
    return names


def check_plugin(name: str) -> None:
    folder = ROOT / "plugins" / name
    manifest = folder / ".claude-plugin" / "plugin.json"
    if not manifest.exists():
        err(f"{name} : .claude-plugin/plugin.json manquant")
        return
    try:
        data = json.loads(manifest.read_text(encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        err(f"{name} : plugin.json illisible : {e}")
        return
    if data.get("name") != name:
        err(f"{name} : le nom dans plugin.json doit être « {name} »")
    if not re.match(r"^\d+\.\d+\.\d+$", str(data.get("version", ""))):
        err(f"{name} : version manquante ou invalide (x.y.z)")
    if not (folder / "README.md").exists():
        err(f"{name} : README.md manquant (à quoi sert le plugin, comment l'utiliser)")
    for skill in sorted((folder / "skills").glob("*/")):
        md = skill / "SKILL.md"
        if not md.exists():
            err(f"{name}/skills/{skill.name} : SKILL.md manquant")
            continue
        fm = frontmatter(md.read_text(encoding="utf-8"))
        if fm.get("name") != skill.name:
            err(f"{name}/skills/{skill.name} : « name » du frontmatter doit être « {skill.name} »")
        if len(fm.get("description", "")) < 40:
            err(f"{name}/skills/{skill.name} : description absente ou trop courte (dire quoi ET quand l'utiliser)")
    hooks = folder / "hooks" / "hooks.json"
    if hooks.exists():
        try:
            json.loads(hooks.read_text(encoding="utf-8"))
        except Exception as e:  # noqa: BLE001
            err(f"{name} : hooks.json illisible : {e}")


def check_unlisted(names: list[str]) -> None:
    for folder in sorted((ROOT / "plugins").glob("*/")):
        if folder.name not in names:
            err(f"plugins/{folder.name} n'est pas déclaré dans .claude-plugin/marketplace.json")


def check_files() -> None:
    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts:
            continue
        rel = path.relative_to(ROOT)
        if path.suffix.lower() in FORBIDDEN_SUFFIXES:
            err(f"{rel} : type de fichier interdit (binaire, archive ou script Windows non relisible)")
        if path.stat().st_size > 1_000_000:
            err(f"{rel} : fichier trop gros (> 1 Mo)")
        if path.suffix.lower() in TEXT_SUFFIXES:
            text = path.read_text(encoding="utf-8", errors="replace")
            for pattern, label in SECRETS:
                if pattern.search(text):
                    err(f"{rel} : ressemble à un secret ({label}) — ne jamais publier de secret")


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass
    names = check_marketplace()
    for name in names:
        check_plugin(name)
    check_unlisted(names)
    check_files()
    if errors:
        print("ÉCHEC de la vérification :")
        for e in errors:
            print(" -", e)
        return 1
    print(f"OK : {len(names)} plugin(s) vérifié(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
