<?php
$imageAddress = $_REQUEST['image'];
//echo $imageAddress;
//exec('chmod 777 blackandwhite.jpg');
$img= shell_exec('python3 blackandwhite.py '.$imageAddress);

 ?>
