var pics = <?php $out = array();
foreach (glob('../../dataset/A00_v2/*.jpg') as $filename) {
    $p = pathinfo($filename);
    $out[] = $p['filename'];
}
echo json_encode($out); ?>;
function upload(){
  var y = document.getElementById("left-crsl");
  y.style.display="block";
  var div = document.getElementById("left-crsl");
  for(var i in pics){
    var z = document.createElement("img");
    z.onclick =function(event){
        console.log("hi");
        var yz = event.target.src;
        //alert(yz);
        var yx=document.getElementById("pop");
        yx.style.display="block";
        var yy=document.getElementById("pic");
        yy.src=yz;
    };
    z.onmouseout=function () {
      var xx=document.getElementById("pop");
      xx.style.display="None";
      };
    z.src='../../dataset/A00_v2/'+pics[i]+'.bmp';
    z.zIndex = 200;
    z.draggable="true";
    z.ondragstart="drag(event)";
    div.appendChild(z);
  }
}

function readTextFile(file)
{
    var rawFile = new XMLHttpRequest();
    rawFile.open("GET", file, true);
    var msg = 'end';
    rawFile.onreadystatechange = function ()
    {
        if(rawFile.readyState == 4)
        {
            if(rawFile.status == 200 || rawFile.status == 0)
            {
                //alert(file);

                var allText = rawFile.responseXML;
                response = allText.getElementsByTagName('msg');
                var p = document.getElementById('sts');
                msg = response[0].childNodes[0].nodeValue;
                p.innerHTML = msg;

            }
        }
    }
    rawFile.send();
    return msg;
}
function runs(){
  var di = document.getElementById("right-crsl");
  var xmlHttp = new XMLHttpRequest();
  var p = document.getElementById('sts');
  p.innerHTML = 'connecting';
  xmlHttp.onreadystatechange = function()
  {
    myVar = setInterval(function(){

      var msg = readTextFile('status.xml');

      var str = 'end';
      if(msg == str)
      {
        clearInterval(myVar);
        alert('Ending script');
        for(var i in segmentedPics){
          var z = document.createElement("img");
          z.onmouseover =function(event){
              console.log("hi");
              var yz = event.target.src;
              //alert(yz);
              var yx=document.getElementById("pop");
              yx.style.display="block";
              var yy=document.getElementById("pic");
              yy.src=yz;
          };
          z.onmouseout=function () {
            var xx=document.getElementById("pop");
            xx.style.display="None";
            };
          z.src='./segmented_data/non_mitotic/'+segmentedPics[i]+'.jpg';
          z.zIndex = 200;
          div.appendChild(z);
        }
      }
    }, 3);

    var y = document.getElementById("right-crsl");
    y.style.display="block";
    var div = document.getElementById("right-crsl");
    if(this.readyState == 4 && this.status == 200)
    {

      //clearInterval(myVar);
      var segmentedPics = <?php $out = array();
      foreach (glob('./segmented_data/non_mitotic/*.jpg') as $filename) {
          $p = pathinfo($filename);
          $out[] = $p['filename'];
      }
      echo json_encode($out); ?>;


      alert(this.responseText);




      }
  }
  xmlHttp.open("POST","blackandwhite.php?image=" + data,true);
  xmlHttp.send();
}
