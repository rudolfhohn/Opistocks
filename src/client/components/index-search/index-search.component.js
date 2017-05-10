angular.module('indexSearch').component('indexSearch', {

    templateUrl: 'components/index-search/index-search.template.html',

    controller: ['$rootScope', function IndexSearchController($rootScope) {

        var self = this;
        this.index = null;

        this.search = function () {
            if (this.index) {
                $rootScope.$broadcast('index', this.index);
                this.index = null;
            }
        };

    }]

});