angular.module('lineChart').component('lineChart', {

    templateUrl: 'components/line-chart/line-chart.template.html',

    controller: ['moment', '$http', function LineChartController(moment, $http) {

        var self = this;

        this.getLabels = function () {
            var labels = [];
            // get last 7 working days
            for (i = 1; labels.length < 7; i++) {
                var date = moment().startOf('day').add(-i, 'day');
                // ignore weekend
                if (date.isoWeekday() == 6 || date.isoWeekday() == 7) {
                    continue;
                } else {
                    labels.push(date);
                }
            }
            return labels;
        };

        this.getStockValues = function (index, callback) {
            // need at least 1 day
            if (this.labels.length == 0) return;

            // construct url
            var start = this.labels[this.labels.length - 1].format('YYYYMMDD');
            var end = this.labels[0].format('YYYYMMDD');
            var url = 'http://localhost:8080/stocks/' + index + '/' + start + '/' + end;

            $http({
                method: 'GET',
                url: url
            }).then(function successCallback(response) {
                var values = [];
                response.data.forEach(function (value) {
                    values.push(value[1]);
                });
                callback(values);
            });
        };

        this.labels = this.getLabels();
        this.data = [[], []];
        this.getStockValues('aapl', function (data) {
            self.data[0] = data;
        });

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

    }]

});