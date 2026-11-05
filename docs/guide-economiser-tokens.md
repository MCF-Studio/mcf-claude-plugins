# Guide Claude Code — Économiser ses tokens

Nov 4, 2026 · @Aroun

Chère communauté MCF studio, voici un petit document pour optimiser votre utilisation de vos IA Claude, et surtout de Claude Code.

On voit passer souvent les mêmes questions sur le Discord : « j'ai cramé ma limite en 2 heures », « pourquoi ça consomme autant ? ». La bonne nouvelle : 80 % du gaspillage vient de quelques mauvaises habitudes faciles à corriger. Ce guide les regroupe, avec les commandes à connaître et un comparatif du coût de chaque modèle.

**La règle d'or à retenir si vous ne lisez qu'une ligne :** un contexte court, une demande complète, le bon modèle pour la tâche.

## 1. Comment Claude consomme vos tokens

À chaque message, Claude Code renvoie **toute la conversation** au modèle, pas seulement votre dernière phrase. Plus la session est longue, plus chaque message coûte cher, même un simple « ok merci ».

Ce qui remplit le contexte (et donc la facture) :

- **L'historique de la conversation** : chaque question, chaque réponse, chaque essai raté.
- **Les fichiers lus** : un fichier de 2 000 lignes ouvert une fois reste dans le contexte pour toute la suite.
- **Les résultats d'outils** : logs, sorties de tests, résultats de recherche, tout est stocké.
- **Le CLAUDE.md et les serveurs MCP** : chargés à chaque requête.
- **La réflexion du modèle (thinking)** : facturée comme des tokens de sortie, les plus chers.

Le cache de prompt réduit le coût de l'historique répété, mais il expire après une pause : le premier message après une longue pause retraite tout le contexte au prix fort.

**À retenir :** une question d'une ligne dans une session ouverte depuis le matin coûte le prix de toute la session. C'est pour ça que les gens « crament » leur limite sans comprendre pourquoi.

## 2. Choisir le bon modèle

À travail égal, Fable coûte environ **5 fois plus** que Sonnet, et Haiku environ **20 fois moins**. Sonnet sert de base 100 % dans le tableau ci-dessous.

| Modèle | Prix API entrée / sortie (par million de tokens) | Coût relatif (Sonnet = 100 %) | À utiliser pour |
| --- | --- | --- | --- |
| Haiku 5.5 | 0,10 $ / 0,50 $ | \~5 % | Petites tâches répétitives, renommages, sous-agents simples, recherche dans le code |
| Sonnet 5.5 | 2 $ / 10 $ | 100 % | **Le choix par défaut** : features, bugs, tests, revue de code |
| Opus 5.5 | 4 $ / 20 $ | \~200 % | Refactors sur plusieurs fichiers, bugs vicieux, architecture |
| Fable 5.1 | 10 $ / 50 $ | \~500 % | Problèmes vraiment durs, quand Opus a échoué |

Prix API publics relevés en octobre 2026 ([tarifs Anthropic](https://platform.claude.com/docs/en/about-claude/pricing), [détail](https://claudecoworkcourse.com/ai-api-pricing/claude)). Sur un abonnement Pro / Max, ces % ne sont pas une règle officielle mais donnent le bon ordre de grandeur : une session sur Fable vide votre quota bien plus vite qu'une session sur Sonnet. Attention, Haiku 5.5 coûte plus cher au-delà de 100 000 tokens de prompt (0,50 $ / 2,50 $).

**La bonne méthode :** travaillez sur Sonnet par défaut, passez sur Opus ou Fable avec `/model` pour une question difficile, puis revenez sur Sonnet. Sur un abonnement, quand vous atteignez la limite d'une session ou de la semaine, changer de modèle ne débloque rien : la limite est commune à tous les modèles.

## 3. Gérer le contexte : le levier n°1

Un contexte propre, c'est l'économie la plus importante, et elle est gratuite. Les commandes à connaître :

| Commande | Ce qu'elle fait | Quand l'utiliser |
| --- | --- | --- |
| `/clear` | Repart d'une conversation vide. Ne coûte rien | Dès que vous changez de tâche (fini le bug, on passe à l'UI) |
| `/rename` puis `/resume` | Nomme la session pour la retrouver plus tard | Avant un `/clear`, si vous voulez pouvoir revenir dessus |
| `/compact` | Résume la conversation pour libérer de la place | Au milieu d'une longue tâche, à un point d'étape (feature finie, bug corrigé) |
| `/compact <consigne>` | Résume en gardant ce que vous précisez | Ex. : `/compact garde la liste des fichiers modifiés et les résultats de tests` |
| `/context` | Montre ce qui occupe le contexte | Quand ça consomme trop sans raison apparente |
| `/usage` | Affiche votre consommation et des recommandations | Régulièrement, pour voir où partent vos tokens |
| `/rewind` ou Échap 2 fois | Revient à un point précédent (conversation et code) | Quand Claude est parti dans une mauvaise direction |
|  |  |  |

**`/clear` ou `/compact` ?**

- Nouvelle tâche sans rapport → `/clear`. C'est gratuit.
- Même tâche, mais la conversation est longue → `/compact`. Attention : compacter un gros contexte est lui-même une grosse requête, ne le faites pas toutes les 5 minutes.
- Évitez de compacter en plein milieu d'une implémentation : le résumé peut perdre un détail dont l'étape suivante a besoin.

**Astuce :** appuyez sur Échap dès que Claude part dans le mauvais sens. Chaque seconde où il continue, il lit des fichiers et écrit du code que vous allez jeter.

## 4. Bien formuler ses demandes

Une demande complète et précise coûte moins cher que dix petites demandes floues. Chaque aller-retour renvoie tout le contexte.

**Regroupez vos modifications.** Ne faites pas une demande pour changer une couleur, puis une autre pour un texte, puis une autre pour une marge. Listez tout d'un coup :

```
Dans src/ui/HudMenu.cs :
1. Passe le bouton "Quitter" en rouge
2. Remplace le texte "Start" par "Jouer"
3. Ajoute 8 px de marge entre les boutons
```

**Donnez les fichiers.** « Corrige le bug de l'inventaire » oblige Claude à fouiller tout le projet. « Corrige le crash quand on drop un item dans `Inventory.rs`, fonction `drop_item` » lui évite des dizaines de lectures. Vous pouvez aussi citer un fichier avec `@chemin/du/fichier`.

**Évitez les demandes vagues.** « Améliore le code » ou « optimise le projet » déclenchent un scan complet du dépôt. Dites quoi améliorer et où.

**Donnez un moyen de vérifier.** Un test, un résultat attendu, une capture d'écran : Claude corrige ses erreurs lui-même au lieu que vous deviez redemander.

**Ne collez pas des logs entiers.** Collez l'erreur et les 20 lignes autour, pas les 5 000 lignes de la console.

**Pour les petites modifs triviales, faites-les vous-même.** Changer un nombre dans un fichier vous prend 5 secondes. Le demander à Claude dans une session chargée peut coûter des dizaines de milliers de tokens.

## 5. CLAUDE.md et configuration

Le fichier `CLAUDE.md` à la racine du projet est chargé **à chaque requête**. Bien écrit, il évite à Claude de redécouvrir le projet à chaque session. Trop gros, il plombe chaque message.

**Ce qu'on met dans CLAUDE.md :**

- L'architecture en quelques lignes (dossiers clés, moteur, langage)
- Les commandes pour build et lancer les tests
- Les conventions de nommage et de style
- Des consignes de compactage, par exemple :

```markdown
# Compact instructions
Quand tu compactes, garde les résultats de tests et la liste des fichiers modifiés.
```

**Ce qu'on n'y met pas :** les procédures longues et rares (process de release, migration de base de données…). Mettez-les dans des **skills**, qui ne se chargent que quand on en a besoin. Visez moins de 200 lignes. Lancez `/init` pour générer une première version, puis élaguez.

**Réglages utiles :**

- **Modèle par défaut** : réglez Sonnet dans `/config`, ou lancez `claude --model sonnet`.
- **Niveau d'effort** : `/effort` baisse la réflexion du modèle pour les tâches simples. La réflexion est facturée en tokens de sortie, les plus chers.
- **Bloquer les dossiers inutiles** : empêchez Claude de lire les builds, dépendances et assets lourds via les permissions de `.claude/settings.json`, par exemple `"permissions": { "deny": ["Read(./build/**)", "Read(./node_modules/**)"] }`.
- **Afficher le contexte en permanence** : configurez la barre de statut avec `/statusline` pour voir le remplissage du contexte en direct.

## 6. Plan mode, sous-agents et MCP

Ces outils peuvent faire économiser beaucoup, ou coûter très cher, selon l'usage.

**Plan mode (Shift+Tab) : à utiliser pour les grosses tâches.** Claude explore et propose un plan avant de toucher au code. Vous validez ou corrigez la direction avant qu'il écrive 500 lignes à jeter. Pour un petit fix, inutile.

**Sous-agents : utiles pour isoler le bruit.** Lancer les tests, lire de gros logs, fouiller la doc : un sous-agent fait le travail dans son propre contexte et ne renvoie qu'un résumé. Votre conversation principale reste légère. Mais chaque sous-agent consomme aussi votre quota : configurez-les sur Haiku pour les tâches simples (`model: haiku` dans leur config).

**Agent teams : à éviter sauf besoin réel.** Plusieurs instances de Claude tournent en parallèle, chacune avec son contexte. La doc officielle parle d'environ **7 fois plus de tokens** qu'une session normale.

**Serveurs MCP : désactivez ceux que vous n'utilisez pas.** Tapez `/mcp` pour voir la liste et couper l'inutile. Quand un outil en ligne de commande existe (`gh`, `git`…), il est plus économe qu'un MCP.

**Hooks : filtrez la sortie avant que Claude la lise.** Un hook peut par exemple ne garder que les lignes `FAIL` ou `ERROR` d'une sortie de tests. On passe de dizaines de milliers de tokens à quelques centaines.

**Attention aux tâches en arrière-plan.** Les `/loop` et tâches planifiées renvoient tout le contexte à chaque déclenchement, même quand vous ne faites rien. Coupez-les quand vous n'en avez plus besoin.

## 7. Les erreurs qui ruinent vos tokens

| Erreur | Pourquoi ça coûte cher | La correction |
| --- | --- | --- |
| Garder la même session toute la journée | Chaque message renvoie des heures d'historique | `/clear` à chaque nouvelle tâche |
| Laisser Opus ou Fable par défaut | 2 à 5 fois le prix de Sonnet pour du travail simple | Sonnet par défaut, `/model` pour les cas durs |
| Une demande par micro-modification | Chaque message re-paie tout le contexte | Regrouper les changements dans un seul message |
| « Améliore le projet » | Claude lit tout le dépôt | Nommer le fichier et la fonction |
| Coller 5 000 lignes de logs | Le log reste dans le contexte jusqu'au `/clear` | Coller seulement l'erreur utile |
| Laisser Claude continuer dans la mauvaise direction | Code écrit pour rien, puis à corriger | Échap tout de suite, puis `/rewind` |
| CLAUDE.md de 1 000 lignes | Chargé à chaque requête | Moins de 200 lignes, le reste en skills |
| 15 serveurs MCP actifs | Leurs instructions occupent le contexte | Désactiver les inutiles avec `/mcp` |
| Revenir après une longue pause dans une grosse session | Le cache a expiré, tout est retraité au prix fort | `/compact` avant la pause, ou `/clear` au retour |
| Lancer plusieurs instances en parallèle sans raison | Chaque instance a sa propre facture | Une seule session, sauf vrai besoin |

## 8. Antisèche

À épingler sur le Discord :

- [ ] Je suis sur **Sonnet** par défaut (`/model`)
- [ ] Je fais `/clear` à chaque changement de tâche
- [ ] Je fais `/compact` à un point d'étape dans une longue tâche
- [ ] Je regroupe mes modifications en une seule demande
- [ ] Je cite les fichiers et fonctions concernés
- [ ] J'utilise le plan mode (Shift+Tab) pour les grosses tâches
- [ ] J'appuie sur Échap dès que Claude part dans le mauvais sens
- [ ] Mon CLAUDE.md fait moins de 200 lignes
- [ ] J'ai désactivé les MCP inutiles (`/mcp`)
- [ ] Je vérifie `/usage` et `/context` de temps en temps

Bon dev à tous, et que vos tokens durent jusqu'à la fin de la semaine.

## Sources

- [Claude Code : gérer ses coûts (doc officielle)](https://code.claude.com/docs/en/costs)
- [Tarifs de l'API Claude](https://platform.claude.com/docs/en/about-claude/pricing)
- [Comparatif des prix par modèle](https://claudecoworkcourse.com/ai-api-pricing/claude)
