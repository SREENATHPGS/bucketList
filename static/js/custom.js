function getBucketListItems( account_id, auth ) {
    xOb.getData("wish", {"Content-Type":"application/json"},[],updateFeed)
}

function updateFeed(resp) {
    let list_items = JSON.parse(resp);
    for (let i=0; i<list_items.length; i++) {
        let middle_panel = document.getElementById("middle_panel");

        let feed_div = document.createElement('div');
        feed_div.className = "card";

        let message_area = document.createElement('div');
        message_area.className = "message_area";

        let message_paragraph = document.createElement('p');
        message_paragraph.innerHTML = list_items[i]["wish"];
        message_area.appendChild(message_paragraph);
        
        feed_div.appendChild(message_area);
        
        let interact_area = document.createElement('div');
        interact_area.className = "interact_area";
        
        let likeButton = document.createElement('button');
        likeButton.innerHTML = 'Like';
        interact_area.appendChild(likeButton);
        
        let metooButton = document.createElement('button');
        metooButton.innerHTML = 'Metoo';
        interact_area.appendChild(metooButton);
        
        feed_div.appendChild(interact_area);
        
        middle_panel.appendChild(feed_div);
        console.log(feed_div);
    }
}

//UI Contols
function toggleLogginForm() {

}

//Check if the user is logged in.
//Call this callback if the cookie is valid.
function showCommonWall() {
    document.getElementById("loginForm").style.display = "none";

    getBucketListItems('1001', {"password":"123456"});

}

function doAfterValidate(response) {
    response = JSON.parse(response);
    let isValid = response["data"]["isValid"];
    
    if (isValid) {
        console.log("User is valid can be logged in.")
        showCommonWall();
    } else {
        console.log("Invalid user.")
    }
}

function validateLogin() {
    let username = getCookie("username");
    let apiKey = getCookie("apiKey");

    if (username && apiKey) {
        xOb.postData("user/authorize",{"Content-Type":"application/json"},[], {"username":username, "apiKey":apiKey}, doAfterValidate)
    } else {
        console.log("No username and apikey in cookies. Login has to be prompted.");
    }
}

//doUILogin
function doUILogin() {
    let username = document.getElementById("loginUsername").value;
    let password = document.getElementById("loginPassword").value;
    doLogin(username, password, doAfterLogin);
}
//Login 
function doAfterLogin(response) {
    response = JSON.parse(response);
    setCookie("username", response["data"]["username"], 1);
    setCookie("apiKey", response["data"]["apiKey"], 1);
    showCommonWall();

}
function doLogin(username, password, callback) {
    if (username && password) {
        xOb.postData("user/login",{"Content-Type":"application/json"},[], {"username":username, "password":password}, callback)
    }
}

(function() {
    validateLogin();
})();