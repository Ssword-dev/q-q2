<?php

function c_getDaysInMonth($y, $m)
{
    return cal_days_in_month(CAL_GREGORIAN, $m, $y);
}

function c_getWeekdayIndex($year, $month, $day)
{
    $date = new DateTime("$year-$month-$day");
    return (int) $date->format("w"); // 0=Sun, 1=Mon, ..., 6=Sat
}


function c_getMonth($year, $month)
{
    $days = cal_days_in_month(CAL_GREGORIAN, $month, $year);
    $meta_days = [];
    $currentDay = 1;
    $index = c_getWeekdayIndex($year, $month, 1);

    // while loop (: could be done in for loop but this is required.
    while ($currentDay <= $days) {
        $dt = new DateTimeImmutable("$year-$month-$currentDay");
        $timestamp = (int) $dt->format('U');
        $meta_days[] = [
            'day' => $currentDay,
            'timestamp' => $timestamp,
            'index' => (
                    // mod by 7 so its sunday then its 0,
                    // basically this is faster.
                (
                    // index plus the current day. since not 0 based,
                    // have to add -1 or $currentDay - 1
                    $index + ($currentDay - 1)
                )
                % 7
            )
        ];
        $currentDay++;
    }

    return [
        'year' => $year,
        'month' => $month,
        'baseIndex' => $index,
        'days' => $meta_days
    ];
}

$chineseZodiacAnimals = [
    'rat',
    'ox',
    'tiger',
    'rabbit',
    'dragon',
    'snake',
    'horse',
    'goat',
    'monkey',
    'rooster',
    'dog',
    'pig',
];

function c_getChineseZodiacAnimal($year)
{
    global $chineseZodiacAnimals;
    return $chineseZodiacAnimals[($year - 1960) % 12];
}

function c_getHolidays($country, $subdiv, $year)
{
    $url = "http://localhost:5000/api/holidays/$country/$year?subdiv=$subdiv";

    $ch = curl_init($url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

    $response = curl_exec($ch);

    if ($response === false) {
        die("cURL Error: " . curl_error($ch));
    }

    curl_close($ch);

    $data = json_decode($response, true);
    return $data;
}

function c_getYear($country, $subdiv, $year)
{
    $meta_months = [];
    $month = 1;
    $numberOfDaysInFebruary = cal_days_in_month(CAL_GREGORIAN, 2, $year);

    while ($month <= 12) {
        $meta_months[] = c_getMonth($year, $month);
        $month++;
    }

    return [
        'year' => $year,
        'leap_year' => $numberOfDaysInFebruary === 29,
        'months' => $meta_months,
        'zodiac' => [
            'chinese' => c_getChineseZodiacAnimal($year)
        ],
        'holidays' => c_getHolidays($country, $subdiv, $year)
    ];
}