<?php
$imageAddress = $_REQUEST['image'];
//echo $imageAddress;
//exec('chmod 777 blackandwhite.jpg');
$command = 'python3 segmentTest.py '.$imageAddress.' 2>&1';
//$ls = system($command,$returnValue);
echo $command;
