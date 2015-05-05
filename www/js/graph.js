
function get_all_fund_names(data, dates) {
    var fundNames = new Set();
    dates.forEach(function (date) {
        data[date].forEach(function (fundPrice) {
            var fundName = fundPrice.fund.name;
            fundNames.add(fundName);
        });
    });
    return fundNames;
}

function get_all_dates(data) {
    return Object.getOwnPropertyNames(data).sort();    
}

function get_fund_names(fundPrices) {
    return fundPrices.map(function (fundPrice) {
        return fundPrice['fund']['name'];
    });
}

$.getJSON('graph.php?d=1', function (data) {
    var allDates = get_all_dates(data);
    var allFunds = get_all_fund_names(data, allDates);
    
    var fundNameCounters = {};
    allFunds.forEach(function (fundName) {
        fundNameCounters[fundName] = 0;
    });
    
    var dataPointsPerFund = {};
    
    var previousFundNames = [];
    allDates.forEach(function (date) {
        data[date].forEach(function (fundPrice) {
            var fund_name = fundPrice['fund']['name'];
            if (previousFundNames.indexOf(fund_name) === -1) {
                fundNameCounters[fund_name] += 1;
            }
            var key = fund_name + "_" + fundNameCounters[fund_name];
            var value = fundPrice['totVal'];
            var timestamp = Date.parse(date);
            
            dataPointsPerFund[key] = dataPointsPerFund[key] || [];
            dataPointsPerFund[key].push([timestamp, value]);
        });
        
        previousFundNames = get_fund_names(data[date]);
    });
    
    var totalPerDate = {};
    allDates.forEach(function (date) {
        data[date].forEach(function (fundPrice) {
            totalPerDate[date] = totalPerDate[date] || 0;
            totalPerDate[date] += fundPrice['totVal']
        });
    }); 
    
    data = [];
    for (var fund in dataPointsPerFund) {
        data.push({
            'key': fund,
            'values': dataPointsPerFund[fund].sort()
        });
    }

    var totalDataPoints = [];
    for (var date in totalPerDate) {
        var timestamp = Date.parse(date);
        totalDataPoints.push([timestamp, totalPerDate[date]]);
    }
    
    data.push({
        'key': 'total',
        'values': totalDataPoints.sort()
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