const HOST = '127.0.0.1' //'51.83.73.242';
const PORT = 5000 //1102;
const API_BASE = `http://${HOST}:${PORT}/api`;

const __formatData = (payload: any) => {
    let formData = new FormData();
    for (const [key, value] of Object.entries(payload))
        formData.append(key, value as any);
    return formData
}

const __get = (endpoint: string) => {
    return fetch(endpoint, {
        method: "GET",
        headers: {
            'Content-Type': 'application/json'
        },
    });
}

const __post = (endpoint: string, payload = {}, method = 'POST') => {
    return fetch(endpoint, {
        method: method,
        body: __formatData(payload)
    });
}

const __put = (endpoint: string, payload = {}) => __post(endpoint, payload, 'PUT');

const __delete = (endpoint:string, payload = {}) => __post(endpoint, payload, 'DELETE');

class Players {
    endpoint: string;

    constructor() {
        this.endpoint = API_BASE + '/player';
    }

    async register(name_: string, email: string, password: string) {
        return __post(`${this.endpoint}/register`, {
            name: name_,
            email: email,
            password: password
        }).then(res => res.json());
    }

    async login(email: string, password: string) {
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

    async get(id: string) {
        return __get(`${this.endpoint}/${id}`)
            .then(res => res.json());
    }

    async from_session(token: string) {
        return __get(`${this.endpoint}/token/${token}`)
            .then(res => res.json());
    }

    async update(id: string, name_ = null, email = null, password = null, score = null) {
        return __put(`${this.endpoint}/${id}/update`, { 
            name: name_,
            email: email,
            password: password,
            score: score
        }).then(res => res.json());
    }

}

class Games {
    endpoint: string;

    constructor() {
        this.endpoint = API_BASE + '/game';
    }

    async new(public_: boolean) {
        return __post(`${this.endpoint}/new`, {
            public: public_
        }).then(res => res.json());
    }

    async list(onlyIds = false, onlyPublic = false) {
        let onlyIdsStr = onlyIds ? 'true' : 'false';
        return __get(`${this.endpoint}/list?only_ids=${onlyIdsStr}&only_public=${onlyPublic}`)
            .then(res => res.json());
    }

    async get(gameKey: string) {
        return __get(`${this.endpoint}/${gameKey}`)
            .then(res => res.json());
    }

    async addplayer(gameKey: string, playerId: string) {
        return __post(`${this.endpoint}/${gameKey}/addplayer`, { 
            player_id: playerId
        }).then(res => res.json());
    }

    async play(gameKey: string, column: string) {
        return __put(`${this.endpoint}/${gameKey}/play`, { 
            column: column
        }).then(res => res.json());
    }

    async delete(gameKey: string) {
        return __delete(`${this.endpoint}/${gameKey}/delete`)
            .then(res => res.json());
    }
}

const Connect4API = {
    'players': new Players(),
    'games': new Games()
}

export { Connect4API };