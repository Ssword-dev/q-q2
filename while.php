<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
    <style>
        .while,
        .dowhile,
        .for {
            width: calc(100% * (1/3));
            height: 100%;
            border: 2px solid black;
        }

        /* .while {
            left: 5vw;
        }

        .dowhile {
            left: 50vw;
        }

        .for {
            left: 60vw;
        } */

        .flex-container {
            display: flex;
            width: 100vw;
            height: 100vh;
            align-items: center;
            justify-content: space-between;
            flex-grow: 1;
        }

        table,
        tr,
        td {
            border: 2px solid black;
        }
    </style>
</head>

<body>
    <!-- <div class="flex-container">
        <div class="while">
            <span>while</span>
            <?php
            $counter = 10;
            while ($counter < 10) {
                echo $counter;
                // echo "<br>";
                $counter++;
            }
            ?>
        </div>

        <div class="dowhile">
            <span>do while</span>
            <?php
            $counter2 = 10;
            do {
                echo $counter2;
                // echo "<br>";
                $counter2++;
            } while ($counter2 < 10)
            ?>
        </div>
        <div class="for">
            <span>for</span>
            <?php
            // $acc = 0;
            // for ($counter3 = 1; $counter3 <= 10; $counter3++) {
            //     echo $counter3;
            //     echo "<br>";
            // }
            // $acc = 0;
            // $lim = 5;
            // for ($counter3 = 1; $counter3 <= $lim; $counter3++) {
            //     $acc += $counter3;
            // }
            // $acc = 1;
            // $lim = 5;
            // for ($counter3 = 1; $counter3 <= $lim; $counter3++) {
            //     $acc *= $counter3;
            // }
            // echo $acc;
            ?>
        </div> -->
    <br>
    <table>
        <tbody>
            <?php
            // $acc = 0;
            // for ($counter3 = 1; $counter3 <= 10; $counter3++) {
            //     echo $counter3;
            //     echo "<br>";
            // }
            // $acc = 0;
            // $lim = 5;
            // for ($counter3 = 1; $counter3 <= $lim; $counter3++) {
            //     $acc += $counter3;
            // }
            $lim = 30;
            for ($counter3 = 1; $counter3 <= $lim; $counter3++) {
                echo "<td>$counter3</td>";
                if ($counter3 % 10 === 0) {
                    if ($counter3) {
                        echo "</tr>";
                    }

                    if ($counter3 !== $lim) {
                        echo "<tr>";
                    }
                }
            }
            ?>
        </tbody>
    </table>
    </div>
</body>

</html>