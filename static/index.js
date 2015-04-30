console.log("HELLO");

var comp = d3.select("#comp");
var a = d3.select("#a")

var fb = d3.select("#chat")
    .on("click", function() {
	a.select("textarea")
	    .remove();
	a.select("br")
	    .remove();
	a.select("br")
	    .remove();
	/*FB.api(
	    "/me",
	    function (response) {
		if (response && !response.error) {
		}
	    }
	);*/
    });
var type = d3.select("#type")
	.on("click", function() {
	    a.append("textarea")
		.attr("name", "a")
		.attr("rows", 4)
		.attr("cols", 50)
		.text("Anonymous Text Goes Here!");
	    a.append("br");
	    a.append("br");
	});
	
var count = 1; // Keeps count of how many textareas you have added
var button = d3.select("#add")
    .on("click", function() {
	count++;
	comp.append("br");
	comp.append("br");
	comp.append("textarea")
	    .attr("name", count)
	    .attr("rows", 4)
	    .attr("cols", 50)
	    .text("Comparison Text #" + count + " Goes Here!");
    });
