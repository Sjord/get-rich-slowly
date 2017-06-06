<?php
    function serve_history_file($filename) {
        $data = json_decode(file_get_contents($filename), true);
        ksort($data);
        $result = [];
        $filter_value = date('Y-m-d', strtotime("-1 year"));
        foreach ($data as $k => $v) {
            if ($k >= $filter_value) {
                $result[$k] = $v;
            }
        }
        die(json_encode($result));
    }

    if ($_GET['d']) {
        header('Content-Type: application/json');
        serve_history_file('../data/portfolio_history.json');
    }
    if ($_GET['m']) {
        header('Content-Type: application/json');
        serve_history_file('../data/money_history.json');
    }
?>

<script src="js/jquery-2.1.3.min.js" charset="utf-8"></script>
<script src="js/d3.v3.min.js" charset="utf-8"></script>
<script src="js/nv.d3.min.js" charset="utf-8"></script>
<link rel="stylesheet" href="css/nv.d3.css" type="text/css" />

<div id="chart">
  <svg></svg>
</div>

<script src="js/graph.js" charset="utf-8"></script>