/*
...
*/

order = [[20,20],[50,50],[150,150],[250,150],[100,150],[200,150],[100,100],[10,100],[100,50],[50,250]]; // [width,height]

total = order.length;
orderArea = totalArea(order);
console.log("Number of cuts ordered: ",total);


Width = 600;
Height = 500;
Area = Width*Height;

 
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
		cut = search(order, colWidth, rowHeight);
		if (cut != null) { var cutWidth = cut[0], cutHeight = cut[1];}
		else {
			xIndex += colWidth;
			colWidth = W - (xIndex - xStart);
			if (colWidth < 0) { break;}
			yIndex = yStart;
			rowHeight = H;
			if (rowHeight > colWidth) {orientation(order, "height");}
			cut = search(order, colWidth, rowHeight);
			if (cut != null) { var cutWidth = cut[0], cutHeight = cut[1];}
			else {break;}
		};
		svg.append("rect")
			.attr("transform", "translate(" + xIndex + "," + yIndex + ")")
			.attr("width",cutWidth)
			.attr("height",cutHeight)
			.attr("style","fill: #efda62; stroke-width:1; stroke:black");
		if (yIndex == yStart) {
			colWidth = cutWidth;
		}
		if ((cutHeight >= (colWidth - cutWidth)) && ((colWidth - cutWidth) > 0)) {
			horizontalFill(colWidth - cutWidth, cutHeight, xIndex + cutWidth, yIndex);
			orientation(order, "width");
		}
		else if ((cutHeight < (colWidth - cutWidth)) && ((colWidth - cutWidth) > 0)) {
			verticalFill(colWidth - cutWidth, cutHeight, xIndex + cutWidth, yIndex);
		};
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
		cut = search(order, colWidth, rowHeight);
		if (cut != null) { var cutWidth = cut[0], cutHeight = cut[1];}
		else {
			yIndex += rowHeight;
			rowHeight = H - (yIndex - yStart);
			if (rowHeight < 0) { break;}
			xIndex = xStart;
			colWidth = W;
			if (colWidth > rowHeight) {orientation(order, "width");}
			cut = search(order, colWidth, rowHeight);
			if (cut != null) { var cutWidth = cut[0], cutHeight = cut[1];}
			else {break;}
		};
		svg.append("rect")
			.attr("transform", "translate(" + xIndex + "," + yIndex + ")")
			.attr("width",cutWidth)
			.attr("height",cutHeight)
			.attr("style","fill: #efda62; stroke-width:1; stroke:black");
		if (xIndex == xStart) {
			rowHeight = cutHeight;
		}
		if ((cutWidth >= (rowHeight - cutHeight)) && ((rowHeight - cutHeight) > 0)) {
			verticalFill(cutWidth, rowHeight - cutHeight, xIndex, yIndex + cutHeight);
			orientation(order, "height");
		}
		else if ((cutWidth < (rowHeight - cutHeight)) && ((rowHeight - cutHeight) > 0)) {
			horizontalFill(cutWidth, rowHeight - cutHeight, xIndex, yIndex + cutHeight);
		};
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
