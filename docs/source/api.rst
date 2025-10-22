API Documentation
=================

Le système utilise Django REST Framework (DRF) pour l'API. La documentation interactive est disponible via drf-yasg.

Endpoints Principaux
--------------------

Events
~~~~~~

- **GET /api/events/** : Liste des événements
- **POST /api/events/** : Créer un événement
- **GET /api/events/{id}/** : Détails d'un événement
- **PUT /api/events/{id}/** : Modifier un événement
- **DELETE /api/events/{id}/** : Supprimer un événement

Tickets
~~~~~~~

- **GET /api/tickets/** : Liste des tickets
- **POST /api/tickets/** : Créer un ticket
- **GET /api/tickets/{id}/** : Détails d'un ticket
- **PUT /api/tickets/{id}/** : Modifier un ticket
- **DELETE /api/tickets/{id}/** : Supprimer un ticket

Users
~~~~~

- **GET /api/users/** : Liste des utilisateurs
- **POST /api/users/** : Créer un utilisateur
- **GET /api/users/{id}/** : Détails d'un utilisateur
- **PUT /api/users/{id}/** : Modifier un utilisateur
- **DELETE /api/users/{id}/** : Supprimer un utilisateur

Halls
~~~~~

- **GET /api/halls/** : Liste des salles
- **POST /api/halls/** : Créer une salle
- **GET /api/halls/{id}/** : Détails d'une salle
- **PUT /api/halls/{id}/** : Modifier une salle
- **DELETE /api/halls/{id}/** : Supprimer une salle

Authentification
----------------

L'API utilise JWT pour l'authentification via dj-rest-auth.

- **POST /api/auth/login/** : Connexion
- **POST /api/auth/logout/** : Déconnexion
- **POST /api/auth/token/refresh/** : Rafraîchir le token

Recherche
---------

Elasticsearch est utilisé pour la recherche avancée.

- **GET /api/search/** : Recherche dans les événements et tickets

Documentation Interactive
-------------------------

Accédez à la documentation Swagger ou Redoc à l'adresse suivante une fois l'application lancée :

- Swagger UI : http://localhost/swagger/
- Redoc : http://localhost/redoc/

Exemples d'Utilisation
----------------------

Créer un événement :

.. code-block:: bash

   curl -X POST http://localhost/api/events/ \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer <token>" \
     -d '{"title": "Concert", "description": "Un concert", "date": "2025-01-01"}'

Lister les tickets :

.. code-block:: bash

   curl -X GET http://localhost/api/tickets/ \
     -H "Authorization: Bearer <token>"
