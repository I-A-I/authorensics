var content = d3.select("#content");
var results = content.selectAll("h3");
var result;
var similarity = 0;
var max = [];
var pmax = 0;
var percents = {};

var confidence_threshold = 0.1;

for (var i = 0; i < results[0].length;i++) {
    result = results[0][i];
    var slist = "";
    for (var j = result.innerHTML.search(": ") + 3;j < result.innerHTML.length - 2;j++) {
	slist = slist + result.innerHTML[j];
    }
    console.log(result.innerHTML[result.innerHTML.search(": ") + 3]);
    console.log(slist);
    slist = slist.split(", ");
    for (var j = 0;j < slist.length;j++) {
	slist[j] = parseInt(slist[j]);
    }
    //similarity = parseInt(result.innerHTML[result.innerHTML.search(": ") + 2] + result.innerHTML[result.innerHTML.search(": ") + 3]);
    similarity = slist[0] * 2 + slist[1] * 3 + slist[2] * 4 + slist[3] * 5 + slist[4] * 6;
    
    percents[result.id] = similarity;
    if (similarity == pmax) {
        max.push(result.id);
    }

    if (similarity > pmax) {
        pmax = similarity;
        max = [result.id];
    }

    d3.select("#" + result.id)
	.style("color", "rgb(" + (255 - (255 * (similarity / 100))) + ", " + (255 * (similarity / 100)) + ", 0");

    if (i == results[0].length - 1) {
        var message;
        if (pmax == 0)
            message = "None of the candidates had any similarity to the anonymous text."

        if (pmax < confidence_threshold)
            message = "None of the candidates had sufficient similarity to the anonymous text.";
        
        if (pmax >= confidence_threshold) {
            if (max.length == 1)
                message = "The closest match was " + max[0] + " with a similarity percentage of " + pmax + "%."

            else {
                var result_names = max.join(" and ");
                message = "The results were tied at " + pmax + "% between " + results_names + ".";
            }
        }
	content.insert("h2")
	    .text(message);
    }

}
