/*
...
*/

// size
Width = 600;
Height = 500;
Area = Width*Height;

// --- pre-specified order
/**
order = [[300,100],[250,125],[150,150],[150,150],[130,90],[130,90]]; // [width,height]
orderArea = totalArea(order);
**/

// --- glaslijst

var lines = document.getElementById("glaslijst").innerHTML.split("\n");
order = [];
for (var i = 0; i < lines.length; i++){
	var sizes = lines[i].split("\t");
	order[i] = [parseInt(sizes[0]),parseInt(sizes[1])]
}
console.log(order);
orderArea = totalArea(order);


// --- glaslijst (tsv)
/**
var order = [];
d3.tsv("https://raw.githubusercontent.com/Pvtwuyver/programmeertheorie/master/GlasLijsten/GlasLijst1.tsv", function(error, data) {
	if (error) throw error;
	// Coerce the data to numbers.
	data.forEach(function(d) {
	d.w = +d.w;
	d.h = +d.h;
	order.push([d.w,d.h]);
	});
	console.log(order);
	orderArea = totalArea(order);
})
**/

// --- random order
/**
orderArea = 0;
count = 0;
order = [];

while (orderArea <= Area) {
	var randomWidth = Math.round(randomSize()), randomHeight = Math.round(randomSize());
	randomCut = [randomWidth,randomHeight]
	orderArea += randomWidth*randomHeight;
	order[count] = randomCut;
	count++;
}
**/

total = order.length;
console.log("Number of cuts ordered: ",total, orderArea, Area);

// meerdere platen

numberOfWindows = 0;
while (order.length > 0) {

var svg = d3.select("body").append("div")
	.attr("style","width: "+ Width + "px; height: "+ Height + "px; border: 2px solid black;  background-color: #eee; transform: translate(0px,"+ numberOfWindows*10 +"px);")
   .append("svg")
   	.attr("height",Height)
	.attr("width",Width);

verticalFill(Width,Height,0,0);
//horizontalFill(Width,Height,0,0);

usedArea = orderArea - totalArea(order);
efficiency = (usedArea/Area);
console.log("Efficiency: ",efficiency);
	
numberOfWindows++;
}


// één plaat
/**
var svg = d3.select("body").append("div")
	.attr("style","width: "+ Width + "px; height: "+ Height + "px; border: 2px solid black;  background-color: #eee;")
   .append("svg")
   	.attr("height",Height)
	.attr("width",Width);
verticalFill(Width,Height,0,0);
**/

usedArea = orderArea - totalArea(order);
efficiency = (usedArea/Area);
console.log("Upper bound: ",orderArea/Area);
console.log("Number of cuts made: ",total - order.length, "/", total);
console.log("Efficiency: ",efficiency);
console.log(order);

function verticalFill(W, H, xIndex, yIndex) {
	var xStart = xIndex;
	var yStart = yIndex;
	var colWidth = W, rowHeight = H;
	while (order.length > 0) {
		orientation(order, "width");
		console.log("vertical - colWidth:", colWidth, "rowHeight", rowHeight);
		cut = search(order, colWidth, rowHeight);
		console.log("Cut: ", cut);
		if (cut != null) { var cutWidth = cut[0], cutHeight = cut[1];}
		else {
			console.log("new col", rowHeight);
			orientation(order, "height");
			cut = search(order, colWidth, rowHeight);
			if (cut != null) { var cutWidth = cut[0], cutHeight = cut[1];}
			else {
				orientation(order, "width");
				xIndex += colWidth;
				console.log("x: ", xIndex);
				colWidth = W - (xIndex - xStart);
				if (colWidth < 0) { console.log("break / no room");break;}
				yIndex = yStart;
				rowHeight = H;
				/**
				if ((rowHeight > colWidth) && (colWidth > 0) && (rowHeight > 0)) {
					horizontalFill(colWidth,rowHeight,xIndex,yIndex);
					orientation(order, "width");
				}
				**/
				console.log("next cut: ",colWidth, rowHeight);
				cut = search(order, colWidth, rowHeight);
				console.log("Cut: ", cut);
				if (cut != null) { var cutWidth = cut[0], cutHeight = cut[1];}
				else {
					console.log("break/ no fit");
					orientation(order, "height");
					console.log("next cut: ",colWidth, rowHeight);
					cut = search(order, colWidth, rowHeight);
					if (cut != null) { var cutWidth = cut[0], cutHeight = cut[1];}
					else {break;};
				//---
				}	
			}
		};
		svg.append("rect")
			.attr("transform", "translate(" + xIndex + "," + yIndex + ")")
			.attr("width",cutWidth)
			.attr("height",cutHeight)
			.attr("style","fill: #efda62; stroke-width:1; stroke:black");
		if (yIndex == yStart) {
			colWidth = cutWidth;
		}
		console.log("Room left:", (colWidth - cutWidth), cutHeight);
		if ((cutHeight > (colWidth - cutWidth)) && ((colWidth - cutWidth) > 0)) {
			horizontalFill(colWidth - cutWidth, cutHeight, xIndex + cutWidth, yIndex);
			orientation(order, "width");
		}
		else if ((cutHeight <= (colWidth - cutWidth)) && ((colWidth - cutWidth) > 0)) {
			verticalFill(colWidth - cutWidth, cutHeight, xIndex + cutWidth, yIndex);
		}
		else {console.log("No recursion possible");};
		yIndex += cutHeight;
		rowHeight = H - (yIndex - yStart);
		//if (rowHeight > colWidth) {horizontalFill(colWidth, rowHeight, xIndex, yIndex)};
	}
};

function horizontalFill(W, H, xIndex, yIndex) {
	var xStart = xIndex;
	var yStart = yIndex;
	var colWidth = W, rowHeight = H;
	while (order.length > 0) {
		orientation(order, "height");
		console.log("horizontal - colWidth:", colWidth, "rowHeight", rowHeight);
		cut = search(order, colWidth, rowHeight);
		console.log("Cut: ", cut);
		if (cut != null) { var cutWidth = cut[0], cutHeight = cut[1];}
		else {
			console.log("new row");
			orientation(order, "height");
			cut = search(order, colWidth, rowHeight);
			if (cut != null) { var cutWidth = cut[0], cutHeight = cut[1];}
			else {
				yIndex += rowHeight;
				rowHeight = H - (yIndex - yStart);
				if (rowHeight < 0) { console.log("break / no room");break;}
				xIndex = xStart;
				colWidth = W;
				/**
				if ((colWidth > rowHeight) && (colWidth > 0) && (rowHeight > 0)) {
					verticalFill(colWidth,rowHeight,xIndex,yIndex);
					orientation(order, "height");
				}
				**/
				cut = search(order, colWidth, rowHeight);
				console.log("Cut: ", cut);
				if (cut != null) { var cutWidth = cut[0], cutHeight = cut[1];}
				else {
					console.log("break/ no fit");
					orientation(order, "width");
					cut = search(order, colWidth, rowHeight);
					if (cut != null) { var cutWidth = cut[0], cutHeight = cut[1];}
					else {break;};
				}
			}
		};
		svg.append("rect")
			.attr("transform", "translate(" + xIndex + "," + yIndex + ")")
			.attr("width",cutWidth)
			.attr("height",cutHeight)
			.attr("style","fill: #efda62; stroke-width:1; stroke:black");
		if (xIndex == xStart) {
			rowHeight = cutHeight;
		}
		console.log("Room left:", cutWidth, (rowHeight - cutHeight));
		if ((cutWidth > (rowHeight - cutHeight)) && ((rowHeight - cutHeight) > 0)) {
			verticalFill(cutWidth, rowHeight - cutHeight, xIndex, yIndex + cutHeight);
			orientation(order, "height");
		}
		else if ((cutWidth <= (rowHeight - cutHeight)) && ((rowHeight - cutHeight) > 0)) {
			horizontalFill(cutWidth, rowHeight - cutHeight, xIndex, yIndex + cutHeight);
		}
		else {console.log("No recursion possible");};
		xIndex += cutWidth;
		colWidth = W - (xIndex - xStart);
	}
};

// sort list by width
function sortWidth(a, b) {
    if (a[0] === b[0]) {
        return 0;
    }
    else {
        return (a[0] > b[0]) ? -1 : 1;
    }
}

// sort list by height
function sortHeight(a, b) {
    if (a[1] === b[1]) {
        return 0;
    }
    else {
        return (a[1] > b[1]) ? -1 : 1;
    }
}

// sort list by circumference
function sortCirc(a, b) {
	circA = 2*a[0] + 2*a[1];
	circB = 2*b[0] + 2*b[1];
    if (circA === circB) {
        return 0;
    }
    else {
        return (circA > circB) ? -1 : 1;
    }
}

// change the orientation of a glass cut
function orientation(list, side) {
	console.log("change orientation", side);
	for (item in list) {	
		var max = Math.max(list[item][0],list[item][1]), min = Math.min(list[item][0],list[item][1]);
		if (side == "width") {
			list[item][0] = max; list[item][1] = min;
			list.sort(sortHeight);
			list.sort(sortWidth);
		}
		else if (side == "height") {
			list[item][1] = max; list[item][0] = min;
			list.sort(sortWidth);
			list.sort(sortHeight);
		}
	}
}

// search
function search(list, maxWidth, maxHeight) {
	for (var i in list) {
		if ((list[i][0] <= maxWidth) && (list[i][1] <= maxHeight)) {
			dim = list[i];
			list.splice(i,1);
			return dim
		}
	}
	return null;
}

function totalArea(list) {
	var area = 0;
	for (i in list) {
		area += list[i][0]*list[i][1];
	}
	return area;
}

function randomSize() {
	var value = 0;
	while (value < 20) {
		value = 350*((Math.random() + Math.random() + Math.random() + Math.random() + Math.random() + Math.random()) - 3) / 3;
	}	
	return Math.abs(value);
}
