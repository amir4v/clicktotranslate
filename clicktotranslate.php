<?php

exec("./home/s/dev/clicktotranslate/do.sh &", $output, $return_var);
var_dump($output);
var_dump($return_var);

echo "Done!";

header("Location: http://127.0.0.1:8000/");
die();

?>
