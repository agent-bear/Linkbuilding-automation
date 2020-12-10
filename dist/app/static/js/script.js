var linkList = document.getElementById("backlinkList");

var xmlhttp = new XMLHttpRequest();
var linkArray = []

function updateList() {
    
    linkList.innerHTML = "";
    for (let i=0; i < linkArray.length; i++) {
        linkList.innerHTML += "<a target='_blank' href=" + linkArray[i] + ">" + linkArray[i] + "</a>";

        linkList.innerHTML += "<button type='button' class='deleteButton' data-linkid=" + i + " id=" + "delete " + i + ">Delete</button>";
        
        linkList.innerHTML += "<br>";
        linkList.innerHTML += "<br>";

    }
    const deleteButtons = document.querySelectorAll(".deleteButton");
    deleteButtons.forEach(deleteButtons => {
        deleteButtons.addEventListener('click', function(){
            var num = this.getAttribute("data-linkid");
            linkArray.splice(num, 1);
            updateList(); 
        });
    })
}


function addLink() {
    let newlink = prompt("pleas enter a URL", "https://");
    console.log(newlink)
    linkArray.push(newlink);
    console.log(linkArray)



    updateList();
}

function start(){
    var targetURL = document.getElementById("targetUrl").value;
    var targetName = document.getElementById("targetName").value;
    var targetEmail = document.getElementById("targetEmail").value;
    var accessToken = document.getElementById("accessToken").value;
    var privateKey = document.getElementById("privateKey").value;
    var devEnviroment = document.getElementById("devEnviroment").checked;

    message = {
        "targetURL":targetURL,
        "targetName":targetName,
        "targetEmail":targetEmail,
        "accessToken":accessToken,
        "privateKey":privateKey,
        "devEnviroment":devEnviroment,
        "linksToRequest": linkArray
    }

    jsonMessage = JSON.stringify(message)
    console.log(jsonMessage)

    xmlhttp.open("POST", "http://127.0.0.1:8080/req", true);
    xmlhttp.setRequestHeader('Content-Type', 'application/json');
    xmlhttp.send(jsonMessage);
    
}
