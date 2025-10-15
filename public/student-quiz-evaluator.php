<?php

$mode = null;

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // get internal flag.
    if (isset($_POST['phase-state-get-records'])) {
        $mode = 'get-records';
    } else if (isset($_POST['phase-state-evaluate'])) {
        $mode = 'evaluate';
    }
} else {
    $mode = 'get-number-of-students';
}

$bodyContentRenderers = [
    // renderer for the first phase
    'get-number-of-students' => function () {
        return "
            <form class='number-of-student-form form' method='POST'>
                <div class='form-card has-depth apply-horizon'>
                    <div class=\"form-field\">
                        <label class=\"\" for=\"number-of-students\">Enter the number of students:</label>
                        <input type=\"number\" name=\"number-of-students\" id=\"number-of-students\" />
                    </div>
                    <button class=\"has-depth form-action\" type=\"submit\">Submit</button>
                </div>
                <!-- DO NOT REMOVE! INTERNAL FLAG. -->
                <input hidden name=\"phase-state-get-records\" value=\"true\" />
            </form>
            ";
    },
    'get-records' => function () {
        $numberOfStudents = $_POST['number-of-students'];
        $studentFormFields = '';

        for ($i = 1; $i <= $numberOfStudents; $i++) {
            $studentFormFields .= "
            <div id=\"student-{$i}\">
                <div class=\"form-field\">
                    <label class=\"\" for=\"student-{$i}-name\">Enter the name of the student:</label>
                    <input type=\"number\" id=\"student-{$i}-name\" />
                </div>
                <div class=\"form-field\">
                    <label class=\"\" for=\"student-{$i}-score\">The score of the student:</label>
                    <input type=\"number\" id=\"student-{$i}-score\" />
                </div>
            </div>
            ";
        }
        return "
        <form class=\"form\">
            <div class=\"form-card has-depth\">
                $studentFormFields
            </div>
        </form>
        ";
    },

    'evaluate' => function () {
        return '';
    }
];


function renderPhase1Style()
{
}

function renderPhase2Style()
{

}

function renderSummaryStyle()
{

}
?>
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>
        <?php
        $subtitles = [
            'get-records' => 'Enter All your records.',
            'evaluate' => 'Data Summary',
            'get-number-of-students' => 'Enter the number of students.'
        ];

        echo "Student Quiz Evaluator | {$subtitles[$mode]}";
        ?>
    </title>
    <style>
        :root {
            --bg: #fff;
            --fg: #000;
            --surface: #aaa;
            --shadow: #ccc;
        }

        *,
        *::before,
        *::after {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-size: 1rem;
        }

        @property --depth {
            syntax: "<length>";
            inherits: false;
            initial-value: 0px;
        }

        /* components */
        .has-depth {
            box-shadow: var(--depth) var(--depth) 1rem var(--shadow);
            transform: translateX(calc(-1 * var(--depth))) translateY(calc(-1 * var(--depth)));
            transition: all 0.4s ease;
        }

        button.has-depth:active {
            box-shadow: none;
            transform: translateX(0) translateY(0);
            transform: 0.4s ease;
        }

        html,
        body,
        form {
            height: 100vh;
            width: 100vw;
            display: flex;
            flex-direction: column;
            justify-content: center;
            place-items: center;
        }

        .form-card {
            position: relative;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            align-items: center;

            background-color: var(--surface);

            /** card */
            height: 60%;
            width: 50%;
            border-radius: 1.25rem;

            /**
            do not cram everything.
             */
            padding-left: 0.75rem;
            padding-right: 0.75rem;
            padding-top: 0.5rem;
            padding-bottom: 0.5rem;

            /**
            3d effect. the margin moves the card
            a little bit so the shadow looks like at z=0
            */
            --depth: 0.5rem;
            --horizon-scale: 40%;
            --horizon-depth: 400%;
            overflow-y: scroll;
        }

        .form-field {
            position: relative;
            width: 100%;
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
        }

        .form-field input {
            padding: 0.25rem;
            font-size: 1rem;
            border-radius: 0.75rem;
        }

        .form-field input:focus-visible {
            box-shadow: 0 0 0.5rem var(--shadow);
        }

        .form-field input:not(:placeholder-shown)~label {
            position: absolute;
            top: -2px;
            left: 2px;
        }

        .form-card .form-action {
            border: none;
            align-self: flex-end;
            border-radius: 0.5rem;
            padding-top: 0.5rem;
            padding-bottom: 0.5rem;
            margin-bottom: 1rem;
            width: 100%;

            /* depth */
            --depth: 2px;
        }


        .form-card .form-action:active {
            transform: translateX(0) translateY(0);
            transition: all 0.2s ease;
            box-shadow: none;
        }
    </style>
    <style>
        <?php
        switch ($mode) {
            case 'get-number-of-students':
                renderPhase1Style();
                break;

            case 'get-records':
                renderPhase2Style();
                break;

            case 'evaluate':
                renderSummaryStyle();
                break;
        }
        ?>
    </style>
</head>

<body>
    <?php
    // this block of php code determines what to render in the site.
    echo $bodyContentRenderers[$mode]();
    ?>

    <script>
        window.addEventListener('DOMContentLoaded', function () {
            <?php
            // this php code determines what javascript to use.
            ?>
        });
    </script>
    <script>
        // basic react-like utility because integrating
        // php with react is hard.
        // this script block contains web components.
        // this web components will basically just be shorthands.

        class ExtendedHTMLElement extends HTMLElement {
            constructor() {
                super();
                this.state = null;
                this.attributes = null;
            }

            connectedCallback() {
                this.state = this.initState();
                this.innerHTML = this.render();
            }

            forceRerender() {
                this.innerHTML = this.render();
            }

            setState(value) {
                this.state = Object.assign({}, this.state, value);
                this.forceRerender();
            }

            initState() {
                return {};
            }

            render() {
                return '';
            }
        };

        class Card extends ExtendedHTMLElement {
            render() {
                return `<div class="card"><slot></slot></div>`;
            }
        };

        class CardAction extends ExtendedHTMLElement {
            render() {
                return `<button class="card-action-button"><slot></slot></button>";
            }
        };

        class FormField extend ExtendedHTMLElement {
            render() {
                return `< div class="form-field" > <slot></slot></div >`;
            }
        };

        const components = {
            'x-card': Card,

        };

        for (const component in components) {
            customElements.define(component, components[component]);
        };
    </script>
</body>

</html>