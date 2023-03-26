// MODELS INTERFACES

interface Trophy {
    id: string,
    title: string,
    description: string
}

interface Player {
    id: string,
    name: string,
    avatar_url: string,
    email: string,
    anonymized_email: string,
    score: number,
    trophies: Trophy[],
    current_game: Game
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

export type { Trophy, Player, Game }