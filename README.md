# PASSEPAR-4

## Présentation

Ce projet est une adaptation du fameux *Puissance 4* pour le web, étendu à un système plus 'compétitif'. Il est constitué de deux parties distinctes : l'**API**, faite en Python (avec Flask), qui gère toute la partie logistique, base de données, websockets, etc. ; et l'**application** à proprement parler, faite en HTML, CSS, JS (TypeScript), le tout à l'aide de VueJS (framework), qui applique toutes les données fournies par l'API au site pour assurer son bon fonctionnement.

## Installation

### API

Suivez ces étapes pas à pas pour installer l'API.

*Prérequis* : 
- `Python >=3.8` : https://www.python.org/downloads/.
- Ne pas avoir de proxy bloquant activé (type lycée).
- Être administrateur de son ordinateur (en cas de mise sur le réseau).

<hr/>

**Windows** :
```bash
$ python -m venv .venv
$ .venv\Scripts\activate
$ pip install -r requirements.txt
```

**Linux** : 
```bash
$ python3 -m venv .venv
$ . .venv/bin/activate
$ pip install -r requirements.txt
```

<hr/>

Il vous faut ensuite créer un fichier `.env` à la racine du dossier `./api` avec les données suivantes :

```bash
DB_URI=sqlite:///site.db 

SECRET=...
```

- `DB_URI` : Nous recommandons de prendre l'adresse donnée par défaut : bien qu'une adresse MySQL/PostgreSQL soit également valide et fonctionne sans aucun doute, l'API n'a pas été testée pour.

- `SECRET` : Clé secrète de l'application, elle peut par exemple être générée de la maniètre suivante :
```python
import uuid
uuid.uuid4().hex  # --> Exemple : '21aad80a741a42d584fc17729a7b2018'
```

Il reste une dernière étape avant que tout soit prêt à être lancé : (re)initialiser la base de données, à l'aide de la commande suivante : 

```bash
$ python resetdb.py
```

> **Note** : Ce fichier à initialement été fait pour réinitialiser la base de données lors de changements durant le développement, mais peut également servir à initialiser la base de données lors du premier lancement du serveur.

Vous pouvez ensuite lancer l'API (en vérifiant bien que vous êtes dans l'environnement virtuel de l'application, raison pour laquelle la ligne suivante ne change pas entre Windows et Linux) : 
```bash
$ python run.py
```

> **Note** : Par défaut, le serveur ne sera accessible qu'en local ! Pour l'ouvrir à votre réseau, il faudra changer le keyword `host` à `0.0.0.0` dans le fichier `run.py` :
> ```python
> if __name__ == '__main__':
>    # Avant : host = '127.0.0.1'
>    socket.run(app, debug = True, host = '0.0.0.0') 
> ```
> Cela nécessite généralement des *droits administrateurs*.

### Application (VueJS)

*Prérequis* :
- `Node.js >=v16.17.0` (des versions antérieures fonctionnent probablement, mais le projet n'a pas été testé avec ces versions) : https://nodejs.org/en/download.
- `npm >=9.6.0` (livré avec Node.js, vérifier que la version est à jour : '`npm --version`').

Pour installer l'application dans son ensemble (hors-API), il suffit d'éxecuter cette commande (à la racine de `./app`) :
```bash
$ npm install 
```
Cette commande va installer toutes les dépendances du projet dans les bonnes versions, il est alors possible de lancer l'application (en développement) avec la commande suivante :
```bash
$ npm run dev
```
> **Note** : Veillez à ce que l'API soit lancée pour éviter des erreurs de connection dans les outils de développement sur votre navigateur.