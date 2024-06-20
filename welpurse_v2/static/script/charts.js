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
            width: '100%',
            height: '100%',
            chart: {
                title: 'Contributions Performance YEAR 2024',
                subtitle: 'TOTAL, Top Contributors, and Contribution Goals',
            },
            backgroundColor: '#E4E4E4', // Sets the background color for the entire chart
            chartArea: {
                backgroundColor: {
                    fill: '#F4F4F4', // The fill color for the chart area
                    fillOpacity: 0.8, // Optional: The fill opacity for the chart area
                },
                left: "50%", // Adjust as needed
                top: "50%", // Adjust as needed
                width: '80%', // Adjust as needed
                height: '80%' // Adjust as needed
            }
        };

        var chart = new google.charts.Bar(document.getElementById('columnchart_material'));
        chart.draw(data, google.charts.Bar.convertOptions(options));
    }
});
