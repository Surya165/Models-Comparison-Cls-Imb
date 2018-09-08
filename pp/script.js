

var list=["intro","abstract","dataset","segment","brh","gbtuom","otsu","mo","ffl","wac","dio","dir","2pt","p1","km","aug","p2","f-m","adv","ada","impl","cs","encode","ocs"];
//var pics = ["2.jpeg","3.jpeg","2.jpeg","2.jpeg","2.jpeg","2.jpeg","2.jpeg","2.jpeg","2.jpeg","2.jpeg","2.jpeg","2.jpeg","2.jpeg","2.jpeg","2.jpeg","2.jpeg"];
var index=0;
var fs = require('fs');
var files = fs.readdirSync('./');
var x=0;
var data;
/*function view(n){
  x=x+n;
  var y= document.getElementById(list[x]);
  y.style.display="block";
}*/



function change(event){
  var w = event.keyCode || event.which;
  var y;
  if(w==37 || w==38){
    index = index-1;
    if(index < 0){
      index=0;
    }
    for(var j=0;j< list.length;j++){
      y = document.getElementById(list[j]);
      y.style.display="None";
    }
    y = document.getElementById(list[index]);
    y.style.display="block";
  }
  if(w==39 || w==40){
    index=index+1;
    if(index>=list.length){
      index=(list.length)-1;
    }
    for(var j=0;j< list.length;j++){
      y = document.getElementById(list[j]);
      y.style.display="None";
    }
    y = document.getElementById(list[index]);
    y.style.display="block";
  }
}


//drag and drop
function allowDrop(ev){
  ev.preventDefault();
}

function drag(ev){
  console.log("dragiing");
  var x= ev.target.src;
  ev.dataTransfer.setData("text",x);

}

function drop(ev){
  ev.preventDefault();
  data = ev.dataTransfer.getData("text");
  data = data.substring(17, data.length);
  data = "../../" + data
  ev.target.src=data;
}

//runs
function alertFunc(message) {
  alert(message);
}
