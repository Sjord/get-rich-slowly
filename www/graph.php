<?php
    if ($_GET['d']) {
        header('Content-Type: application/json');
        readfile('../data/portfolio_history.json');
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


<script>
$.getJSON('graph.php?d=1', function (data) {
    funds = {};
    total = {};
    for (var datum in data) {
        for (var i = 0; i < data[datum].length; i++) {
            var fund_data = data[datum][i];
            var fund_name = fund_data['fund']['name'];
            var value = fund_data['totVal'];
            var timestamp = Date.parse(datum);
            funds[fund_name] = funds[fund_name] || [];
            funds[fund_name].push([timestamp, value]);

            total[timestamp] = total[timestamp] || 0;
            total[timestamp] += value;
        }
    }

    data = [];
    for (var fund in funds) {
        data.push({
            'key': fund,
            'values': funds[fund].sort()
        });
    }

    totals = []
    for (var timestamp in total) {
        totals.push([+timestamp, total[timestamp]]);
    }

    data.push({
        'key': 'total',
        'values': totals.sort()
    });

    nv.addGraph(function() {
        var chart = nv.models.lineChart()
            .x(function (d, i) { return d[0]; })
            .y(function (d, i) { return d[1]; })
            ;

        chart.xAxis
            .tickFormat(function(d) { return d3.time.format('%Y-%m-%d')(new Date(d)) });

        chart.yAxis
            .tickFormat(d3.format(',.2f'));

        chart.forceY([0]);

        d3.select('#chart svg')
            .datum(data)
            .call(chart);

        nv.utils.windowResize(chart.update);

        return chart;
    });


    //Generate some nice data.
    function exampleData() {
        data = []
        for (var i = 0; i < 100; i++) {
            data.push({
                key: 'Stream #' + i % 3,
                values: [i]
            });
        };
        return data;
    }
});
</script>
