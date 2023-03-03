const HOST = '127.0.0.1';
const PORT = 5000
const API_BASE = `http://${HOST}:${PORT}/api`;

const __format_data = (payload) => {
    let formData = new FormData();
    for (const [key, value] of Object.entries(payload))
        formData.append(key, value);
    return formData
}

class Players {
    constructor() {
        this.endpoint = API_BASE + '/player';
    }


    register(name_, email, password) {
        let payload = {
            name: name_,
            email: email,
            password: password
        };
        
        return fetch(`${this.endpoint}/register`, {
            method: "POST",
            body: __format_data(payload)
        }).then((res) => res.json());
    }

    login(email, password) {
        let payload = {
            email: email,
            password: password
        };
        
        return fetch(`${this.endpoint}/login`, {
            method: "POST",
            body: __format_data(payload)
        }).then((res) => res.json());
    }

    search(name_ = '', email = '', limit = 10) {
        let params = `?name=${name_}&email=${email}&limit=${limit}`;
        return fetch(`${this.endpoint}/search${params}`, {
            method: "GET",
            headers: {
                'Content-Type': 'application/json'
            },
        }).then((res) => res.json());
    }

    get(id) {
        return fetch(`${this.endpoint}/${id}`, {
            method: "GET",
            headers: { 
                'Content-Type': 'application/json' 
            },
        }).then((res) => res.json());
    }

    update(id, name_ = null, email = null, password = null, score = null) {
        let payload = { 
            name: name_,
            email: email,
            password: password,
            score: score
        };

        return fetch(`${this.endpoint}/${id}/update`, {
            method: "PUT",
            body: __format_data(payload)
        }).then((res) => res.json());
    }

}

class Games {

    constructor() {
        this.endpoint = API_BASE + '/game';
    }

    new() {
        return fetch(`${this.endpoint}/new`, {
            method: "POST"
        }).then((res) => res.json());
    }

    list(onlyIds = false) {
        onlyIds = 'True' ? onlyIds : 'False';
        return fetch(`${this.endpoint}/list?onlyids=${onlyIds}`, {
            method: "GET",
            headers: { 
                'Content-Type': 'application/json' 
            },
        }).then((res) => res.json());
    }

    get(gameKey) {
        return fetch(`${this.endpoint}/${gameKey}`, {
            method: "GET",
            headers: { 
                'Content-Type': 'application/json' 
            },
        }).then((res) => res.json());
    }

    addplayer(gameKey, playerId) {
        let payload = { 
            player_id: playerId
        };

        return fetch(`${this.endpoint}/${gameKey}/addplayer`, {
            method: "POST",
            body: __format_data(payload)
        }).then((res) => res.json());
    }

    play(gameKey, column) {
        let payload = { 
            column: column
        };

        return fetch(`${this.endpoint}/${gameKey}/play`, {
            method: "PUT",
            body: __format_data(payload)
        }).then((res) => res.json());
    }

    delete(gameKey) {
        return fetch(`${this.endpoint}/${gameKey}/delete`, {
            method: "DELETE",
            body: __format_data(payload)
        }).then((res) => res.json());
    }
}

const Connect4API = {
    'players': new Players(),
    'games': new Games()
}

// Connect4API.players.register(name_ = 'TestUser', email = 'test@user.com', password = '1234')
//     .then((data) => console.log(data));