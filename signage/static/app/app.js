'use strict';

angular.module('signage', [
  'ngAnimate',
  'signage.context',
  'signage.slide',
  'signage.video',
])

.config(['$httpProvider', function($httpProvider) {
  $httpProvider.defaults.headers.common["X-Requested-With"] = 'XMLHttpRequest';
}])

.controller('ContentController', ['$scope', 'slideService', 'videoService', function($scope, slideService, videoService) {
  $scope.slideService = slideService;
  $scope.videoService = videoService;
}]);
