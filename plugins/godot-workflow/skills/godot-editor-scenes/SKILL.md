---
name: godot-editor-scenes
description: Règles et pièges pour créer ou modifier des scènes (.tscn), nœuds et scripts d'un projet Godot 4 pendant que l'éditeur est ouvert, à la main ou via un serveur MCP Godot. À utiliser avant de modifier une scène ou un script d'un projet Godot dont l'éditeur peut être ouvert, et avant de commiter une scène réenregistrée par l'éditeur.
---

# Modifier un projet Godot avec l'éditeur ouvert

## Choisir la méthode
- Si un serveur MCP Godot relié à l'éditeur est disponible : modifier les **scènes déjà ouvertes ou connues de
  l'éditeur** par ses outils (pas de conflit, Ctrl+Z possible). Sinon l'éditeur peut réécraser le fichier modifié
  sur le disque.
- Une **nouvelle** scène peut être écrite directement en `.tscn` (aucun conflit).
- Les nouveaux scripts avec `class_name` doivent être connus de l'éditeur (cache
  `.godot/global_script_class_cache.cfg`) : créer d'abord les scripts dont les autres dépendent.

## Après chaque série de modifications
1. Lire les erreurs de l'éditeur (journal / sortie).
2. `git diff` de chaque `.tscn` touché :
   - les lignes `[connection]` (signaux) sont toujours là ;
   - pas de propriétés `= null` ajoutées par l'éditeur (scène réenregistrée après une modif de script sur disque) ;
   - pas de fichiers `.import` réécrits sans raison (les restaurer).
3. Après une modification de `project.godot` (autoloads, actions, plugins) : demander à l'utilisateur
   **Projet > Recharger le projet actuel**.
4. Tester (skill `godot-headless-test`), puis commiter.

## Pièges connus
- Un autoload ajouté à `project.godot` hors de l'éditeur n'est pas vu par les vérifications de syntaxe de
  l'éditeur (faux « Identifier not found ») : vérifier par un vrai lancement.
- Les scripts `@tool` ne sont pas toujours rechargés par l'éditeur : ne pas réenregistrer une scène qui les
  utilise avant rechargement.
- Un seul `Polygon2D` ne dessine qu'une forme : un polygone qui se croise n'affiche rien.
- Interfaces et niveaux : préférer des scènes `.tscn` éditables (une par élément, instanciées) à de l'UI ou des
  cartes construites par code — l'utilisateur doit pouvoir les retoucher dans l'éditeur.
