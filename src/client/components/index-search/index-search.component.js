angular.module('indexSearch').component('indexSearch', {

    templateUrl: 'components/index-search/index-search.template.html',

    controller: ['$rootScope', '$http', function IndexSearchController($rootScope, $http) {

        var self = this;
        this.index = null;
        this.error = null;

        this.search = function () {
            if (this.index) {
                $http({
                    method: 'GET',
                    url: 'http://localhost:8080/index/' + this.index
                }).then(function successCallback(response) {
                    if (response.data.valid) { 
                        $rootScope.$broadcast('index', self.index);
                        self.error = null;
                        self.index = null;
                    } else self.error = 'Index doesn\'t exists';
                });
            }
        };

    }]

});