# Connect Four - WEB Game
## INSTALL

To install the project : 
```bash
$ python -m venv .venv
$ . .venv/Scripts/activate
$ pip install -r requirements.txt
```

Then, you can add a `.env` file with the following values :
```config
DB_URI=sqlite:///site.db

SECRET=...
```

Endpoints & error codes : 
```markdown
/api/game/... - Error codes : 
    - G1 : invalid coordinates
    - G2 : game id doesn't exist
    - G3 : no space left on the choosen column
    - G4 : max number of players reached (2)

/api/players/... - Error codes :
    - U1 : ...
    - U2 : ...
    - U3 : ...
    - U4 : ...
```