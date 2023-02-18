console.log(
    "Loaded"
)




/* fetch("http://127.0.0.1:5000/api/game/new", {
    method: "POST",
    headers: {
        'Content-Type': 'application/json'
    },
}).then(res => {
    console.log("Request complete! response:", res);
}); */

function post(url) {
    fetch(url, {
            method: "POST",
            headers: {
                'Content-Type': 'application/json'

            },
        }).then((response) => response.json())
        .then((data) => {
            console.log(data)
            return (data)
        })
        .catch((error) => {
            console.error('Error:', error);
        });
}


console.log(post("http://127.0.0.1:5000/api/game/new"))