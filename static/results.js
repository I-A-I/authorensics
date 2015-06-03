var content = d3.select("#content");
var results = content.selectAll("h3");
var result;
var similarity = 0;
var max = [];
var pmax = 0;
var percents = {};

var confidence_threshold = 0.1;

/*
var bars1 = [];
var bars2 = [{"name":"", "y":""}];
var bars3 = [{"name":"", "y":""}];
var bars4 = [{"name":"", "y":""}];
var bars5 = [{"name":"", "y":""}];
*/

var bardata = [{"y": "2gram"},
	       {"y": "3gram"},
	       {"y": "4gram"},
	       {"y": "5gram"},
	       {"y": "6gram"}];

var barlabel = [];

for (var i = 0; i < results[0].length;i++) {
    result = results[0][i];
    var slist = "";
    for (var j = result.innerHTML.search(": ") + 3;j < result.innerHTML.length - 2;j++) {
	slist = slist + result.innerHTML[j];
    }
    slist = slist.split(", ");
    console.log(slist);
    for (var j = 0;j < slist.length;j++) {
    	slist[j] = parseFloat(slist[j]);
    }
    /*
    bars1.push({"name":result.id, "y":parseInt(slist[0] * 100)});
    bars2.push({"name":result.id, "y":parseInt(slist[1] * 100)});
    bars3.push({"name":result.id, "y":parseInt(slist[2] * 100)});
    bars4.push({"name":result.id, "y":parseInt(slist[3] * 100)});
    bars5.push({"name":result.id, "y":parseInt(slist[4] * 100)}); 
    */

    barlabel.push(result.id);
    bardata[0][result.id] = parseInt(slist[0] * 100);
    bardata[1][result.id] = parseInt(slist[1] * 100);
    bardata[2][result.id] = parseInt(slist[2] * 100);
    bardata[3][result.id] = parseInt(slist[3] * 100);
    bardata[4][result.id] = parseInt(slist[4] * 100);

    //    slist = map(slist,function(j){ parseFloat(j); }); map is not included :(
    //similarity = parseInt(result.innerHTML[result.innerHTML.search(": ") + 2] + result.innerHTML[result.innerHTML.search(": ") + 3]);
    similarity = (slist[0] * 2 + slist[1] * 3 + slist[2] * 4 + slist[3] * 5 + slist[4] * 6) / (2 + 3 + 4 + 5 + 6);
    
    percents[result.id] = similarity;
    if (similarity == pmax) {
        max.push(result.id);
    }

    if (similarity > pmax) {
        pmax = parseInt(similarity * 100);
        max = [result.id];
    }


    if (similarity <= 0.5) {
	d3.select("#" + result.id)
	    .style("color", "rgb(255, " + parseInt(255 * similarity) + ", 0)");	
    } else {
	d3.select("#" + result.id)
	    .style("color", "rgb(" + parseInt(255 - (255 * similarity)) + ", 255, 0)");
    }

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
                message = "The results were tied at " + pmax + "% between " + result_names + ".";
            }
        }
	content.insert("h2")
	    .text(message);
    }

}

console.log(bardata);
console.log(barlabel);

Morris.Bar({
    element: "barchart",
    data: bardata,
    xkey: "y",
    ykeys: barlabel,
    labels: barlabel
});

/*
var amt = bars1.length;

var width=600;
var height=400;
var padding=20;

var yScale = d3.scale.linear()
    .domain([0,110])
    .range([height,20]);

var xScale = d3.scale.linear()
    .domain([0,(amt + 1) * 5 - 1])
    .range([0,width]);

var yAxis = d3.svg.axis().scale(yScale).orient("left");

var svg = d3.select("#content")
    .append("svg")
    .attr('width',width)
    .attr('height',height)
    .attr("id","svg")
    .classed('bordered',true)
    .append("g")
    .attr("transform","translate(40,-30)")
    .call(yAxis);

svg.selectAll(".bars")
    .data(bars1)
    .enter()
    .append("g")
    .classed('bars',true);

svg.selectAll(".bars")
    .append("rect")
    .attr("x",function(d,i){return xScale(i);})
    .attr("y",function(d){return yScale(d.y);})
    .attr("width",width/(amt * 5 - 1) -20)
    .attr("height",function(d){return height-yScale(d.y);})
    .attr("fill","#0000ff");

svg.selectAll(".bars")
    .append("text")
    .attr("x",function(d,i){return xScale(i);})
    .attr("y",function(d){return yScale(d.y);})
    .attr("font-family",'sans-serif')
    .attr("font-size","25px")
    .attr("fill","#000000")
    .text(function(d){return d.y;});

svg.selectAll(".bars")
    .append("text")
    .attr("transform","translate(0,55)")
    .attr("x",function(d,i){return xScale(i);})
    .attr("y",function(d){return height-30;})
    .attr("font-family",'sans-serif')
    .attr("font-size","30px")
    .attr("fill","black")
    .text(function(d){return d.name;});

svg.selectAll(".bars")
    .data(bars2)
    .enter()
    .append("g")
    .classed("bars", true);

svg.selectAll(".bars")
    .append("rect")
    .attr("x",function(d,i){return xScale(i + amt);})
    .attr("y",function(d){return yScale(d.y);})
    .attr("width",width/(amt * 5 - 1) -20)
    .attr("height",function(d){return height-yScale(d.y);})
    .attr("fill","#0000ff");

svg.selectAll(".bars")
    .append("text")
    .attr("x",function(d,i){return xScale(i + amt);})
    .attr("y",function(d){return yScale(d.y);})
    .attr("font-family",'sans-serif')
    .attr("font-size","25px")
    .attr("fill","#000000")
    .text(function(d){return d.y;});

svg.selectAll(".bars")
    .append("text")
    .attr("transform","translate(0,55)")
    .attr("x",function(d,i){return xScale(i + amt);})
    .attr("y",function(d){return height-30;})
    .attr("font-family",'sans-serif')
    .attr("font-size","30px")
    .attr("fill","black")
    .text(function(d){return d.name;});

svg.selectAll(".bars")
    .data(bars3)
    .enter()
    .append("g")
    .classed("bars", true);

svg.selectAll(".bars")
    .append("rect")
    .attr("x",function(d,i){return xScale(i + amt);})
    .attr("y",function(d){return yScale(d.y);})
    .attr("width",width/(amt * 5 - 1) -20)
    .attr("height",function(d){return height-yScale(d.y);})
    .attr("fill","#0000ff");

svg.selectAll(".bars")
    .append("text")
    .attr("x",function(d,i){return xScale(i + amt);})
    .attr("y",function(d){return yScale(d.y);})
    .attr("font-family",'sans-serif')
    .attr("font-size","25px")
    .attr("fill","#000000")
    .text(function(d){return d.y;});

svg.selectAll(".bars")
    .append("text")
    .attr("transform","translate(0,55)")
    .attr("x",function(d,i){return xScale(i + amt);})
    .attr("y",function(d){return height-30;})
    .attr("font-family",'sans-serif')
    .attr("font-size","30px")
    .attr("fill","black")
    .text(function(d){return d.name;});

svg.selectAll(".bars")
    .data(bars4)
    .enter()
    .append("g")
    .classed("bars", true);

svg.selectAll(".bars")
    .append("rect")
    .attr("x",function(d,i){return xScale(i + amt);})
    .attr("y",function(d){return yScale(d.y);})
    .attr("width",width/(amt * 5 - 1) -20)
    .attr("height",function(d){return height-yScale(d.y);})
    .attr("fill","#0000ff");

svg.selectAll(".bars")
    .append("text")
    .attr("x",function(d,i){return xScale(i + amt);})
    .attr("y",function(d){return yScale(d.y);})
    .attr("font-family",'sans-serif')
    .attr("font-size","25px")
    .attr("fill","#000000")
    .text(function(d){return d.y;});

svg.selectAll(".bars")
    .append("text")
    .attr("transform","translate(0,55)")
    .attr("x",function(d,i){return xScale(i + amt);})
    .attr("y",function(d){return height-30;})
    .attr("font-family",'sans-serif')
    .attr("font-size","30px")
    .attr("fill","black")
    .text(function(d){return d.name;});

svg.selectAll(".bars")
    .data(bars5)
    .enter()
    .append("g")
    .classed("bars", true);

svg.selectAll(".bars")
    .append("rect")
    .attr("x",function(d,i){return xScale(i + amt);})
    .attr("y",function(d){return yScale(d.y);})
    .attr("width",width/(amt * 5 - 1) -20)
    .attr("height",function(d){return height-yScale(d.y);})
    .attr("fill","#0000ff");

svg.selectAll(".bars")
    .append("text")
    .attr("x",function(d,i){return xScale(i + amt);})
    .attr("y",function(d){return yScale(d.y);})
    .attr("font-family",'sans-serif')
    .attr("font-size","25px")
    .attr("fill","#000000")
    .text(function(d){return d.y;});

svg.selectAll(".bars")
    .append("text")
    .attr("transform","translate(0,55)")
    .attr("x",function(d,i){return xScale(i + amt);})
    .attr("y",function(d){return height-30;})
    .attr("font-family",'sans-serif')
    .attr("font-size","30px")
    .attr("fill","black")
    .text(function(d){return d.name;});
*/
