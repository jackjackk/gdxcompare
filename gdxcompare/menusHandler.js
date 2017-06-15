function Symb(name, desc, sets, data) {
	this.name = name;
	this.desc = desc;
	this.sets = sets;
	this.data = data;
	this.mask = 0;
	this.maxDiff = 0;
	this.tempMaxDiff = 0;
	var i;
	for (i=0;i<sets.length-1;i++) {
		this.mask |= 1<<sets[i];
	}
}
/*var symbList = new Array();
symbList[0] = new Symb("Q_EN",[0,1]);
symbList[1] = new Symb("I_EN",[1]);
symbList[2] = new Symb("K_EN",[0]);

var symbList = [new Symb("Q_EN",[0,1]),
				new Symb("I_EN",[1]),
				new Symb("K_EN",[0])];
*/
function Set(name, elems) {
this.name = name;
this.elems = elems;
this.currTable = undefined;
}
/*
var setList = new Array();
setList[0] = new Set('j',[1,2,3,4]);
setList[1] = new Set('n',['a','b','c']);
setList[2] = new Set('t',[10,20,30]);

var series = ['gdx1','gdx2'];

var xaxis = [2,2,2];

var yaxis =
	[
		[
			[
				[3,15,2,1,6,4], [3,5,2,11,6,2], [3,5,2,21,6,1]
			],
			[
				[3,5,12,1,6,5], [3,5,12,1,6,0], [3,5,2,1,26,2]
			],
			[
				[3,5,2,11,6,8], [3,15,2,1,6,9], [23,5,2,1,6,1]
			],
			[
				[3,5,2,1,16,8], [13,5,2,1,6,2], [3,5,22,1,6,4]
			]
		],
		[ 
			[34,5,2,1,6,9], [3,5,24,1,6,10], [3,5,2,14,6,12]
		],
		[
		[3,5,20,1,6,15], [3,5,2,10,6,20], [30,5,2,1,6,12], [3,50,2,1,6,17]
		],
	];
*/

/*var symbList = [
new Symb("x",[1, 0],{'0,3': [1.6094379124341003, 3.2188758248682006], '0,2': [1.3862943611198906, 2.772588722239781], '0,1': [1.0986122886681098, 2.1972245773362196], '0,0': [0.6931471805599453, 1.3862943611198906], '1,2': [1.252762968495368, 2.505525936990736], '1,3': [1.5040773967762742, 3.0081547935525483], '1,0': [0.4054651081081644, 0.8109302162163288], '1,1': [0.9162907318741551, 1.8325814637483102], '2,1': [0.8472978603872037, 1.6945957207744073], '2,0': [0.28768207245178085, 0.5753641449035617], '2,3': [1.466337068793427, 2.932674137586854], '2,2': [1.2039728043259361, 2.4079456086518722]}),
new Symb("y",[1, 0],{'0,3': [1.3862943611198906, 2.772588722239781], '0,2': [1.0986122886681098, 2.1972245773362196], '0,1': [0.6931471805599453, 1.3862943611198906], '1,2': [0.4054651081081644, 0.8109302162163288], '1,3': [0.6931471805599453, 1.3862943611198906], '1,0': [-0.6931471805599453, -1.3862943611198906], '2,1': [-0.40546510810816444, -0.8109302162163289], '2,0': [-1.0986122886681098, -2.1972245773362196], '2,3': [0.28768207245178085, 0.5753641449035617]}),
];
var setList = [
new Set("t",[['1', '2', '3', '4']]),
new Set("n",[['A', 'B', 'C']]),
];
var series = ['demo1.gdx', 'demo2.gdx'];
*/

function State(color) {
	this.color = color;
}
var borderColor = new Array();
borderColor[0] = "rgb(254, 254, 254)";
//borderColor[1] = "rgb(0, 128, 255)";
borderColor[1] = "rgb(10, 10, 10)";

var borderStyle = new Array();
borderStyle[0] = "solid";
borderStyle[1] = "solid";

var borderWidth = new Array();
borderWidth[0] = "3px";
borderWidth[1] = "3px";

var fontWeightList = new Array();
fontWeightList[0] = 'normal';
fontWeightList[1] = 'bold';

var colorList = new Array();
colorList[0] = new State("rgb(255, 255, 255)");
colorList[1] = new State("rgb(204, 204, 0)");

function hslToString(hsl) {
	return "hsl("+hsl[0]+', '+hsl[1]+'%,'+hsl[2]+'%)';
}

function setState(obj, state) {
/*	if (obj.hsl[1] == 0) {
		obj.hsl[0] = 210*state;
		obj.hsl[2] = 100-50*state;
	} else
		obj.hsl[2] = 40+state*(80-40);
	obj.style.borderColor = hslToString(obj.hsl);*/
//	obj.style.borderColor = hslToString([0,100,(100+state*(50-100))]);
//	obj.style.fontWeight = fontWeightList[state];
	obj.style.borderStyle = borderStyle[state];
	obj.style.borderWidth = borderWidth[state];
	obj.style.borderColor = borderColor[state];
}

function createMenuTable(elemList, elemClick, hover) {
	var table = document.createElement("table");

	for (i=0;i<elemList.length;i++) {
		//insert a new row at the bottom
		var newRow = table.insertRow(i);
 
		//create new cells
		var newCell = newRow.insertCell(0);
		if (typeof(elemList[i]) == 'object') {
			newCell.innerHTML = elemList[i].name;
		} else {
			newCell.innerHTML = elemList[i];
		}			
//		newCell.style.margin = "-10px";
		newCell.style.borderStyle = borderStyle[0];
		newCell.style.borderWidth = borderWidth[0];
		newCell.style.borderColor = borderColor[0];
		newCell.style.cursor = 'default';
		newCell.hsl = [0,100,50];
		newCell.onclick = elemClick;
		if (hover) {
			newCell.onmouseover = elemClick;
		} else {
			newCell.onmouseover = highlight;
			newCell.onmouseout = dehighlight;
		}
		newCell.myId = i;
		//newCell.setAttribute('id',elemList[i]);
	}

	return table;
}

function highlight() { this.style.backgroundColor = "rgb(230,230,230)"; }
function dehighlight() { this.style.backgroundColor = "rgb(255,255,255)"; }

function getSetsSelection() {
	if (symbList.curr == undefined)
		return null;
	var activeSets = symbList[symbList.curr.myId].sets;
	var currSet;
	var currSelection = new Array();
	var bAll = true;
	for (j=0;j<activeSets.length;j++) {
		currSet = activeSets[j];
		if(setList[j].curr == undefined) {
			bAll = false;
			currSelection[j] = null;
		}
		else {
			currSelection[j] = setList[j].curr;
		}
	}
	if (!bAll)
		return null;
	return currSelection;
}

function updatePlot() {
	var currId = symbList.curr.myId;
	var currSymb = symbList[currId];
//	alert(setList.mask+":"+currSymb.mask+":"+(currSymb.mask & setList.mask));
	if ((currSymb.mask & setList.mask) == currSymb.mask) {
		var sets = currSymb.sets;
		xset = setList[sets[sets.length-1]]

		var dataHeader = new Array();
		dataHeader[0] = xset.name;
		var s;
		for (s=0;s<series.length;s++)
			dataHeader[s+1] = series[s];

		var indList = ''
		for (j=0;j<sets.length-1;j++) {
			indList = indList + setList[sets[j]].currId + ','
		}
		
		var xdata = xset.elems;
		var i;
		var dataBody = new Array();
//		var record = new Array();
		var xl = xdata.length;
		for(i=0;i<xl;i++) {
			dataBody[i] = new Array();
			dataBody[i][0] = xdata[i];
			dataRecord = currSymb.data[indList+i]
//			alert(indList+i+" : "+dataRecord);	
			if (dataRecord == undefined) {
				for (s=0;s<series.length;s++) {
					dataBody[i][s+1] = 0;
				}
			} else {
				for (s=0;s<series.length;s++) {
					dataBody[i][s+1] = dataRecord[s];
				}				
			}
		}
/*		var rep = '['
		for (i=0;i<dataBody.length;i++) {
			for (var j=0;j<dataBody[i].length;j++) {
				rep +='['+dataBody[i][0];
				for (var s=0;s<series.length;s++) {
					rep += ',[';
					for (var k=0;k<dataBody[i][s+1].length;k++) {
						rep += dataBody[i][s+1][k]+',';
					}
					rep +=']';
				}
				rep +='],';
			}
		}
		rep+=']';
		alert(rep);
*/
//		alert(dataBody);
//		var dataToPlot = dataHeader + dataBody;
//		alert(dataToPlot);
		if(symbList.g == undefined) {
			symbList.g = new Dygraph(
			  // containing div
			  document.getElementById("graphdiv"),
			  // CSV or path to a CSV file.
			  dataBody,
			  {
				  labels: dataHeader,
                  title: currSymb.lastElem.toUpperCase(),
				  xlabel: 'MaxDiff: '+currSymb.maxDiff+'; TempMaxDiff: '+currSymb.tempMaxDiff,
                  includeZero: true,
                  axes: {
                      x: {
                          axisLabelFormatter: function(val) {
                              return val.toFixed(0);
                          }
                      }
                  },
				  sigFigs: 3,
				  colorValue: 0.8,
				  strokeWidth: 3,
//				  customBars: true,
//				  errorBars: true
			  });
		} else {
			symbList.g.updateOptions(
				{
					file: dataBody,
					labels: dataHeader,
                    title: currSymb.lastElem.toUpperCase(),
					xlabel: 'MaxDiff: '+currSymb.maxDiff+'; TempMaxDiff: '+currSymb.tempMaxDiff,
				});
		}
					
	}
}

function getColor(preIndList,domId) {
	var currSymb = symbList[symbList.curr.myId];
	// check if color value already cache for current symbol
	var ret = symbList.values[domId][preIndList];

	if (ret != undefined) {
        if (! isNaN(ret)) {
		    currSymb.tempMaxDiff = Math.max(ret,currSymb.tempMaxDiff);
        }
		return ret;
	}
	// Otherwise...

	// base case
	var d;
	if (domId == (currSymb.sets.length-1)) {
		ret = -1;
		d = currSymb.data[preIndList];
		if (d != undefined) {
			for (var i=0; i<series.length;i++) {
				if ((d[i] != 0) && (! isNaN(d[i]))) {
					ret = 1;
					break;
				}
			}
			if (ret==1) {
				var cum = 0.0;
				for (i=d.length-1;i>=0;i--) {
                    if (isNaN(d[i])) continue;
					cum += d[i];
				}
				var avg = cum/d.length;
				cum = 0.0;
				for (i=d.length-1;i>=0;i--) {
                    if (isNaN(d[i])) continue;
					cum += Math.pow(d[i]-avg,2);
				}
				ret = cum;
                if (! isNaN(ret)) {
				    currSymb.tempMaxDiff = Math.max(ret,currSymb.tempMaxDiff);
                }
			}
		}
//		alert('preIndList: '+preIndList+'; domId: '+domId+'; data: '+currSymb.data[preIndList]+'; ret: '+ret);
	} else {
		domId += 1;
		var currSet = setList[currSymb.sets[domId]];
		var checkData = 0;
		// recursive step
		if (preIndList != '')
			preIndList +=',';
		var tempPreIndList;
		ret = -1;
		var dataCum = 0; 
		var missingCount = 0;
		var tempRet;
		for (var i=0; i<currSet.elems.length; i++) {
			tempPreIndList = preIndList+i;
			tempRet = getColor(tempPreIndList, domId);
			if (tempRet == -1) {
				missingCount++;
				tempRet = 0;
			}
			dataCum += tempRet;
//			alert('domId: '+domId+'tempPreIndList: '+tempPreIndList+'; ret: '+tempRet+'; dataCum: '+dataCum);			
		}
		if (missingCount<currSet.elems.length) {
			ret = dataCum;
		}
	}
	symbList.values[domId][preIndList] = ret;
	return ret;
}

function colorMap(v) {
	if (v<0) {
		v=0;
	} else if (v>1) {
		v=1;
	}
	return (210*(1-Math.log(1.0+v*(Math.E-1))));
//	return (120*(2-Math.exp(Math.log(2)*v)));
//	return (120*(1-v));
}

function setOnClick() {
	setClick(this);
}
function setClick(cell) {
	// tr -> tbody -> table
	var domTable = cell.parentNode.parentNode.parentNode;
	var domId = domTable.domId;

	var currSetId = domTable.myId;
	var currSet = setList[currSetId];
	var prev = currSet.curr;
	if (prev != undefined)
		setState(prev,0);
	currSet.curr = cell;
	currSet.currId = cell.myId;
	
	var currSymb = symbList[symbList.curr.myId];
	currSymb.tempMaxDiff = 0;
    currSymb.lastElem = cell.innerHTML
	for (var i=domId+1; i<(currSymb.sets.length-1); i++) {
		colorColumn(i);
	}
	setState(cell,1);
	
	setList.mask |= 1<<currSetId;
//	alert('currSymb.mask: '+currSymb.mask+', setList.mask: '+setList.mask);		
	updatePlot();
}

function colorColumn(j) {
//	alert(symbList.curr.myId);
	var currSymb = symbList[symbList.curr.myId];
	if (j==(currSymb.sets.length-1))
		return;
	var currSet = setList[currSymb.sets[j]];
	var preIndList = '';
	for (var i=0;i<j;i++) {
		preIndList += setList[currSymb.sets[i]].currId+',';
	}
	var tempPreIndList;
	var vcol = new Array(currSet.elems.length);
	var vmax = -1;
	for (var i=0;i<currSet.elems.length;i++) {
		tempPreIndList  = preIndList+i;
		vcol[i] = getColor(tempPreIndList,j);
//		alert(tempPreIndList+': '+vcol[i]);
		if ((vcol[i] != -1) && (! isNaN(vcol[i]))) {
			if (vmax == -1)
				vmax = vcol[i];
			else
				vmax = Math.max(vcol[i],vmax);
		}
//		alert('preIndList: '+tempPreIndList+'; j: '+j+'; vcol: '+vcol);
	}	
	currSymb.maxDiff = Math.max(vmax,currSymb.maxDiff);
	for (var i=0;i<currSet.elems.length;i++) {
		var hsl = currSet.currTable.rows[i].cells[0].hsl;
		if (vcol[i] != -1) {
			var r = 0;
			if (vmax>0)
				r = vcol[i]/vmax;
			h = colorMap(r)
			hsl[0] = h;
            //hsl[0] = 200;
            //hsl[1] = 255-h;
		    currSet.currTable.rows[i].style.display = 'table-row';
			currSet.currTable.rows[i].style.backgroundColor = hslToString(hsl);
            /*text_hsl = hsl.slice(0);
            text_hsl[0] = ((255*hsl[0]+125) % 255);
            text_hsl[1] = 200;
            text_hsl[2] = 200;
			currSet.currTable.rows[i].style.color = hslToString(text_hsl);*/
			currSet.currTable.rows[i].style.color = "rgb(255, 255, 255)";
		} else {
			currSet.currTable.rows[i].style.display = 'none';
			currSet.currTable.rows[i].style.backgroundColor = "rgb(255,255,255)";
			currSet.currTable.rows[i].style.color = "rgb(200, 200, 200)";
		}
	}
}

function symbClick() {
//alert(this.innerHTML);
	var prev = symbList.curr;
	symbList.curr = this;
	if (prev != undefined) {
		setState(prev, 0);
	}
	var i, j, trmenus;
	var newMenu, newMenuTable, currSet;
	var currSymb = symbList[this.myId];
	var sets = currSymb.sets;
	if (symbList.values != undefined)
		delete symbList.values;
	symbList.values = new Array(sets.length);
	for (i=0;i<sets.length;i++) {
		symbList.values[i] = {};
	}
	
	// write headers
	trmenus = document.getElementById("menus").rows[0];
	for (j=trmenus.cells.length-1;j>0;j--) {
		trmenus.deleteCell(j);
	}	
	for (j=0;j<sets.length-1;j++) {
		currSet = setList[sets[j]];
		newCell = document.createElement('th');
		newCell.innerHTML = currSet.name;
		trmenus.appendChild(newCell);
	}

	// write elements list
	trmenus = document.getElementById("menus").rows[1];
	for (j=trmenus.cells.length-1;j>0;j--) {
		trmenus.deleteCell(j);
	}	
	var cellsToSelect = new Array(sets.length-1);
	for (j=0;j<sets.length-1;j++) {
		currSet = setList[sets[j]];
		newCell = trmenus.insertCell(j+1);
//		newCell.style.height = "100%";
		newDiv = document.createElement('div');
		newDiv.className = "myCol"
		newDiv.style.overflow = 'auto';
		newDiv.style.paddingRight = '20px';
		newDiv.style.paddingLeft = '20px';
		newMenuTable = createMenuTable(
			currSet.elems,
			setOnClick,true);
		newMenuTable.myId = sets[j];
		newMenuTable.domId = j;
		
		currSet.currTable = newMenuTable;

		var activeId = 0;
		if (currSet.currId != undefined) {
			activeId = currSet.currId;
		}
		cellsToSelect[j] = newMenuTable.rows[activeId].cells[0];
//		currSet.curr = cellToSelect;
//		setState(cellToSelect,1);
		
		newDiv.appendChild(newMenuTable);
		newCell.appendChild(newDiv);
	}

	colorColumn(0);
	for (j=0;j<sets.length-1;j++) {
		setClick(cellsToSelect[j]);		
	}
	if (symbClick.graphTitle == undefined)
		symbClick.graphTitle = document.getElementById('graphtitle');
	symbClick.graphTitle.innerHTML = currSymb.desc;
	setState(this, 1);
	resizeColumns();
	updatePlot();
}



function init(){
	// init variables
	setList.mask = 0;
	newDiv = document.createElement('div');
	newDiv.className = "myCol"
	newDiv.style.overflow = 'auto';
	newDiv.style.paddingRight = '20px';
	newDiv.style.paddingLeft = '5px';
	
	//get the symbTableDiv
	var symbTable = createMenuTable(
		symbList,symbClick,false);
	newDiv.appendChild(symbTable)
	document.getElementById("symbMenu").appendChild(newDiv);
	window.onresize = resizeColumns();
}

function resizeColumns() {
	var divs = document.getElementsByClassName('myCol');
	for (var i=0; i<divs.length; i++) {
		divs[i].style.height = window.innerHeight*0.9;
	}
//	document.title = 'Height: '+(window.innerHeight*0.9);
}
