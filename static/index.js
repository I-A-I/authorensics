console.log("HELLO");

var comp = d3.select("#comp");
var a = d3.select("#a")
var typebool = false;
var select = "";

var chat = d3.select("#chat")
    .on("click", function() {
	if (typebool == true) {
	    a.select("textarea")
		.transition()
		.duration(500)
		.style("width", "0px")
		.style("height", "0px")
		.remove();
	    typebool = false;
	}
	FB.login(getUserData, {scope: "read_mailbox"});
    });
var type = d3.select("#type")
    .on("click", function() {
	if (typebool == false) {
	    a.append("textarea")
	    	.attr("name", "a")
		.style("width", "0px")
		.style("height", "0px") 
		.style("margin-bottom", "20px")
		.transition()
		.duration(750)
		.style("width", "559px")
		.style("height", "107px")
		.transition()
		.delay(750)
		.text("Anonymous Text Goes Here!");
	    typebool = true;
	}
    });
	
var count = 1; // Keeps count of how many textareas you have added
var button = d3.select("#add")
    .on("click", function() {
	count++;
	comp.append("br")
	comp.append("textarea")
	    .attr("name", count)
	    .style("width", "0px")
	    .style("height", "0px") 
	    .style("margin-bottom", "20px")
	    .transition()
	    .duration(750)
	    .style("width", "559px")
	    .style("height", "107px")
	    .transition()
	    .delay(750)
	    .text("Comparison Text #" + count + " Goes Here!");
    });

function getUserData() {
    FB.api("/me", getInbox);
};

function getInbox(response) {
    if (response.error) {
    }
    user_data = response;
    FB.api("/me/inbox", {limit: 50 }, displayFriends);
}

function displayFriends(response) {
    var chats = response.data;
    var content = d3.select("#content")
	.remove();
    d3.select("center")
	.append("div")
	.attr("id", "content")
    d3.select("#content")
	.append("h3")
	.text("Select chat involving...")
	.style("margin-bottom", "20px")
	.append("table")
	.attr("id", "t")
	.attr("border", "1px");

    for (i = 0;i < 50;i++) {	
	var people = "";
	var to = chats[i]["to"]["data"];
	people = people + to[0]["name"];
	for (j = 1;j < to.length;j++) {
	    people = people + ", " + to[j]["name"];
	}

	d3.select("#t")
	    .append("tr")
	    .append("td")
	    .text(people)
	    .attr("id", "t" + i)
	    .on("click", function() {
		var id = "";
		for (h = 0;h < this.id.length;h++) {
		    if (!isNaN(parseInt(this.id[h]))) {
			id = id + this.id[h];
		    }
		}
		var url = chats[parseInt(id)]["comments"]["paging"]["next"];
		d3.json(url, function(json) {
		    for (h = 0;h < json["data"].length;h++) {
			select = select + json["data"][h]["from"]["name"] + ": " + json["data"][h]["message"] + "\n";
		    }
		});
	    });
    }
}
