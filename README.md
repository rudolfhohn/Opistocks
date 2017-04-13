# Opistocks

## Description / Objectifs
Cette application a pour objectif d'observer visuellement la correlation entre le cours d'un indice boursier et le sentiment de l'entreprise sur les réseaux sociaux.

## Collection / Source de données
Pour avoir accès aux indices boursiers, nous utilisons [l'API de Yahoo Finance](https://pypi.python.org/pypi/yahoo-finance/1.1.4). Pour un indice donné, elle retourne l'évolution du taux dans un laps de temps choisi. Concernant les réseaux sociaux, nous utilisons [l'API Twitter](https://dev.twitter.com/overview/api). En effet, elle permet d'obtenir les tweets de la dernière semaine.

## Techniques d'analyse envisagées
L'analyse du sentiment des tweets se fait en deux phases. La première phase consiste à détecter les 10 tags les plus fréquents (Information Retrieval) dans la série de tweets, en relation avec l'indice.
La deuxième phase consiste à récupérer tous les tweets contenant les 10 tags détectés précédemment et les classifier à l'aide de techinques d'apprentissage statistiques (Machine Learning). Nous entraînons le classifieur sur un jeu de tweets déjà classifiés (training set) que nous trouvons sur [Crowdflower](https://www.crowdflower.com/data-for-everyone/).
