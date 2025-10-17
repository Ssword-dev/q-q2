<?php

require_once '../utils.php';

$table = [];

$lim = $_GET['limit'];

$y = 1;

while ($y <= $lim) {
    $x = 1;
    $row = [];

    while ($x <= $lim) {
        $row[] = $x * $y;
        $x++;
    }

    $table[] = $row;
    $y++;
}

sendJSONResponse(200, $table);