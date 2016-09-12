angular.module('signage.video', ['djng.urls'])

.factory('videoService', ['$http', '$timeout', 'displayContext', 'djangoUrl', function($http, $timeout, displayContext, djangoUrl) {
  var service = {
    video: undefined,
  };

  var updateVideo = function() {
    $http.get(djangoUrl.reverse('signage:display_video', {'pk': displayContext.pk}))
      .then(function(response) {
        service.video = response.data;
      }, function(response) {
        service.video = undefined;
      });
    $timeout(updateVideo, displayContext.interval * 1000);
  };

  updateVideo();

  return service;
}]);
