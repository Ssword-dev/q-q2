<?php

include '../utils.php';

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    sendError(401, "Bad Request");
}



