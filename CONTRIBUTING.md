# Contribuer

Merci de proposer vos skills et plugins ! Le catalogue est public : tout ce qui est fusionné sera installé par
d'autres membres, sur leur machine. D'où quelques règles.

## Étapes

1. **Fork** du dépôt, puis une branche : `ajout/<nom-du-plugin>` ou `correction/<nom-du-plugin>`.
2. Créer (ou modifier) un dossier `plugins/<nom-du-plugin>/` :
   ```
   plugins/<nom>/
     .claude-plugin/plugin.json   # name, description, version (x.y.z), author, license
     README.md                    # à quoi ça sert, comment l'utiliser, prérequis
     skills/<skill>/SKILL.md      # frontmatter : name (= nom du dossier) + description (quoi ET quand)
     skills/<skill>/<script>.py   # facultatif : scripts appelés par le skill
     agents/<agent>.md            # facultatif
     commands/<commande>.md       # facultatif
     hooks/hooks.json             # facultatif (relecture renforcée, voir plus bas)
   ```
3. Déclarer le plugin dans `.claude-plugin/marketplace.json` (source `./plugins/<nom>`).
4. Vérifier : `python tools/validate.py` doit afficher `OK`.
5. Tester chez soi : `/plugin marketplace add <chemin de votre clone>` puis `/plugin install <nom>@mcf-studio`.
6. Ouvrir une **pull request** en remplissant le modèle. L'équipe relit, peut demander des changements, puis
   fusionne. Une nouvelle version d'un plugin existant = augmenter sa `version`.

## Règles

- **Nom** : minuscules, chiffres, tirets (`mon-plugin`). Langue : français de préférence (anglais accepté).
- **Un plugin = un sujet.** Préférer plusieurs petits plugins à un gros fourre-tout.
- **Description du skill** : dire ce qu'il fait *et quand l'utiliser* — c'est elle qui décide quand Claude le charge.
- **Skills courts** : aller à l'essentiel, renvoyer vers un fichier à côté pour le détail. Chaque ligne coûte des
  tokens à ceux qui l'utilisent.
- **Rien de personnel ni de secret** : pas de webhook, clé, jeton, mot de passe, adresse IP de serveur, chemin de
  votre disque (`C:\Users\…`) ou donnée de quelqu'un d'autre. Utiliser des variables d'environnement.
- **Pas de binaire ni d'archive** (`.exe`, `.dll`, `.zip`…) : tout doit être relisible. Scripts en Python ou
  Node, lisibles, commentés, multiplateformes (Windows, Linux, macOS) autant que possible.
- **Pas de téléchargement caché** : un script ne doit pas télécharger et exécuter du code au moment de l'usage.
  Les dépendances éventuelles sont listées dans le README et installées par l'utilisateur lui-même.
- **Pas de MCP vers un serveur distant inconnu** : tout serveur MCP déclaré doit être documenté (qui l'opère,
  quelles données il reçoit).
- **Hooks** : ils s'exécutent automatiquement chez tout le monde. Ils doivent être courts, sans accès réseau, et
  leur comportement expliqué dans le README. Relecture renforcée par deux personnes de l'équipe.
- Respecter les licences : ne publier que votre travail ou du contenu dont la licence le permet (citer la source).

## Signaler un problème

Bug ou idée : ouvrir une *issue* avec le modèle correspondant. Faille de sécurité : voir [SECURITY.md](SECURITY.md),
**pas** d'issue publique.
