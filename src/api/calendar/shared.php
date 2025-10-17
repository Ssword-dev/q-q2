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



function c_getMonth($year, $month, $country = 'ph', $subdivision = null, $holidays = null)
{
    $numberOfDays = cal_days_in_month(CAL_GREGORIAN, $month, $year);

    // a whole matrix.
    $meta_days = [
        [null, null, null, null, null, null, null],
        [null, null, null, null, null, null, null],
        [null, null, null, null, null, null, null],
        [null, null, null, null, null, null, null],
        [null, null, null, null, null, null, null],
        [null, null, null, null, null, null, null],
    ];

    $currentDay = 1;
    $index = c_getWeekdayIndex($year, $month, 1);
    $y = 0;
    // while loop (: could be done in for loop but this is required.
    while ($y < 6) {
        $x = 0;
        while ($x < 7) {
            // for the first row,
            // if x is less than the index,
            // then point x to the index.
            if ($y === 0 && $x < $index) {
                $x = $index;
                continue;
            }

            // if the current day is gteq to number of days,
            // then break. limit has been reached.
            if ($currentDay >= $numberOfDays) {
                break;
            }

            $meta_days[$y][$x] = [
                'day' => $currentDay,
            ];

            $currentDay++;
            $x++;
        }

        $y++;
    }

    return [
        'number_of_days' => $numberOfDays,
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

// function c_getHolidays($country, $state, $year)
// {
//     $url = "http://localhost:4000/api/node/holidays/$year/$country?state=$state";

//     $ch = curl_init($url);
//     curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

//     $response = curl_exec($ch);

//     if ($response === false) {
//         die("cURL Error: " . curl_error($ch));
//     }

//     curl_close($ch);

//     $data = json_decode($response, true);
//     return $data;
// }

function c_getYear($country, $state, $year)
{
    $meta_months = [];
    $month = 1;
    $numberOfDaysInFebruary = cal_days_in_month(CAL_GREGORIAN, 2, $year);

    while ($month <= 12) {
        $meta_months[] = c_getMonth($year, $month, $country, $state, $holidays);
        $month++;
    }

    return [
        'year' => $year,
        'leap_year' => $numberOfDaysInFebruary === 29,
        'months' => $meta_months,
        'zodiac' => [
            'chinese' => c_getChineseZodiacAnimal($year)
        ],
        // 'holidays' => c_getHolidays($country, $state, $year)
    ];
}