/*
...
*/

order = [[20,20],[50,50],[150,150],[250,150],[100,150],[200,150],[100,100],[10,100],[100,50]]; // [width,height]

Width = 500;
Height = 300;

 
var svg = d3.select("body").append("div")
	.attr("style","width: "+ Width + "px; height: "+ Height + "px; border: 2px solid black;  background-color: #eee;")
   .append("svg")
   	.attr("height",Height)
	.attr("width",Width);

// voer functie uit:
	
verticalFill(Width,Height,0,0);
//horizontalFill(Width,Height,0,0);

function verticalFill(W, H, xIndex, yIndex) {
	var xStart = xIndex;
	var yStart = yIndex;
	var colWidth = W, rowHeight = H;
	orientation(order, "width");
	order.sort(sortHeight);
	order.sort(sortWidth);
	while (order.length > 0) {
		console.log(colWidth);
		cut = search(order, colWidth, rowHeight);
		console.log("Cut:", cut);
		if (cut != null) { var cutWidth = cut[0], cutHeight = cut[1];}
		else {
			xIndex += colWidth;
			colWidth = W - xIndex;
			if (colWidth < 0) { break;}
			console.log(colWidth);
			yIndex = yStart;
			rowHeight = H;
			cut = search(order, colWidth, rowHeight);
			if (cut != null) { var cutWidth = cut[0], cutHeight = cut[1];}
			else {break;}
			console.log(cut);
		};
		svg.append("rect")
			.attr("transform", "translate(" + xIndex + "," + yIndex + ")")
			.attr("width",cutWidth)
			.attr("height",cutHeight)
			.attr("style","fill: #efda62; stroke-width:1; stroke:black");
		if (yIndex == yStart) {
			colWidth = cutWidth;
		}
		yIndex += cutHeight;
		rowHeight = H - yIndex;
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
		console.log(rowHeight);
		cut = search(order, colWidth, rowHeight);
		console.log("Cut:", cut);
		if (cut != null) { var cutWidth = cut[0], cutHeight = cut[1];}
		else {
			yIndex += rowHeight;
			rowHeight = H - yIndex;
			if (rowHeight < 0) { break;}
			console.log(rowHeight);
			xIndex = xStart;
			colWidth = W;
			cut = search(order, colWidth, rowHeight);
			if (cut != null) { var cutWidth = cut[0], cutHeight = cut[1];}
			else {break;}
			console.log(cut);
		};
		svg.append("rect")
			.attr("transform", "translate(" + xIndex + "," + yIndex + ")")
			.attr("width",cutWidth)
			.attr("height",cutHeight)
			.attr("style","fill: #efda62; stroke-width:1; stroke:black");
		if (xIndex == xStart) {
			rowHeight = cutHeight;
		}
		xIndex += cutWidth;
		colWidth = W - xIndex;
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
