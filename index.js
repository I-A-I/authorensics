console.log("HELLO");

var comp = d3.select("#comp");

var count = 1; // Keeps count of how many textareas you have added
var counter = d3.select("#counter");
var button = d3.select("#add")
    .on("click", function() {
	console.log("HELLO!");
	count++;
	counter.attr("value", count);
	comp.append("br");
	comp.append("br");
	comp.append("textarea")
	    .attr("name", count)
	    .attr("rows", 4)
	    .attr("cols", 50)
	    .text("Comparison Text #" + count + " Goes Here!");
    });
