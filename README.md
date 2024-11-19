# Planificateur d'événements

Par Yoann Dewilde.

Le planificateur est une interface en ligne de commandes. Il permet de créer des événements, de les lister et de voir les conflits.

## Exécution

Pour l'exécuter, aucune librairie externe n'est nécessaire. Il faut exécuter la commande `python main.py`.
L'interface suivante s'affiche, demandant l'action :

```
Veuillez saisir une action
1. Lister evenements
2. Ajouter evenement
3. Quitter
```

Voici une liste d'événements, dont certains sont en conflit :
```
- e0, de 11:00 a 12:00
- [CONFLIT] e1, de 12:00 a 13:00
- [CONFLIT] e2, de 12:30 a 13:30
- [CONFLIT] e3, de 15:00 a 15:30
```

## Exécuter les tests

La commande pour lancer tous les tests est :

```sh
python -m unittest tests
```

## Fonctionnement

La liste est triée à chaque appel à `add_event`, car le nouvel événement est inséré au bon endroit.
Donc `list_events` retourne la liste telle quelle.

L'affichage des événements en conflit est effectué grâce à un booléen stocké dans `Event`. Donc `find_conflicts` n'est pas appelé.