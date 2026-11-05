# MCF Studio — catalogue de skills et plugins Claude Code

Catalogue communautaire de **skills** et **plugins** pour [Claude Code](https://code.claude.com), tenu par
MCF Studio et ouvert aux membres du Discord : chacun peut les installer et proposer les siens.

## Installer

Dans Claude Code :

```
/plugin marketplace add LeBriCodeur/mcf-claude-plugins
/plugin install godot-workflow@mcf-studio
```

Mettre à jour plus tard : `/plugin marketplace update mcf-studio`.
Voir ce qu'un plugin contient avant de l'installer : `claude plugin details godot-workflow@mcf-studio`.

## Plugins disponibles

| Plugin | Contenu | Pour qui |
| --- | --- | --- |
| [`godot-workflow`](plugins/godot-workflow) | Skills `godot-headless-test` (tests Godot 4 sans son, données utilisateur isolées, sortie filtrée) et `godot-editor-scenes` (modifier les scènes avec l'éditeur ouvert sans rien casser) | Développeurs Godot 4 |
| [`econome-tokens`](plugins/econome-tokens) | Skill `economie-tokens` + [guide complet](docs/guide-economiser-tokens.md) | Tout utilisateur de Claude Code |

## C'est quoi, un skill ? un plugin ?

| | Chargé quand | Sert à |
| --- | --- | --- |
| **Skill** | Seulement quand la tâche correspond (ou par `/nom`) | Une procédure : tester, déployer, publier… |
| **Hook** | Automatiquement avant / après une action de Claude | Une règle qui ne doit jamais être oubliée |
| **Agent** | Quand on le lance, dans son propre contexte | Le travail bruyant qui ne renvoie qu'un résumé |
| **Plugin** | Installé une fois | Le paquet qui regroupe skills, hooks, agents, commandes |

## Proposer un ajout

Lire [CONTRIBUTING.md](CONTRIBUTING.md) : fork, un dossier par plugin dans `plugins/`, vérification
`python tools/validate.py`, pull request relue par l'équipe avant fusion.

## Sécurité

Un plugin peut exécuter du code sur la machine de ceux qui l'installent (hooks, scripts). Chaque ajout est **relu
ligne à ligne** avant fusion, et aucun binaire ni secret n'est accepté. Détails et signalement :
[SECURITY.md](SECURITY.md). Comme pour tout logiciel, relisez ce que vous installez.

## Licence

[MIT](LICENSE). En proposant une contribution, vous acceptez qu'elle soit publiée sous cette licence.
