# API DOCUMENTATION

## Endpoints

### Games

- `/api/game/new` : [`POST`] Creates a new game record in the database.
- `/api/game/list?onlyids=True` : [`GET`] Returns the list of all currently active games.
- `/api/game/<gamekey>` : [`GET`] Returns informations about a given game.
- `/api/game/<gamekey>/addplayer` : [`POST`] Adds a player with given `player_id` in a game if it isn't full.
    
    - `player_id` : string

- `/api/game/<gamekey>/update?column=` : [`PUT`] Adds a pawn in the given `column` if not full.

    - `column` : integer

- `/api/game/<gamekey>/delete` : [`DELETE`] Deletes the game with id `gamekey` if it exists.

> **Error codes** : 
>
> - `G1` : Maximum number of players reached.
> - `G2` : Game ID doesn't exist.
> - `G3` : No space left on the choosen column.
> - `G4` : Requested player doesn't exist.
> - `G5` : Player is already in a game.
> - `G6` : The choosen column is invalid.

### Players

- `/api/player/register` : [`POST`] Registers a player with its `name`, `email` and `password`. 

    - `name` : string
    - `email` : string
    - `password` : string

- `/api/player/<playerid>` : [`GET`] Returns informations about a given player.
- `/api/player/<playerid>/update` : [`PUT`] Updates a player's informations.

> **Error codes** : 
>
> - `P1` : Player's email (`1`) or name (`2`) already exists in the database.
> - `P2` : Player with given id or email doesn't exist.
> - `P3` : Email entered is not valid (for registration).
> - `P4` : Login failed (incorrect password).