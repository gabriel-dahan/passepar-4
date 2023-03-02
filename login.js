console.log("linked");


function submitData(objButton) {

    const formData = new FormData()
    url = 'http://51.83.73.242:1102/api/players/register'
    nom = document.getElementById('name1').value;
    email = document.getElementById('email1').value;
    psd = document.getElementById('msg1').value;
    formData.append("username" = nom);
    formData.append("email" = email);
    formData.append("password" = psd);
    console.log(formData);
    const request = new XMLHttpRequest();
    request.open("POST", url);
    request.send(formData);
}