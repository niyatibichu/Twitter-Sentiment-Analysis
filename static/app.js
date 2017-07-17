var app = angular.module("myapp", []);

app.controller("MainController", ['$scope', '$http', function ($scope, $http) {
   // $scope.tweets=[];
    $scope.submitData = function () {

        console.log($scope.latitude);
        console.log($scope.longitude);
        console.log($scope.radius);
        console.log($scope.keyword);

        $http({
            url: '/getdata',
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            },
            params: {
                lat: $scope.latitude,
                lon: $scope.longitude,
                rad: $scope.radius,
                key:$scope.keyword
            }
        }).then(function success(response) {
            $scope.tweets=response.data;
            console.log($scope.tweets);

            
            // angular.forEach($scope.tweets, function (tweet) {
            //     //$scope.text=tweet._source.text                
            //     console.log("Tweet: ",tweet);
            // });
           // console.log($scope.tweets)

        }, function error(error) {
            console.log(error);
        });


    }
}]);