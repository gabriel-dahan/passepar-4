function submitData(objButton) {
    url = '/api/players/register'
    nom = document.getElementById('name1').value;
    email = document.getElementById('email1').value;
    msg = document.getElementById('msg1').value;
    console.log(nom, email, msg)
    data = nom, email, msg
    postdata(url, data)
}





function postdata(url, obj) {
    fetch(url + obj, {
            method: "POST",
            headers: {
                'Content-Type': 'application/json'

            },
        }).then((response) => response.json())
        .then((data) => {
            console.log(data)
        })
        .catch((error) => {
            console.error('Error:', error);
        });
}