console.log("HELLO");

var content = d3.select("#content");
var a = content.selectAll("h3");
var t;
var p = 0;
var max = "";
var pmax = 0;
var percents = {};

for (var i = 0;i < a[0].length;i++) {
    t = a[0][i];
    p = parseInt(t.innerHTML[t.innerHTML.search(": ") + 2] + t.innerHTML[t.innerHTML.search(": ") + 3]);
    percents[t.id] = p;
    if (p >= pmax) {
	pmax = p;
	max = t.id;
    }

    d3.select("#" + t.id)
	.style("color", "rgb(" + (255 - (255 * (p / 100))) + ", " + (255 * (p / 100)) + ", 0");

    if (i == a[0].length - 1) {
	content.insert("h2")
	    .text("The closest match was " + max + " with a similarity percentage of " + pmax + "%!");
    }
}

