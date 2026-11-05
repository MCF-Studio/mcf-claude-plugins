# Sécurité

## Pourquoi c'est important

Installer un plugin Claude Code revient à donner à Claude des instructions (skills, agents) et, parfois, à faire
exécuter du code sur sa machine (hooks, scripts, serveurs MCP). Un catalogue public est donc une cible.

## Qui peut faire quoi

| Rôle | Droits |
| --- | --- |
| Membre / visiteur | Lire, installer, ouvrir des issues, proposer des pull requests depuis un fork |
| Relecteur de l'équipe MCF Studio | Relire et approuver les pull requests |
| Mainteneur (propriétaire du dépôt) | Fusionner dans `main`, publier, retirer un plugin |

La branche `main` est protégée : pas de push direct, fusion uniquement par pull request approuvée, vérification
automatique (`tools/validate.py`) obligatoire.

## Menaces et mesures

| Menace | Mesure |
| --- | --- |
| Code malveillant dans un hook ou un script | Relecture ligne à ligne de chaque PR ; hooks relus par deux personnes ; pas de binaire ni d'archive ; pas de téléchargement à l'exécution |
| Instructions piégées dans un skill (faire lire / envoyer des fichiers, désactiver des protections) | Relecture du texte des skills et agents comme du code ; tout envoi de données hors de la machine doit être explicite et documenté |
| Fuite de secret dans une contribution | Vérification automatique des motifs de secrets (webhooks, clés, jetons) sur chaque PR ; règle « aucun secret » |
| Serveur MCP distant qui aspire des données | Serveurs MCP distants refusés sauf opérateur connu et documenté |
| Prise de contrôle du dépôt | Branche protégée, 2FA exigée pour tout compte ayant des droits d'écriture, CODEOWNERS sur les fichiers sensibles |
| Plugin abandonné qui devient dangereux | Un plugin peut être retiré du catalogue à tout moment par les mainteneurs |

## Signaler une faille

Ne pas ouvrir d'issue publique. Utiliser **Security > Report a vulnerability** sur GitHub (signalement privé), ou
contacter l'équipe MCF Studio en message privé sur le Discord. Nous retirons d'abord le plugin concerné, puis
corrigeons.

## Conseil aux utilisateurs

Avant d'installer : `claude plugin details <plugin>@mcf-studio` et lire les fichiers du plugin, surtout `hooks/`
et les scripts. Installer seulement ce dont vous avez besoin.
