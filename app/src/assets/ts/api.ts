import _ from 'lodash';
import axios from 'axios';

const API_BASE = `/api`;

const ERR_CODES = {
    // -- See error codes : https://github.com/gabriel-dahan/connect4-game/blob/main/api/README.md --

    G1: false,
    G2: false,
    G3: false,
    G4: false,
    G5: false,
    G6: false,

    U1: {
        S1: false,
        S2: false
    },
    U2: false,
    U3: false,
    U4: false,
    U5: false,
    U6: false
}

const getRawErrs = () => {
    return _.cloneDeep({
        ...ERR_CODES,
        noMatch: false // In case passwords do not match.
    })
}

const updateErrs = (ref: any, data: any) => {
    const errCode = data.code;
    const errSubCode = data.subcode;
    if(Object.keys(ref.value).includes(errCode) && errSubCode == undefined)
        ref.value[errCode] = true;
    else if(errSubCode)
        ref.value[errCode][errSubCode] = true;
}

const __formatData = (payload: any) => {
    let formData = new FormData();
    for (const [key, value] of Object.entries(payload))
        formData.append(key, value as any);
    return formData
}

const __get = (endpoint: string) => {
    return axios.get(endpoint, {
        headers: {
            'Content-Type': 'application/json'
        },
    });
}

const __post = (endpoint: string, payload = {}) => {
    return axios.post(endpoint, __formatData(payload), {
        headers: {
            'Content-Type': 'multipart/form-data'
        } 
    });
}

const __put = (endpoint: string, payload = {}) => {
    return axios.put(endpoint, __formatData(payload), {
        headers: {
            'Content-Type': 'multipart/form-data'
        } 
    });
}

const __delete = (endpoint:string) => { 
    return axios.delete(endpoint);
}

class Users {
    endpoint: string;

    constructor() {
        this.endpoint = API_BASE + '/user';
    }

    async all() {
        return __get(`${this.endpoint}/all`).then(res => res.data);
    }

    async register(name_: string, email: string, password: string) {
        return __post(`${this.endpoint}/register`, {
            name: name_,
            email: email,
            password: password
        }, ).then(res => res.data);
    }

    async login(email: string, password: string) {
        return __post(`${this.endpoint}/login`, {
            email: email,
            password: password
        }).then(res => res.data);
    }

    async search(name_ = '', email = '', limit = 10) {
        let params = `?name=${name_}&email=${email}&limit=${limit}`;
        return __get(`${this.endpoint}/search${params}`)
            .then(res => res.data);
    }

    async get(id: string) {
        return __get(`${this.endpoint}/${id}`)
            .then(res => res.data);
    }

    async from_session(token: string) {
        return __get(`${this.endpoint}/token/${token}`)
            .then(res => res.data);
    }

    async delete_session(token: string) {
        return __delete(`${this.endpoint}/token/${token}/delete`)
            .then(res => res.data);
    }

    async update(id: string, name_: string | null = null, email: string | null = null, password: string | null = null, score: number | null = null) {
        return __put(`${this.endpoint}/${id}/update`, { 
            name: name_,
            email: email,
            password: password,
            score: score
        }).then(res => res.data);
    }

    async add_score(id: string, score: number) {
        return __put(`${this.endpoint}/${id}/addscore`, {
            score: score
        }).then(res => res.data);
    }
}

class Games {
    endpoint: string;

    constructor() {
        this.endpoint = API_BASE + '/game';
    }

    async new(public_: boolean, ownerId: string) {
        return __post(`${this.endpoint}/new`, {
            public: public_,
            owner_id: ownerId
        }).then(res => res.data);
    }

    async list(onlyIds = false, onlyPublic = false) {
        let onlyIdsStr = onlyIds ? 'true' : 'false';
        return __get(`${this.endpoint}/list?only_ids=${onlyIdsStr}&only_public=${onlyPublic}`)
            .then(res => res.data);
    }

    async get(gameKey: string) {
        return __get(`${this.endpoint}/${gameKey}`)
            .then(res => res.data);
    }

    async addplayer(gameKey: string, color: number, userId: string | null = null) {
        /* userId is null when the player added is a guest (no-user). */
        return __post(`${this.endpoint}/${gameKey}/addplayer`, { 
            user_id: userId,
            color: color
        }).then(res => res.data);
    }

    async play(gameKey: string, column: string) {
        return __put(`${this.endpoint}/${gameKey}/play`, { 
            column: column
        }).then(res => res.data);
    }

    async delete(gameKey: string) {
        return __delete(`${this.endpoint}/${gameKey}/delete`)
            .then(res => res.data);
    }
}

const API = {
    'users': new Users(),
    'games': new Games()
}

export { API, getRawErrs, updateErrs };