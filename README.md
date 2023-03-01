# Connect Four - WEB Game

## PRESENTATION

This project is an adaptation of the famous game *Connect Four* for the web, with accounts, and competition ! It contains two distincts parts : the [API](./api/), made with *Python* (using Flask) ; and the FrontEnd, made with *HTML, CSS, JavaScript*, making use of the API.

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

API Endpoints & error codes : [here](./DOC.md)