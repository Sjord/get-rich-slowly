<?php
    if ($_GET['d']) {
        header('Content-Type: application/json');
        readfile('../data/portfolio_history.json');
        exit();
    }
    if ($_GET['m']) {
        header('Content-Type: application/json');
        readfile('../data/money_history.json');
        exit();
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