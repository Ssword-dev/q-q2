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

function c_getMonthMatrix($year, $month, $country = 'ph', $subdivision = null, $holidays = null)
{
    $days = cal_days_in_month(CAL_GREGORIAN, $month, $year);
    $meta_days = [];
    $currentDay = 1;
    $index = c_getWeekdayIndex($year, $month, 1);

    for ($i = 0; $i <= $index; $i++) {
        $meta_days[] = null; // pad. so that the client does not have to further compute anything.
    }

    if (!$holidays) {
        $holidays = c_getHolidays($country, $subdivision, $year);
    }

    // while loop (: could be done in for loop but this is required.
    $limit = 7 * 6;
    $y = 0; // y axis.
    while (true) {
        $x = 0; // x axis
        $dt = new DateTimeImmutable("$year-$month-$currentDay");
        $timestamp = (int) $dt->format('U');

        $meta_day = [
            'day' => $currentDay,
            'timestamp' => $timestamp,
            'index' => (
                    // mod by 7 so its sunday then its 0,
                    // basically this is faster than calling cal_* api.
                (
                    // index plus the current day. since not 0 based,
                    // have to add -1 or $currentDay - 1
                    $index + ($currentDay - 1)
                )
                % 7
            )
        ];

        $maybeHolidayKey = $dt->format("Y-m-d");
        $isHoliday = isset($holidays[$maybeHolidayKey]);

        // add holiday metadata if applicable.
        if ($isHoliday) {
            $meta_day['holidayMetadata'] = $holidays[$maybeHolidayKey];
        }

        $meta_day['isHoliday'] = $isHoliday;
        $meta_days[] = $meta_day;
        $currentDay++;
    }

    return [
        'year' => $year,
        'month' => $month,
        'baseIndex' => $index,
        'days' => $meta_days
    ];
}


function c_getMonth($year, $month, $country = 'ph', $subdivision = null, $holidays = null)
{
    $days = cal_days_in_month(CAL_GREGORIAN, $month, $year);
    $meta_days = [];
    $currentDay = 1;
    $index = c_getWeekdayIndex($year, $month, 1);

    if (!$holidays) {
        $holidays = c_getHolidays($country, $subdivision, $year);
    }

    // while loop (: could be done in for loop but this is required.
    while ($currentDay <= $days) {
        $dt = new DateTimeImmutable("$year-$month-$currentDay");
        $timestamp = (int) $dt->format('U');

        $meta_day = [
            'day' => $currentDay,
            'timestamp' => $timestamp,
            'index' => (
                    // mod by 7 so its sunday then its 0,
                    // basically this is faster than calling cal_* api.
                (
                    // index plus the current day. since not 0 based,
                    // have to add -1 or $currentDay - 1
                    $index + ($currentDay - 1)
                )
                % 7
            )
        ];

        $maybeHolidayKey = $dt->format("Y-m-d");
        $isHoliday = isset($holidays[$maybeHolidayKey]);

        // add holiday metadata if applicable.
        if ($isHoliday) {
            $meta_day['holidayMetadata'] = $holidays[$maybeHolidayKey];
        }

        $meta_day['isHoliday'] = $isHoliday;
        $meta_days[] = $meta_day;
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

function c_getHolidays($country, $state, $year)
{
    $url = "http://localhost:4000/api/node/holidays/$year/$country?state=$state";

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
    $holidays = c_getHolidays($country, $subdiv, $year);

    while ($month <= 12) {
        $meta_months[] = c_getMonth($year, $month, $country, $subdiv, $holidays);
        $month++;
    }

    return [
        'year' => $year,
        'leap_year' => $numberOfDaysInFebruary === 29,
        'months' => $meta_months,
        'zodiac' => [
            'chinese' => c_getChineseZodiacAnimal($year)
        ],
    ];
}