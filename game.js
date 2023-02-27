var game_token = 0
var len = function () {
    return this.length;
};


function generateTable(x, y, matrix) {
    // creates a <table> element and a <tbody> element
    const tbl = document.createElement("table");
    const tblBody = document.createElement("tbody");

    // creating all cells
    for (let i = 0; i < x; i++) {
        // creates a table row
        const row = document.createElement("tr");

        for (let j = 0; j < y; j++) {
            // Create a <td> element and a text node, make the text
            // node the contents of the <td>, and put the <td> at
            // the end of the table row
            const cell = document.createElement("td");
            const cellText = document.createTextNode(matrix[i][j]);
            cell.appendChild(cellText);
            row.appendChild(cell);
        }

        // add the row to the end of the table body
        tblBody.appendChild(row);
    }

    // put the <tbody> in the <table>
    tbl.appendChild(tblBody);
    // appends <table> into <body>
    document.body.appendChild(tbl);
    // sets the border attribute of tbl to '2'
    tbl.setAttribute("border", "2");
}




function create_board(token) {
    let url = 'http://127.0.0.1:5000/api/game/'
    //// API request for the game board => url/api/game/game_id
    fetch(url + token, {
            method: "POST",
            headers: {
                'Content-Type': 'application/json'

            },
        }).then((response) => response.json())
        .then((data) => {
            /// cheking if the player dont tryed to bruteforce the api
            if (token != data.id) {
                alert("Houston we have a problem")
            } else {


                generateTable(data.matrix.length, data.matrix[0].length, data.matrix)


            }
        })
        .catch((error) => {
            console.error('Error:', error);
        });


}


function newgame(url) {
    fetch(url, {
            method: "POST",
            headers: {
                'Content-Type': 'application/json'

            },
        }).then((response) => response.json())
        .then((data) => {
            game_token = data.game_id
            create_board(game_token)
        })
        .catch((error) => {
            console.error('Error:', error);
        });
}


if (confirm('Do you want to start a new game?')) {
    // Star it!
    console.log('Game started');
    newgame("http://127.0.0.1:5000/api/game/new")

} else {
    window.open("./login.html", "Bye")
    console.log('Bye');

}



console.log(game_token)