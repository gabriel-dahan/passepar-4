const matrixAsColumns = (matrix: any[][]) => {
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

export { matrixAsColumns, };