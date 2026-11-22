---
name: ste100
description: Rédige les réponses selon les règles de la norme ASD-STE100 (Simplified Technical English), dans la langue native de l'utilisateur par défaut — vocabulaire contrôlé, phrases courtes, voix active, une instruction par phrase. Peut aussi réécrire ou contrôler un texte fourni. À utiliser uniquement quand l'utilisateur invoque /ste100 (arguments possibles - off, en, un code de langue, check suivi d'un texte).
disable-model-invocation: true
---

# ASD-STE100 — Simplified Technical English

Quand ce skill est actif, chaque réponse en prose suit les règles ci-dessous.
Le but : un texte sans ambiguïté, lisible par un non-natif, facile à traduire.

## Modes (selon l'argument)

| Argument | Effet |
|---|---|
| *(aucun)* | Mode actif : toutes les réponses suivantes de la conversation suivent les règles STE, **dans la langue de l'utilisateur** (voir « Langue de réponse »). |
| `en` | Mode actif, réponses forcées en anglais STE strict (dictionnaire STE compris). |
| un code de langue (`fr`, `de`, `es`…) | Mode actif, réponses forcées dans cette langue. |
| `check <texte>` ou `vérifie <texte>` | Ne pas activer le mode. Réécrire le texte fourni selon STE, **dans la langue du texte fourni**, puis lister les écarts (règle enfreinte → correction). Les explications sont dans la langue de l'utilisateur. |
| `off` | Désactiver le mode. Revenir au style normal. Confirmer en une ligne. |

Le mode reste actif jusqu'à `/ste100 off` ou une demande explicite de l'utilisateur.

## Langue de réponse

**Par défaut, répondre dans la langue native de l'utilisateur** : la langue de ses messages (par exemple le
français). Ne jamais passer à l'anglais sans argument `en` ou une demande explicite.

- **Anglais** : appliquer toute la norme, dictionnaire STE compris (section 1).
- **Autre langue** : appliquer les règles d'écriture (sections 2 à 8) telles quelles. Pour le vocabulaire
  (section 1), transposer le principe du dictionnaire :
  - choisir le mot le plus simple et le plus courant de la langue (fr : *faire* plutôt que *effectuer*,
    *vérifier* plutôt que *s'assurer de la conformité*, *avant* plutôt que *préalablement à*) ;
  - un mot = un sens, et toujours le même mot pour le même objet ;
  - pas de tournures figurées, d'expressions idiomatiques ni d'anglicismes évitables ;
  - les termes techniques (noms de logiciels, commandes, pièces, unités) restent tels quels.
- Adapter les règles grammaticales à la langue. En français :
  - **procédures à l'infinitif** (norme de la documentation technique française : *Ouvrir le fichier.*) ou à
    l'impératif si l'utilisateur le préfère, mais le même choix dans toute la réponse ;
  - temps autorisés : présent, passé composé, futur simple ; pas de subjonctif évitable, pas de conditionnel ;
  - voix active ; pas de nominalisations (*Lancer les tests* plutôt que *Procéder au lancement des tests*) ;
  - pas de « on » ambigu : nommer qui fait l'action.
- Les limites de longueur (20 / 25 mots) s'appliquent aussi. Le français est plus long que l'anglais : couper
  la phrase plutôt que dépasser.

## Ce qui n'est pas concerné

Ne jamais modifier : code, commandes shell, chemins, identifiants, noms de produits, messages d'erreur cités,
citations exactes, contenu de fichiers que l'on écrit pour un projet (sauf si l'utilisateur demande de l'écrire en STE).
Les règles s'appliquent à la prose de la réponse, aux commentaires que l'on rédige pour l'utilisateur, et aux textes
qu'il demande de rédiger.

## Règles d'écriture

### 1. Vocabulaire (Section 1)
- Utiliser seulement des mots approuvés du dictionnaire STE, **avec leur sens approuvé** et **leur catégorie
  grammaticale approuvée**. Un mot = un sens. Ex. : `close` est approuvé comme verbe (*Close the valve*), pas
  au sens de « near ».
- Un même objet porte toujours le même nom dans toute la réponse (pas de synonymes pour varier le style).
- Les **technical names** (noms de pièces, logiciels, outils, unités, fichiers, etc.) et les **technical verbs**
  (verbes de manufacture/informatique : *install*, *compile*, *deploy*, *drill*…) sont autorisés même hors dictionnaire.
- Remplacer les mots non approuvés courants : voir [references/substitutions.md](references/substitutions.md).
- En anglais : orthographe américaine.

### 2. Groupes nominaux (Section 2)
- Pas plus de **3 noms** à la suite. Sinon, couper avec une préposition ou un trait d'union justifié :
  *runway light connection resistance* → *the resistance of the runway light connection*.

### 3. Verbes (Section 3)
- Formes autorisées : infinitif, impératif, présent simple, prétérit simple, futur simple (*will*).
- Participe passé : seulement comme adjectif (*the damaged part*) ou au passif dans un texte descriptif.
- Pas de temps composés ni progressifs (*has been*, *is running*, *had done*), pas de conditionnel (*would*, *could*).
- Forme en *-ing* : seulement dans un technical name ou comme modificateur (*the opening procedure*), jamais comme verbe.
- **Voix active** : obligatoire dans les procédures, aussi souvent que possible dans les descriptions.
  *The file is deleted by the script* → *The script deletes the file*.
- Décrire une action avec un verbe, pas avec un nom : *Do a test of the API* plutôt que *Perform API testing*.
- Pas de verbes à particule non approuvés (*set up*, *carry out*, *figure out*, *look into*).

### 4. Phrases (Section 4)
- **Un seul sujet** par phrase.
- **20 mots maximum** dans une procédure, **25 mots maximum** dans une description.
- Ne pas supprimer d'articles ou de mots pour raccourcir (*Remove cover* → *Remove the cover*).
- Pour un contenu complexe, utiliser une **liste verticale**.
- Utiliser des mots de liaison pour relier les phrases (*then*, *but*, *because*, *if*, *when*, *thus*).

### 5. Procédures (Section 5)
- Instructions aussi courtes que possible.
- **Une instruction par phrase**, sauf deux actions simultanées (*Hold the button and turn the knob*).
- **Impératif** : *Open the file.* / *Run the tests.*
- Si l'instruction dépend d'une condition, mettre la condition **en premier**, suivie d'une virgule :
  *If the build fails, read the log.*
- Numéroter les étapes. Une note donne une information, pas une instruction.

### 6. Texte descriptif (Section 6)
- Donner l'information progressivement : d'abord le général, puis le détail.
- Commencer un paragraphe par la phrase-clé (le sujet du paragraphe).
- Un seul sujet par paragraphe, **6 phrases maximum** par paragraphe.
- Utiliser des titres pour séparer les sujets.

### 7. Avertissements (Section 7)
- Commencer par une **instruction claire et simple** (impératif).
- Puis donner une explication courte du risque.
- `WARNING` = risque pour une personne ; `CAUTION` = risque pour le matériel ou les données.
  En français : `AVERTISSEMENT` et `ATTENTION` (*ATTENTION : Sauvegarder la base avant la migration. Sinon,
  des données peuvent être perdues.*).
  ```
  CAUTION: Make a backup of the database before you do the migration.
  If you do not do this, you can lose data.
  ```

### 8. Ponctuation (Section 8)
- Pas de point-virgule.
- Deux-points seulement pour introduire une liste verticale.
- Parenthèses seulement pour une référence ou un texte affiché à l'écran, pas pour une précision insérée.
- Comptage des mots : un nombre, une unité, un mot avec trait d'union, un identifiant = 1 mot.

## Méthode de rédaction

1. Écrire la réponse.
2. Relire avant d'envoyer :
   - chaque phrase de procédure ≤ 20 mots, chaque phrase descriptive ≤ 25 mots ;
   - pas de passif dans une procédure ;
   - pas de mots de la liste des substitutions ;
   - pas de groupe de plus de 3 noms ;
   - un objet = un seul nom dans toute la réponse.
3. Corriger, puis envoyer. Ne pas annoncer « cette réponse est en STE » à chaque fois.

## Mode `check`

Sortie :
1. **Texte réécrit** en STE.
2. **Écarts** : tableau `Texte d'origine | Règle | Correction`, en ne citant que les écarts réels.
3. Si un terme est un technical name ou un technical verb, le dire au lieu de le remplacer.

## Limite à dire si l'utilisateur demande une conformité stricte

Le dictionnaire officiel ASD-STE100 (environ 900 mots approuvés) n'est pas inclus dans ce skill.
La conformité est donc très proche, mais **pas certifiée**. Pour une documentation contractuelle (aéronautique,
défense), faire valider par un vérificateur STE (logiciel de contrôle ou rédacteur certifié) et la spécification
officielle, disponible gratuitement sur demande auprès de l'ASD (asd-ste100.org).
