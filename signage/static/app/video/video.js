angular.module('signage.video', ['djng.urls'])

.factory('videoService', ['$http', '$timeout', 'displayContext', 'djangoUrl', function($http, $timeout, displayContext, djangoUrl) {
  var service = {
    url: undefined,
  };

  var updateVideo = function() {
    $http.get(djangoUrl.reverse('signage:display_video', {'pk': displayContext.pk}))
      .then(function(response) {
        service.url = response.data.url;
      }, function(response) {
        service.url = undefined;
      });
    $timeout(updateVideo, displayContext.interval * 1000);
  };

  updateVideo();

  return service;
}])

.directive('playVideo', ['videoService', function(videoService) {
  return function(scope, element, attrs) {
    if (Hls.isSupported()) {
      var hls = new Hls();
      hls.attachMedia(element[0]);
      hls.on(Hls.Events.MEDIA_ATTACHED, function() {
        hls.loadSource(videoService.url);
        hls.on(Hls.Events.MANIFEST_PARSED, function() {
          element[0].play();
        });
      });

      element.on('$destroy', function() {
        hls.destroy();
      });
    }
  };
}]);
