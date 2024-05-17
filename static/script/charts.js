// Your chart.js file with jQuery
$(document).ready(function() {
    google.charts.load('current', {'packages':['bar']});
    google.charts.setOnLoadCallback(drawChart);

    function drawChart() {
        var data = google.visualization.arrayToDataTable([
            ['Month', 'TOTAL', 'Top Contributors', 'Contribution Goals'],
            ['JAN', 100000, 20000, 150000],
            ['FEB', 150000, 70000, 150000],
            ['MARCH', 130000, 35000, 150000],
            ['APRIL', 90000, 15000, 150000],
            ['MAY', 97000, 11000, 150000],
            ['JUNE', 170000, 11020, 100000],
            ['JULY', 65000, 7000, 150000],
            ['AUG', 50000, 8000, 150000],
            ['SEPT', 89000, 10000, 10000],
            ['OCT', 165000, 16000, 15000],
            ['NOV', 170000, 2500, 200000],
            ['DEC', 185000, 80000, 200000],
        ]);

        var options = {
            chart: {
                title: 'Contributions Performance YEAR 2024',
                subtitle: 'TOTAL, Top Contributors, and Contribution Goals',
            }
        };

        var chart = new google.charts.Bar($('#columnchart_material')[0]);
        chart.draw(data, google.charts.Bar.convertOptions(options));
    }
});
