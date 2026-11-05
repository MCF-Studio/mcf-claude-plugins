---
name: economie-tokens
description: Conseils pour consommer moins de tokens avec Claude Code - quand faire /clear ou /compact, quel modèle choisir, comment formuler une demande, alléger CLAUDE.md, les MCP et les sous-agents. À utiliser quand l'utilisateur dit qu'il atteint sa limite trop vite, demande pourquoi ça consomme autant, ou veut optimiser sa configuration.
---

# Économiser ses tokens

Le guide complet est dans `docs/guide-economiser-tokens.md` du dépôt du catalogue. L'essentiel :

**Règle d'or : un contexte court, une demande complète, le bon modèle pour la tâche.**

1. Chaque message renvoie **toute la conversation** : `/clear` à chaque changement de tâche (gratuit),
   `/compact` à un point d'étape d'une longue tâche.
2. Modèle : Sonnet par défaut, Opus / Fable seulement pour les problèmes durs (`/model`), Haiku pour les
   sous-agents simples.
3. Regrouper les modifications dans une seule demande, nommer les fichiers et fonctions, donner un moyen de
   vérifier, coller l'erreur utile et pas 5 000 lignes de log.
4. `CLAUDE.md` court (< 200 lignes) : les procédures longues et rares vont dans des **skills** ; les gros
   journaux d'avancement sont découpés (fichier court + archive consultée par recherche).
5. Désactiver les MCP inutiles (`/mcp`), interdire la lecture des dossiers lourds (`permissions.deny` sur
   `node_modules/`, `build/`, `.godot/`…), filtrer les sorties de tests (hook ou script).
6. Plan mode (Maj+Tab) pour les grosses tâches ; Échap dès que Claude part dans le mauvais sens, puis `/rewind`.
7. Vérifier `/context` et `/usage` de temps en temps.

Pour diagnostiquer une configuration : regarder la taille des `CLAUDE.md` chargés, des fichiers lus à chaque
début de session, le nombre de MCP actifs, puis proposer les coupes les plus rentables en premier.
