console.log("HELLO");

var comp = d3.select("#comp");
var a = d3.select("#a");
var s = "";

//Choose between using FB chat and user input
var chat = d3.select("#chat")
    .on("click", function() {
	/*if (typebool) { With multiple anonymous text areas, removal here is superficial
	    a.select("textarea")
		.transition()
		.duration(500)
		.style("width", "0px")
		.style("height", "0px")
		.remove();
	    typebool = false;
	}*/
	FB.login(getUserData, {scope: "read_mailbox"});
    });
var counta = 0;
var type = d3.select("#type")
    .on("click", function() {
	counta++;
	a.append("br")
	a.append("textarea")
	    .attr("name", "a" + counta)
	    .style("width", "0px")
	    .style("height", "0px") 
	    .style("margin-bottom", "20px")
	    .transition()
	    .duration(750)
	    .style("width", "559px")
	    .style("height", "107px")
	    .transition()
	    .delay(750)
	    .text("Anonymous Text #" + counta + " Goes Here!");
    });
	
var countc = 1; // Keeps count of how many textareas you have added
d3.select("#addc")
    .on("click", function() {
	countc++;
	comp.append("br")
	comp.append("textarea")
	    .attr("name", countc)
	    .style("width", "0px")
	    .style("height", "0px") 
	    .style("margin-bottom", "20px")
	    .transition()
	    .duration(750)
	    .style("width", "559px")
	    .style("height", "107px")
	    .transition()
	    .delay(750)
	    .text("Comparison Text #" + countc + " Goes Here!");
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

function test(url, json) {
    url = json["paging"]["next"];
    s = "";
    for (var h = 0;h < json["data"].length;h++) {
	s = s + json["data"][h]["from"]["name"] + ": " + json["data"][h]["message"] + "\n";
	if (h == json["data"].length - 1) {
	    d3.select("#list")
		.remove();
	    d3.select("#content")
		.style("display", "inline");
	}
    }
}

function displayFriends(response) {
    var chats = response.data;
    //console.log(chats);
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
		s = "";
		for (var h = 0;h < this.id.length;h++) { //Gets the ID of the row you clicked on
		    if (!isNaN(parseInt(this.id[h]))) {
			id = id + this.id[h];
		    }
		}
		var url1 = chats[parseInt(id)]["comments"]["paging"]["next"];// + ".json"; Original url
		var next = [];
		var prev = [];

		//Recursively gets all "next" pages, then calls function below
		var getURLNext = function(url) {
		    d3.json(url, function(json) {
			next.push(json["data"]);
			//console.log("In Function: " + json["paging"]["next"]);
			if (!("paging" in json)) {
			    getURLPrev(url1);
			} else {
			    getURLNext(json["paging"]["next"]);
			}
		    });
		}

		//Recursively gets all "previous" pages, then calls function below
		var getURLPrev = function(url) {
		    d3.json(url, function(json) {
			prev.push(json["data"]);
			//console.log("In Function: " + json["paging"]["next"]);
			if (!("paging" in json)) {
			    setUp();
			} else {
			    getURLPrev(json["paging"]["previous"]);
			}
		    });
		}

		//Orders the chat properly, then sets up the textbox
		var setUp = function() {
		    next.pop();
		    next = next.reverse();
		    prev.pop();
		    prev = prev.reverse();
		    prev.pop();
		    prev = prev.reverse();
		    for (var h = 0;h < next.length;h++) {
			for (var k = 0;k < next[h].length;k++) {
			    s = s + next[h][k]["from"]["name"] + ": " + next[h][k]["message"] + "\n";
			}
		    }
		    for (var h = 0;h < prev.length;h++) {
			for (var k = 0;k < prev[h].length;k++) {
			    s = s + prev[h][k]["from"]["name"] + ": " + prev[h][k]["message"] + "\n";
			}
			if (h == prev.length - 1) {
			    d3.select("#list")
				.remove();
			    d3.select("#content")
				.style("display", "inline");
			    
			    counta++;
			    a.append("br")
			    a.append("textarea")
	    			.attr("name", "a" + counta)
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
		}

		getURLNext(url1);
	    })
    }
}
