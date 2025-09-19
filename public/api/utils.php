<?php

function execQuery(mysqli $conn, string $template, string $types, ...$parameters)
{
    $stmt = $conn->prepare(
        $template
    );
    $stmt->bind_param($types, ...$parameters);
    $stmt->execute();
}


function fetchQuery(mysqli $conn, string $template, string $types = '', ...$parameters): ?array
{
    $stmt = $conn->prepare($template);
    if (!$stmt) {
        throw new Exception("Prepare failed: " . $conn->error);
    }

    if ($types && $parameters) {
        $stmt->bind_param($types, ...$parameters);
    }

    $stmt->execute();

    $result = $stmt->get_result();
    if ($result) {
        return $result->fetch_all(MYSQLI_ASSOC);
    }

    return null; // error
}


function readRequestBody()
{
    $body = file_get_contents(REQUEST_BODY_URL);
    return $body; // if it fails, it returns false.
}

function readRequestBodyJson()
{
    $body = readRequestBody();

    if ($body === false) {
        return null; // error.
    }

    try {
        return json_decode($body, true, 512, JSON_THROW_ON_ERROR); // associative
    } catch (Throwable $_) {
        return null; // error.
    }
}


function sendError($statusCode, $message = null): never
{
    // tell client im sending json.
    header("Content-Type: application/json");

    // give client the error, message is optional.
    echo json_encode([
        'type' => 'error',
        'message' => $message
    ]);

    // set the response code.
    http_response_code($statusCode);
    die(0); // exit sucessfully
}


function sendJSONResponse($statusCode, $assocArrayOrPrimitive = null, $exit = true): never
{
    // tell client im sending the specified content type
    header("Content-Type: application/json");

    // set the response code.
    http_response_code($statusCode);


    echo json_encode($assocArrayOrPrimitive);


    if ($exit) {
        die(0);
    }
}