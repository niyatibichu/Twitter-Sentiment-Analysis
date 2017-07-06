var app = angular.module("myapp", []);

app.controller("MainController", ['$scope', '$http', function ($scope, $http) {

    $scope.submitData = function () {

        console.log($scope.latitude);
        console.log($scope.longitude);
        console.log($scope.radius);

        $http({
            url: '/getdata',
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            },
            params: {
                lat: $scope.latitude,
                lon: $scope.longitude,
                rad: $scope.radius
            }
        }).then(function success(response) {
            $scope.tweets = response;
            console.log(response)

        }, function error(error) {
            console.log(error);
        });


    }
}]);