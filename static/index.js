var comp = d3.select("#comp");
var a = d3.select("#a");
var s = "";
var user_data;

var ROW_COLOR_ONE = "rgb(160, 220, 250)";
var ROW_COLOR_TWO = "white";

d3.select("#submit")
    .on("click", function() {
        var is_disabled = $(this).hasClass("pure-button-disabled");
        if (is_disabled)
            d3.event.preventDefault();
    } );

d3.select("#anon")
    .on("keyup", anonTextChanged)
    .on("change", anonTextChanged);

function anonTextChanged() {
    var num_candidates = d3.selectAll("#comp textarea")[0].length;
    if (num_candidates > 0)
        $("#submit").removeClass("pure-button-disabled");
}

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
	
var countc = 0; // Keeps count of how many textareas you have added
d3.select("#addc")
    .on("click", function() {
        var current_anon_text = d3.select("#anon")[0][0].value;
        if (current_anon_text.length > 1)
            $("#submit").removeClass("pure-button-disabled");
	countc++;
	comp.append("br")	
	comp.append("textarea")
	    .attr("name", countc)
	    .attr("id", "c" + countc)
	    .style("width", "0px")
	    .style("height", "0px") 
	    .style("margin-bottom", "20px")
	    .transition()
	    .duration(750)
	    .style("width", "559px")
	    .style("height", "107px")
	    .transition()
	    .delay(750)
        .attr("placeholder", "Paste candidate text");
	comp.insert("input", "#c" + countc)
	    .attr("name", "n" + countc)
	    .style("margin-bottom", "20px")
	    .attr("type", "text")
	    .style("width", "0px")
	    .style("margin-right", "10px")
	    .transition()
	    .delay(750)
	    .duration(250)
	    .style("width", "189px")
	    .transition()
	    .delay(1000)
	    .attr("placeholder", "Candidate Name");
    });

//FB API Stuff
function getUserData() {
    FB.api("/me", getInbox);
};

function getInbox(response) {
    if (response.error) {
    }
    user_data = response;
    //console.log(user_data);
    FB.api("/me/inbox", {limit: 50 }, displayFriends);
}

function displayFriends(response) {
    var chats = response.data;
    //console.log(chats);
    if (chats == undefined) {
	// FB API ERROR
	alert("Too many Facebook API Requests! Try again in 15 minutes!");
    } else {
	getChats(chats);
    }
}

function getChats(chats) {
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
    .attr("style", "border-color: rgb(200, 200, 200)")
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
	    .attr("style", function() {
		if (i % 2 == 0) {
		    return "background-color: " + ROW_COLOR_ONE;
		} else {
		    return "background-color: " + ROW_COLOR_TWO;
		}
	    })
	    .on("mouseover", function() {
		var origcolor = this.style.backgroundColor;
		d3.select(this)
		    .attr("style", "background-color: rgb(190, 250, 255)")
		    .on("mouseout", function() {
			d3.select(this)
                .attr("style", "background-color: " + origcolor)
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
		var limit = 0; //Limit for how much FB can access
		
		//Loading bar
		var load = 0; //Percent loaded
		var list = d3.select("#list")
		    .remove();
		//console.log(list);
		d3.select("center")
		    .append("div")
		    .attr("class", "progress")
		    .style("margin", "25px 50px 25px 50px")
		    .append("div")
		    .attr("id", "load")
		    .attr("class", "progress-bar progress-bar-striped active")
		    .attr("role", "progressbar")
		    .attr("aria-valuenow", 0)
		    .attr("aria-valuemin", 0)
		    .attr("aria-valuemax", 100)
		    .style("width", "0%")
		d3.select("center")[0][0].appendChild(list[0][0]);
		
		//Recursively gets all "next" pages, then calls function below
		var getURLNext = function(url) {
		    d3.json(url, function(json) {
			//console.log(json);
			next.push(json["data"]);
			//console.log("In Function: " + json["paging"]["next"]);
			if (!("paging" in json) || limit > 10) {
			    limit = 0;
			    load = 88;
			    d3.select("#load")
				.style("width", load + "%")
				.attr("aria-valuenow", load)
				.text(load + "%");
			    getURLPrev(url1);
			} else {
			    load = load + 8;
			    d3.select("#load")
				.style("width", load + "%")
				.attr("aria-valuenow", load)
				.text(load + "%");
			    limit++;
			    getURLNext(json["paging"]["next"]);
			}
		    });
		}

		//Recursively gets all "previous" pages, then calls function below
		var getURLPrev = function(url) {
		    d3.json(url, function(json) {
			prev.push(json["data"]);
			//console.log("In Function: " + json["paging"]["next"]);
			if (!("paging" in json) || limit > 10) {
			    limit = 0;
			    load = 100;
			    d3.select("#load")
				.style("width", load + "%")
				.attr("aria-valuenow", load)
				.text(load + "%");
			    setUp();
			} else {
			    load = 100;
			    d3.select("#load")
				.style("width", load + "%")
				.attr("aria-valuenow", load)
				.text(load + "%");
			    limit++;
			    getURLPrev(json["paging"]["previous"]);
			}
		    });
		}

		//Orders the chat properly, then sets up the textbox
		var setUp = function() {
            var current_anon_text = d3.select("#anon")[0][0].value;
            if (current_anon_text.length > 1)
                $("#submit").removeClass("pure-button-disabled");
            countc++;
		    next.pop();
		    next = next.reverse();
		    prev.pop();
		    prev = prev.reverse();
		    prev.pop();
		    prev = prev.reverse();
		    //console.log(next);
		    //console.log(prev);
		    for (var h = 0;h < next.length;h++) {
                for (var k = 0;k < next[h].length;k++) {
                    if (next[h][k]["from"] == undefined) { //Sometimes the "from" is missing? Stupid FB API
                        null;
                    } else {
                        if (next[h][k]["from"]["name"] != user_data["first_name"] + " " + user_data["last_name"]) {
                            s = s + next[h][k]["from"]["name"] + ": " + next[h][k]["message"] + "\n";
                        }
                    }
                }
		    }
		    for (var h = 0; h < prev.length;h++) {
                for (var k = 0; k < prev[h].length;k++) {
                    if (prev[h][k]["from"] == undefined) {
                        //s = s + prev[h][k]["message"] + "\n";
                        null;
                    } else {
                        if (prev[h][k]["from"]["name"] != user_data["first_name"] + " " + user_data["last_name"]) {
                            s = s + prev[h][k]["from"]["name"] + ": " + prev[h][k]["message"] + "\n";
                        }
                    }
                }

			if (h == prev.length - 1) {	    
			    d3.select("#list")
				.remove();
			    d3.select(".progress")
				.remove();
			    d3.select("#content")
				.style("display", "inline");
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
				.text(s);
                console.log(s);
			}
		    }
		}

		getURLNext(url1);
	    })
    }
}
