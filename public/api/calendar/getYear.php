<?php

require "../utils.php";
require "./shared.php";


if ($_SERVER['REQUEST_METHOD'] !== 'GET') {
    sendError(400, "Bad Method.");
}

if (!isset($_GET['year'])) {
    sendError(400, "Bad Request.");
}

// variables
$year = $_GET['year'];
// try to parse both as int. 


try {
    $year - 0;
} catch (_) {
    sendError(400, "Bad Query.");
}


header("Cache-Control: max-age=28800"); // tell browser to cache for an 8 hours.
sendJSONResponse(200, c_getYear($year - 0));