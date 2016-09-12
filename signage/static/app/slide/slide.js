angular.module('signage.slide', ['djng.urls'])

.controller('SignageController', ['$scope', 'slideService', function($scope, slideService) {
  $scope.slideService = slideService;
}])

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
    // TODO don't hardcode update interval
    $timeout(updateSlides, 10000);
  };

  updateSlides();
  nextSlide();

  return service;
}])

.directive('bgImage', ['$window', function($window) {
  return function(scope, element, attrs) {
    var resizeBG = function() {
      var bgwidth = element.width();
      var bgheight = element.height();

      var winwidth = $window.innerWidth;
      var winheight = $window.innerHeight;

      var widthratio = winwidth / bgwidth;
      var heightratio = winheight / bgheight;

      var widthdiff = heightratio * bgwidth;
      var heightdiff = widthratio * bgheight;

      if (heightdiff > winheight) {
        element.css({
          width: winwidth + 'px',
          height: winheight + 'px'
        });
      } else {
        element.css({
          width: widthdiff + 'px',
          height: heightdiff + 'px'
        });
      }
    };

    var windowElement = angular.element($window);
    windowElement.resize(resizeBG);

    element.bind('load', function() {
      resizeBG();
    });
  };
}])

.animation('.animate', function() {
  return {
    enter: function(element, done) {
      TweenMax.fromTo(element, 1, {opacity: 0}, {opacity: 1, onComplete: done});
    },
    leave: function(element, done) {
      TweenMax.to(element, 1, {opacity: 0, onComplete: done});
    }
  };
});
