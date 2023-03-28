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
    avatar_url: string,
    email: string,
    anonymized_email: string,
    score: number
}

interface Game {
    id: string,
    matrix: number[][],
    turn: boolean,
    players: Player[],
    status: number,
    created_at: Date,
    public: boolean
}

export type { User, Player, Game }