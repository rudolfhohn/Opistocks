angular.module('lineChart').component('lineChart', {

    templateUrl: 'components/line-chart/line-chart.template.html',

    controller: ['moment', function LineChartController(moment) {

        this.labels = [];

        // get last 7 working days
        for (i = 1; this.labels.length < 7; i++) {
            var date = moment().startOf('day').add(-i, 'day');

            // ignore weekend
            if (date.isoWeekday() == 6 || date.isoWeekday() == 7) {
                continue;
            } else { 
                this.labels.push(date);
            }
        }

        this.series = ['Stock', 'Sentiment'];

        this.datasets = [{
            yAxisID: 'stock',
            fill: false,
            borderColor: 'lightblue'
        }, {
            yAxisID: 'sentiment',
            fill: false,
            borderColor: 'lightgreen'
        }];

        this.options = {
            scales: {
                xAxes: [{
                    type: 'time',
                    time: { unit: 'day' }
                }],
                yAxes: [{
                    position: 'left',
                    id: 'stock',
                    gridLines: { display: false },
                    scaleLabel: {
                        display: true,
                        labelString: 'Stock'
                    }
                }, {
                    position: 'right',
                    id: 'sentiment',
                    gridLines: { display: false },
                    scaleLabel: {
                        display: true,
                        labelString: 'Sentiment'
                    }
                }]
            }
        };

        this.data = [
            [65, 59, 80, 81, 56, 55, 40],
            [28, 48, 40, 19, 86, 27, 90]
        ];

    }]

});