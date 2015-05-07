console.log("HELLO");

var comp = d3.select("#comp");
var a = d3.select("#a");
var typebool = false;
var s = "";

//Choose between using FB chat and user input
var chat = d3.select("#chat")
    .on("click", function() {
	if (typebool) {
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
	if (!typebool) {
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

//FB API Stuff
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
    
    //Remove everything and add a table
    d3.select("#content")
	.style("display", "none");
    d3.select("center")
	.append("div")
	.attr("id", "list")
    d3.select("#list")
	.append("h3")
	.text("Select chat involving...")
	.style("margin-bottom", "20px")
    d3.select("#list")
	.append("table")
	.attr("id", "t")
	.attr("border", "1px");

    //Populate the table with the people in your chats
    for (var i = 0;i < chats.length;i++) {	
	var people = "";
	var to = chats[i]["to"]["data"];
	people = people + to[0]["name"];
	for (var j = 1;j < to.length;j++) {
	    people = people + ", " + to[j]["name"];
	}

	d3.select("#t")
	    .append("tr")
	//Pretty stuff below
	    .attr("bgcolor", function() {
		if (i % 2 == 0) {
		    return "#87CEFA";
		} else {
		    return "#FFFFFF";
		}
	    })
	    .on("mouseover", function() {
		var origcolor = this.getAttribute("bgcolor");
		d3.select(this)
		    .attr("bgcolor", "#FAFAD2")
		    .on("mouseout", function() {
			d3.select(this)
			    .attr("bgcolor", origcolor);
		    });
	    })
	    .append("td")
	    .text(people)
	    .attr("id", "t" + i)
	//When you click on a row, it should get back the chat to put in the textbox
	    .on("click", function() {
		var id = "";
		for (var h = 0;h < this.id.length;h++) {
		    if (!isNaN(parseInt(this.id[h]))) {
			id = id + this.id[h];
		    }
		}
		var url = chats[parseInt(id)]["comments"]["paging"]["next"];
		d3.json(url, function(json) {
		    //console.log(json);
		    for (var h = 0;h < json["data"].length;h++) {
			//console.log(json["data"][h]["from"]["name"] + ": " + json["data"][h]["message"]);
			//console.log("I WORK");
			s = s + json["data"][h]["from"]["name"] + ": " + json["data"][h]["message"] + "\n";
			//console.log("I DID SOMETHING WITH S");
			//console.log("S is : " + s);
			if (h == json["data"].length - 1) {
			    console.log(s);
			    d3.select("#list")
				.remove();
			    d3.select("#content")
				.style("display", "inline");
			    console.log("S is : " +s);
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
				.text(s);
			}
		    }
		});
	    });
    }
}
