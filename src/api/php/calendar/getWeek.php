<?php

require "../utils.php";
require "./shared.php";


if ($_SERVER['REQUEST_METHOD'] !== 'GET') {
    sendError(400, "Bad Method.");
}

if (!(isset($_GET['year']) && isset($_GET['month']))) {
    sendError(400, "Bad Request.");
}

// variables
$year = $_GET['year'];
$month = $_GET['month'];

// try to parse both as int. 

foreach ([$year, $month] as $shouldBeStringInteger) {
    try {
        $shouldBeStringInteger - 0;
    } catch (_) {
        sendError(400, "Bad Query.");
    }
}

sendJSONResponse(200, c_getMonth($year - 0, $month - 0));