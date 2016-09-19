angular.module('signage.slide', ['djng.urls', 'ngAnimate'])

.factory('slideService', ['$http', '$timeout', 'displayContext', 'djangoUrl', function($http, $timeout, displayContext, djangoUrl) {
  var currentIndex = 0;
  var service = {
    slides: [],
  };

  service.isCurrentSlide = function(index) {
    return currentIndex === index;
  };

  var nextSlide = function() {
    var duration = 0;

    if (service.slides.length) {
      currentIndex = (currentIndex < service.slides.length - 1) ? ++currentIndex : 0;
      duration = service.slides[currentIndex].duration * 1000;
    }
    $timeout(nextSlide, duration);
  };

  var updateSlides = function() {
    $http.get(djangoUrl.reverse('signage:display_slides', {'pk': displayContext.pk}))
      .then(function(response) {
        if (!angular.equals(service.slides, response.data)) {
          service.slides = response.data;
        }
      });
    $timeout(updateSlides, displayContext.interval * 1000);
  };

  updateSlides();
  nextSlide();

  return service;
}])

.directive('backgroundColor', [function() {
  return function(scope, element, attrs) {
    element.on('load', function() {
      var vibrant = new Vibrant(element[0]);
      var swatches = vibrant.swatches();
      var color = '#000';

      if (swatches.hasOwnProperty('DarkMuted') && swatches['DarkMuted']) {
        color = swatches['DarkMuted'].getHex();
      }
      angular.element(document.body).css('background-color', color);
    });
  };
}]);
