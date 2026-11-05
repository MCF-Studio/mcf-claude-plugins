"""Lance un test Godot 4 en headless, avec des données utilisateur isolées et une sortie réduite.

Usage (depuis la racine du projet Godot) :
    python run_test.py <nom_du_test> [--dir tests] [--window] [--timeout 300] [--full] [-- args...]

- Exécutable Godot : variable d'environnement GODOT (sous Windows, le binaire « console »), sinon `godot`
  dans le PATH.
- <nom_du_test> : nom sans extension ; lance res://<dir>/<nom>.tscn s'il existe, sinon le script
  res://<dir>/<nom>.gd (via --script). Dossier par défaut : variable GODOT_TEST_DIR, sinon « tests ».
- APPDATA (Windows) et XDG_DATA_HOME (Linux) pointent vers un dossier temporaire neuf : les sauvegardes,
  réglages et identités de l'utilisateur (user://) ne sont jamais touchés.
- Toujours --audio-driver Dummy (aucun son). --window : avec fenêtre (captures, rendu) ; sinon --headless.
- Sortie : lignes OK / ÉCHEC / FAIL / PASS / erreurs + résumé ; --full pour tout afficher.
Code de retour = celui de Godot (0 = test réussi).
"""
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

KEEP = re.compile(r"^(OK|ÉCHEC|ECHEC|FAIL|PASS)\b|ERROR|SCRIPT ERROR|Parse Error|at: ", re.I)
OK_LINE = re.compile(r"(ok|pass)\b", re.I)
FAIL_LINE = re.compile(r"(échec|echec|fail)\b", re.I)


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass
    args = sys.argv[1:]
    extra: list[str] = []
    if "--" in args:
        i = args.index("--")
        args, extra = args[:i], args[i + 1:]
    if not args or args[0].startswith("-"):
        print(__doc__)
        return 2
    name = args[0]
    window = "--window" in args
    full = "--full" in args
    timeout = int(args[args.index("--timeout") + 1]) if "--timeout" in args else 300
    test_dir = args[args.index("--dir") + 1] if "--dir" in args else os.environ.get("GODOT_TEST_DIR", "tests")

    root = Path.cwd()
    if not (root / "project.godot").exists():
        print("Lancer depuis la racine du projet Godot (project.godot introuvable).")
        return 2
    folder = root / test_dir
    if (folder / f"{name}.tscn").exists():
        target = [f"res://{test_dir}/{name}.tscn"]
    elif (folder / f"{name}.gd").exists():
        target = ["--script", f"res://{test_dir}/{name}.gd"]
    else:
        print(f"Test introuvable : {test_dir}/{name}.tscn ou .gd")
        return 2

    godot = os.environ.get("GODOT") or shutil.which("godot")
    if not godot:
        print("Exécutable Godot introuvable : définir la variable GODOT.")
        return 2
    data = tempfile.mkdtemp(prefix=f"godot_test_{name}_")
    env = dict(os.environ, APPDATA=data, XDG_DATA_HOME=data)
    cmd = [godot] + ([] if window else ["--headless"]) + ["--audio-driver", "Dummy", "--path", str(root)] + target
    if extra:
        cmd += ["--"] + extra
    print("Commande :", " ".join(cmd))
    print("Données utilisateur isolées :", data)
    try:
        proc = subprocess.run(cmd, env=env, capture_output=True, text=True, encoding="utf-8",
                              errors="replace", timeout=timeout)
    except subprocess.TimeoutExpired:
        print(f"DÉLAI DÉPASSÉ ({timeout} s)")
        return 124
    lines = (proc.stdout + proc.stderr).splitlines()
    shown = lines if full else [line for line in lines if KEEP.search(line)]
    for line in shown[:200]:
        print(line)
    if len(shown) > 200:
        print(f"... {len(shown) - 200} lignes de plus (relancer avec --full)")
    oks = sum(1 for line in lines if OK_LINE.match(line))
    fails = sum(1 for line in lines if FAIL_LINE.match(line))
    print(f"--- {name} : code {proc.returncode}, {oks} OK, {fails} ÉCHEC, {len(lines)} lignes de sortie")
    return proc.returncode


if __name__ == "__main__":
    sys.exit(main())
