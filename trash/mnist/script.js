var list=["intro","encode","ada"];
var pics = ["2.jpeg","2.jpeg","2.jpeg","2.jpeg","2.jpeg","2.jpeg","2.jpeg","2.jpeg","2.jpeg","2.jpeg","2.jpeg","2.jpeg","2.jpeg","2.jpeg","2.jpeg","2.jpeg"];
var index=-1;
var x=0;
/*function view(n){
  x=x+n;
  var y= document.getElementById(list[x]);
  y.style.display="block";
}*/

function upload(){
  var y = document.getElementById("left-crsl");
  y.style.display="block";
  var div = document.getElementById("left-crsl");
  for(var i in pics){
    var z = document.createElement("img");
    z.src=pics[i];
    div.appendChild(z);
  }
}

function change(event){
  var w = event.keyCode || event.which;
  var y;
  for(var j=0;j<list.length;j++){
    y = document.getElementById(list[j]);
    y.style.display="None";
  }
  if(w==37 || w==38){
    index = index-1;
    if(index<0){
      index=0;
    }
    y = document.getElementById(list[index]);
    y.style.display="block";
  }
  if(w==39 || w==40){
    index=index+1;
    if(index>=list.length){
      index=(list.length)-1;
    }
    y = document.getElementById(list[index]);
    y.style.display="block";
  }
}
