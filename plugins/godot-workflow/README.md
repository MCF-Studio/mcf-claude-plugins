# godot-workflow

Skills pour travailler avec Claude Code sur un projet **Godot 4**.

| Skill | Ce qu'il fait |
| --- | --- |
| `godot-headless-test` | Lance un test en headless avec `--audio-driver Dummy`, les données `user://` redirigées vers un dossier temporaire (vos sauvegardes et réglages ne sont jamais touchés) et une sortie réduite aux OK / ÉCHEC / erreurs. Script `run_test.py`. |
| `godot-editor-scenes` | Règles pour modifier scènes et scripts quand l'éditeur est ouvert (seul ou via un serveur MCP Godot) : ordre de création, vérifications du `git diff` (signaux, propriétés `= null`, `.import`), rechargement du projet. |

## Prérequis

- Python 3.9+.
- Variable d'environnement `GODOT` = chemin de l'exécutable Godot (sous Windows, la version `_console.exe`),
  sinon `godot` doit être dans le PATH. Facultatif : `GODOT_TEST_DIR` (dossier des tests, `tests` par défaut).

## Exemple

```
python <chemin du skill>/run_test.py inventaire_unit --dir tests
```
Les tests affichent une ligne `OK  <vérification>` ou `ÉCHEC <vérification>` et quittent avec le code 1 en cas
d'échec (`get_tree().quit(1 if _fails > 0 else 0)`).

Aucun hook, aucun accès réseau.
