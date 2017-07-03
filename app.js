var app = angular.module("myapp", []);

app.controller("MainController", ['$scope', '$http', function ($scope, $http) {

    $scope.submitData = function () {

        console.log($scope.latitude);

        $http({
            method: 'GET',
            url: '/getTweets',
            params:{
                lon:$scope.longitude,
                lat:$scope.latitude,
                rad:$scope.radius
            }
        }).then(function success(response) {
            $scope.tweets=response;

        }, function error(error) {
            console.log(error);            
        });


    }
}]);