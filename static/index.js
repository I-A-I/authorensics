console.log("HELLO");

var comp = d3.select("#comp");
var a = d3.select("#a")
var typebool = false;

var fb = d3.select("#chat")
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
