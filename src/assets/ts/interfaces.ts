// MODELS INTERFACES

interface Player {
    id: string,
    color: number,
    user: User,
    game: Game
}

interface User {
    id: string,
    name: string,
    short_name: string,
    avatar_url: string,
    email: string,
    anonymized_email: string,
    score: number,
    game_id: string
}

interface Game {
    id: string,
    matrix: number[][],
    turn: number,
    players: Player[],
    status: number,
    created_at: Date,
    public: boolean,
    owner: User
}

export type { User, Player, Game }