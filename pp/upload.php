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
function updateStatus()
{

}
function runs(){
  var di = document.getElementById("right-crsl");
  var xmlHttp = new XMLHttpRequest();
  var p = document.getElementById('sts');
  p.innerHTML = 'connecting';
  xmlHttp.onreadystatechange = function()
  {
    var i = 0;
    var status = 0;
    var myVar = setInterval(function(){
      msg = readTextFile('status.xml');
      var p = document.getElementById('sts');
      console.log(msg);
      p.innerHTML = msg;
    if(this.readyState==4 && this.status == 200)
    {

        if(msg == '1')
        {
          console.log('Script Ended');
          clearInterval(myVar);
          console.log(i);
          if(status == 0)
          { var segmentedPics = <?php $out = array();
          foreach (glob('./segmented_data/mitotic/*.jpg') as $filename) {
              $p = pathinfo($filename);
              $out[] = $p['filename'];
          }
          echo json_encode($out); ?>;
          var div = document.getElementById("right-crsl");
          for(var i in segmentedPics){
            var z = document.createElement("img");
            z.onclick =function(event){
                var yz = event.target.src;
                //alert(yz);
                var yx=document.getElementById("pop");
                yx.style.display="block";
                var yy=document.getElementById("pic");
                yy.src=yz;
            };
            z.onmouseout = function () {
              var xx = document.getElementById("pop");
              xx.style.display="None";
              };
            z.src='./segmented_data/mitotic/'+segmentedPics[i]+'.jpg';
            z.zIndex = 200;
            z.draggable="true";
            z.ondragstart="drag(event)";
            div.appendChild(z);
          }
        }
      }
      },30);
      console.log(this.readyState);
      console.log(this.responseText);
      //alert(this.readyState);
      //alert(this.responseText);
    }

  };
  xmlHttp.open("POST","blackandwhite.php?image=" + data,true);
  xmlHttp.send();
}
