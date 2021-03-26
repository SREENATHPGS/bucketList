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

getBucketListItems('1001', {"password":"123456"});
//updateFeed(list_items);