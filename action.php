<?php
$command = escapeshellcmd('python Script.py '.$_POST["k"].' "'.$_POST["query"].'"');
$output = shell_exec($command);
echo $output
?>