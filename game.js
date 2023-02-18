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
    }).then(res => {
        console.log("Request complete! response:", res);
    });
}

post("http://127.0.0.1:5000/api/game/new")