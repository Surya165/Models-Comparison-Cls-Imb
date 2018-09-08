<?php
$imageAddress = $_REQUEST['image'];
//echo $imageAddress;
//exec('chmod 777 blackandwhite.jpg');
$command = 'python3 blackandwhite.py '.$imageAddress.' 2>&1';
$ls = system($command,$returnValue);
echo $ls;
