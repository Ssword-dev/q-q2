<?php

use Ssword\DataAnalysis\DataFrame;

include '../utils.php';

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    sendError(401, "Bad Request");
}

// {
//  "students": [
//      "<name:string>", <score:string>
//  ],
//  "configuration": {
//      "max-score": <int>,
//  }
// }

$body = readRequestBodyJson();

$students = $body['students'];
$config = $body['configuration'];

$maxScore = $config['max-score'];

$studentDatas = [
    'name' => [],
    'percentage' => [],
    'score' => []
];

foreach ($students as $student) {
    $name = $student[0];
    $score = $student[1];

    $studentDatas['name'][] = $name;
    $studentDatas['score'][] = $score;
    $studentDatas['percentage'] = 100 * ($score / $maxScore);
}

$studentDataDataframe = new DataFrame($studentDatas);

$summary = [
    'mean' => $studentDataDataframe->mean('score'),
    'median' => $studentDataDataframe->median('score'),
    'mode' => $studentDataDataframe->mode('score'),
];

$passers = $studentDataDataframe->query()->where(fn($s) => $s['percentage'] >= 75)->finalize();
$failers = $studentDataDataframe->query()->where(fn($s) => $s['percentage'] < 75)->finalize();

// TODO: Actually hook this up to frontend.