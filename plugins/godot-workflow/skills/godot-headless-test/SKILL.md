---
name: godot-headless-test
description: Lancer et lire des tests Godot 4 en headless sans son et sans toucher aux sauvegardes ni aux réglages de l'utilisateur (données user:// isolées), avec une sortie réduite aux résultats. À utiliser pour tester une modification d'un projet Godot, relancer un test existant ou écrire un nouveau test automatisé.
---

# Tests Godot en headless

## Règles
- **Toujours `--audio-driver Dummy`** : aucun son pendant les tests.
- **Données utilisateur isolées** : un test qui lance le jeu écrit dans `user://` (sauvegardes, réglages, jetons
  d'identité…). Rediriger `APPDATA` (Windows) / `XDG_DATA_HOME` (Linux) vers un dossier temporaire. Si un test a
  quand même touché les vrais fichiers : les **déplacer** (jamais supprimer) et restaurer la copie.
- Ne jamais coller toute la sortie dans la conversation : seulement les résultats et les erreurs.

## Lancer
Le script `run_test.py` (à côté de ce fichier) fait tout cela :
```
python <chemin du skill>/run_test.py <nom>                # headless, sortie filtrée
python <chemin du skill>/run_test.py <nom> --window       # avec fenêtre (captures, rendu)
python <chemin du skill>/run_test.py <nom> --dir tests_tmp --full
```
Réglages : variable `GODOT` (binaire Godot, la version **console** sous Windows), `GODOT_TEST_DIR` (dossier des
tests, « tests » par défaut). Code de retour 0 = réussi.

## Écrire un test
- Une scène ou un script par sujet dans le dossier de tests, versionné.
- Afficher une ligne par vérification : `OK  <quoi>` ou `ÉCHEC <quoi>`, puis
  `get_tree().quit(1 if _fails > 0 else 0)`.
- Captures d'écran : les enregistrer dans le dossier de données isolé, puis les **regarder** (mesurer sur l'image
  rendue plutôt que sur les transforms).

## Jeux en réseau
- Un dossier de données par processus (serveur, client A, client B) et un port propre au test.
- Si le serveur dédié ne charge pas tout le monde (carte, objets), tester les fonctions liées au monde contre un
  **vrai serveur dédié**, pas un hôte : un hôte a toute la scène, le dédié non, et le test peut passer alors que la
  production casse.
- Attendre la fin de chaque processus avant le test suivant (un serveur resté vivant garde le port).
