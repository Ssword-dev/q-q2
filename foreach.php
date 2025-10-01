<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>

<body>
    <form action="" method="POST">
        <label for="name">
            Input your name:
        </label>
        <input type="text" name="name">
        <br />
        <label for="grades">
            Input your grades for each subject, comma seperated:
        </label>
        <input type="text" name="grades">
        <br />
        <button type="submit">Submit</button>
    </form>
    <?php
    // // hindi mag ooutput pag wala yung grades at name.
    // if (isset($_POST['name']) && isset($_POST['grades'])) {
    //     // retrieve user input. kapag parehas meron. bawal
    //     // isa lang. di dapat pinapaasa ang isa't isa (:
    //     $name = $_POST['name'];
    //     $unsafe_grades = $_POST['grades'];
    
    //     // ahem. regex.
    //     // leading digit, trailing digits
    //     // can have underscores and spaces.
    //     if (!preg_match("/[\s\d_]+(\,[\s\d_]+)?/", (string) $unsafe_grades)) {
    //         echo "Invalid Format";
    //         die(1);
    //     }
    
    //     // accumulator. pero sa grades.
    //     $total_grade = 0;
    
    //     // ','.split(unsafe_grades) in python and unsafe_grades.split(',') in javascript
    //     $grades = explode(",", $unsafe_grades);
    
    //     // calculate total grades.
    //     foreach ($grades as $grade) {
    //         // replace every single space and underscores.
    //         $total_grade += (int) str_replace([" ", "_"], "", $grade);
    //     }
    
    //     // the number of subjects is the number of grades provided.
    //     $subjects = count($grades);
    
    //     // divide sa number ng subjects for average (:
    //     $ave = $total_grade / $subjects;
    
    //     // echo. using string interpolation (: like `${name} your average is ${ave}`
    //     // or f"{name} your average is {ave}" in python.
    //     echo "$name your average is $ave";
    // }
    
    function getItemsFromInputString($s)
    {
        return explode(",", $s);
    }
    ;


    // hindi mag ooutput pag wala yung grades at name.
    if (isset($_POST['name']) && isset($_POST['grades'])) {
        // retrieve user input. kapag parehas meron. bawal
        // isa lang. di dapat pinapaasa ang isa't isa (:
        $unsafe_names = $_POST['name'];
        $unsafe_grades = $_POST['grades'];

        // ahem. regex.
        // leading digit, trailing digits
        // can have underscores and spaces.
        if (!preg_match("/[\s\d_]+(\,[\s\d_]+)?/", (string) $unsafe_grades)) {
            echo "Invalid Format";
            die(1);
        }

        $names = getItemsFromInputString($unsafe_names);
        $grades = getItemsFromInputString($unsafe_grades);

        if (count($names) !== count($grades)) {
            echo "Number of names and average grades must be equal.";
        }

        foreach (range(0, count($names) - 1) as $idx) {
            $name = $names[$idx];
            $grade = $grades[$idx];
            echo "$name: $grade";
        }
    }
    ?>
</body>

</html>