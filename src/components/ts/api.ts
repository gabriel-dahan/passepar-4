const HOST = '127.0.0.1';
const PORT = 5000
const API_BASE = `http://${HOST}:${PORT}/api`;

const __formatData = (payload) => {
    let formData = new FormData();
    for (const [key, value] of Object.entries(payload))
        formData.append(key, value);
    return formData
}

const __get = (endpoint) => {
    return fetch(endpoint, {
        method: "GET",
        headers: {
            'Content-Type': 'application/json'
        },
    });
}

const __post = (endpoint, payload = null, method = 'POST') => {
    return fetch(endpoint, {
        method: method,
        body: payload ? __formatData(payload) : payload
    });
}

const __put = (endpoint, payload = null) => __post(endpoint, payload, 'PUT');

const __delete = (endpoint, payload = null) => __post(endpoint, payload, 'DELETE');

class Players {
    constructor() {
        this.endpoint = API_BASE + '/player';
    }

    async register(name_, email, password) {
        return __post(`${this.endpoint}/register`, {
            name: name_,
            email: email,
            password: password
        }).then(res => res.json());
    }

    async login(email, password) {
        return __post(`${this.endpoint}/login`, {
            email: email,
            password: password
        }).then(res => res.json());
    }

    async search(name_ = '', email = '', limit = 10) {
        let params = `?name=${name_}&email=${email}&limit=${limit}`;
        return __get(`${this.endpoint}/search${params}`)
            .then(res => res.json());
    }

    async get(id) {
        return __get(`${this.endpoint}/${id}`)
            .then(res => res.json());
    }

    async update(id, name_ = null, email = null, password = null, score = null) {
        return __put(`${this.endpoint}/${id}/update`, { 
            name: name_,
            email: email,
            password: password,
            score: score
        }).then(res => res.json());
    }

}

class Games {

    constructor() {
        this.endpoint = API_BASE + '/game';
    }

    async new() {
        return __post(`${this.endpoint}/new`)
            .then(res => res.json());
    }

    async list(onlyIds = false) {
        onlyIds = 'True' ? onlyIds : 'False';
        return __get(`${this.endpoint}/list?onlyids=${onlyIds}`)
            .then(res => res.json());
    }

    async get(gameKey) {
        return __get(`${this.endpoint}/${gameKey}`)
            .then(res => res.json());
    }

    async addplayer(gameKey, playerId) {
        return __post(`${this.endpoint}/${gameKey}/addplayer`, { 
            player_id: playerId
        }).then(res => res.json());
    }

    async play(gameKey, column) {
        return __put(`${this.endpoint}/${gameKey}/play`, { 
            column: column
        }).then(res => res.json());
    }

    async delete(gameKey) {
        return __delete(`${this.endpoint}/${gameKey}/delete`)
            .then(res => res.json());
    }
}

const Connect4API = {
    'players': new Players(),
    'games': new Games()
}

