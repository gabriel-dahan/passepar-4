# DOCUMENTATION

## Endpoints

### - **`/api/game`**

- `/new` : [`POST`] Creates a new game record in the database.
- `/list?onlyids=True` : [`GET`] Returns the list of all currently active games.
- `/<gamekey>` : [`GET`] Returns informations about a given game.
- `/<gamekey>/addplayer` : [`POST`] Adds a player with given `id` in a game if it isn't full.
    
    - `player_id` : string

- `/<gamekey>/update?column=` : [`PUT`] Adds a poon in the given `column` if not full.

    - `column` : integer

- `/<gamekey>/delete` : [`DELETE`] Deletes the game with id `gamekey` if it exists.

> **Error codes** : 
>
> - `G1` : Maximum number of players reached.
> - `G2` : Game ID doesn't exist.
> - `G3` : No space left on the choosen column.
> - `G4` : Requested player doesn't exist.
> - `G5` : Player is already in a game.
> - `G6` : The choosen column isn't valid.

### - **`/api/players`**

- `/register` : [`POST`] Registers a player with its `name`, `email` and `password`. 

    - `name` : string
    - `email` : string
    - `password` : string

- `/<playerid>` : [`GET`] Returns informations about a given player.
- `/<playerid>/update` : [`PUT`] Updates a player's informations.

> **Error codes** : 
>
> - `P1-1` or `P1-2` : Player's email (`1`) or name (`2`) already exists in the database.
> - `P2` : ...
> - `P3` : ...
> - `P4` : ...