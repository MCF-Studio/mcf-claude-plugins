# redaction-ste100

Le skill `ste100` fait rédiger Claude selon les règles de la norme **ASD-STE100** (Simplified Technical English),
la norme de rédaction technique de l'aéronautique : vocabulaire simple et constant, phrases courtes, voix active,
une instruction par phrase. Résultat : des réponses sans ambiguïté, faciles à suivre et à traduire.

Il ne se lance **que sur demande** (jamais automatiquement).

## Utilisation

| Commande | Effet |
| --- | --- |
| `/redaction-ste100:ste100` | Active le mode : les réponses suivantes suivent les règles STE, dans la langue de l'utilisateur |
| `/redaction-ste100:ste100 en` | Anglais STE strict (dictionnaire STE compris) |
| `/redaction-ste100:ste100 de` | Force une langue (`fr`, `de`, `es`…) |
| `/redaction-ste100:ste100 check <texte>` | Réécrit un texte selon STE et liste les écarts corrigés, sans activer le mode |
| `/redaction-ste100:ste100 off` | Retour au style normal |

Le code, les commandes, les chemins et les citations ne sont jamais modifiés.

## Exemple

Avant :
> Il est recommandé de procéder à une sauvegarde de la base de données préalablement à l'exécution de la
> migration, faute de quoi une perte de données pourrait éventuellement survenir.

Après (`ste100`) :
> ATTENTION : Sauvegarder la base de données avant la migration. Sinon, des données peuvent être perdues.

## Limites

Le dictionnaire officiel ASD-STE100 (environ 900 mots approuvés) n'est pas inclus : le skill s'appuie sur les
règles de rédaction et une liste de substitutions courantes. Le résultat est proche de la norme, mais **non
certifié**. Pour une documentation contractuelle, faire valider le texte par un vérificateur STE. La
spécification officielle est disponible gratuitement sur demande auprès de l'ASD. Dans une autre langue que
l'anglais, le skill applique les règles d'écriture de la norme et transpose le principe du dictionnaire.

ASD-STE100 est une norme de l'ASD (AeroSpace and Defence Industries Association of Europe). Ce plugin résume
ses règles avec ses propres mots et n'est pas affilié à l'ASD.

Aucun hook, aucun script, aucun accès réseau.
