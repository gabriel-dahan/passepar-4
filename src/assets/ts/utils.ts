import type { Ref } from "vue";
import type { User } from "./interfaces";

const APP_NAME = 'PASSEPAR-4'

const matrixAsColumns = (matrix: number[][]) => {
    let newMatrix = [];
    for (let j = 0; j < 7; j++) {
        let column: number[] = [];
        for (let i = 0; i < matrix.length; i++) {
            column.push(matrix[i][j]);
        }
        newMatrix.push(column);
    }
    return newMatrix
};

const loadCurrentUser = async (promisedUser: Promise<User> | Promise<null> | undefined, ref: Ref) => {
    let user = await promisedUser;
    if(user !== undefined)
        ref.value = user as User;
    else
        console.error('Current user cannot be loaded.')
};

export { matrixAsColumns, APP_NAME, loadCurrentUser };