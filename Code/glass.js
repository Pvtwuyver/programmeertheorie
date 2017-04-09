/*
...
*/

// size
Width = 600;
Height = 500;
Area = Width*Height;

// --- pre-specified order
//order = [[20,20],[50,50],[150,150],[250,150],[100,150],[200,150],[100,100],[10,100],[100,50],[50,250]]; // [width,height]

// order = [[190,270],[90,160],[120,290],[110,220],[160,120],[90,120],[200,100],[110,290],[120,170],[100,320],[90,160],[190,300],[170,250],[180,340],
// [170,180],[90,100],[110,270],[70,220],[40,130],[140,330],[130,110],[40,240]];

// read tsv file and create order in [[h,w],[h,w]] format
// var order = [];
// d3.tsv("Glaslijsten/GlasLijst1.tsv", function(error, data) {
//   if (error) throw error;
//   // Coerce the data to numbers.
//   data.forEach(function(d) {
//     d.w = +d.w;
//     d.h = +d.h;
//     order.push([d.w,d.h]);
//   });
//   console.log(order);
// })

// --- random order
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

total = order.length;
console.log("Number of cuts ordered: ",total, orderArea, Area);

 
var svg = d3.select("body").append("div")
	.attr("style","width: "+ Width + "px; height: "+ Height + "px; border: 2px solid black;  background-color: #eee;")
   .append("svg")
   	.attr("height",Height)
	.attr("width",Width);

// voer functie uit:
	
verticalFill(Width,Height,0,0);
//horizontalFill(Width,Height,0,0);

usedArea = orderArea - totalArea(order);
efficiency = (usedArea/Area);
console.log("Number of cuts made: ",total - order.length);
console.log("Efficiency: ",efficiency);
console.log(order);

function verticalFill(W, H, xIndex, yIndex) {
	var xStart = xIndex;
	var yStart = yIndex;
	var colWidth = W, rowHeight = H;
	orientation(order, "width");
	order.sort(sortHeight);
	order.sort(sortWidth);
	while (order.length > 0) {
		console.log("vertical - colWidth:", colWidth, "rowHeight", rowHeight);
		cut = search(order, colWidth, rowHeight);
		console.log("Cut: ", cut);
		if (cut != null) { var cutWidth = cut[0], cutHeight = cut[1];}
		else {
			console.log("new col");
			xIndex += colWidth;
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
			cut = search(order, colWidth, rowHeight);
			console.log("Cut: ", cut);
			if (cut != null) { var cutWidth = cut[0], cutHeight = cut[1];}
			else {console.log("break/ no fit");break;}
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
	}
};

function horizontalFill(W, H, xIndex, yIndex) {
	var xStart = xIndex;
	var yStart = yIndex;
	var colWidth = W, rowHeight = H;
	orientation(order, "height");
	order.sort(sortWidth);
	order.sort(sortHeight);
	while (order.length > 0) {
		console.log("horizontal - colWidth:", colWidth, "rowHeight", rowHeight);
		cut = search(order, colWidth, rowHeight);
		console.log("Cut: ", cut);
		if (cut != null) { var cutWidth = cut[0], cutHeight = cut[1];}
		else {
			console.log("new row");
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
			else {console.log("break/ no fit");break;}
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

// change the orientation of a glass cut
function orientation(list, side) {
	console.log("change orientation", side);
	for (item in list) {	
		var max = Math.max(list[item][0],list[item][1]), min = Math.min(list[item][0],list[item][1]);
		if (side == "width") {list[item][0] = max; list[item][1] = min;}
		else if (side == "height") {list[item][1] = max; list[item][0] = min;}
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
	while (value < 0.01) {
		value = ((Math.random() + Math.random() + Math.random() + Math.random() + Math.random() + Math.random()) - 3) / 3;
	}	
	return 350*Math.abs(value);
}
