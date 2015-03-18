var signage = angular.module('signage', ['ngAnimate', 'ngResource']);

signage.config(['$resourceProvider', '$httpProvider', function($resourceProvider, $httpProvider) {
  $resourceProvider.defaults.stripTrailingSlashes = false;
  $httpProvider.defaults.headers.common["X-Requested-With"] = 'XMLHttpRequest';
}]);

signage.controller('SignageController', ['$scope', '$timeout', '$resource', function($scope, $timeout, $resource) {
  $scope.slides = [];

  function isCurrentSlideIndex(index) {
    return $scope.currentIndex === index;
  }

  function getSlideDuration() {
    try {
      return $scope.slides[$scope.currentIndex].duration * 1000;
    } catch (err) {
      return 3000;
    }
  }

  function nextSlide() {
    $scope.currentIndex = ($scope.currentIndex < $scope.slides.length - 1) ? ++$scope.currentIndex : 0;
    $timeout(nextSlide, getSlideDuration());
  }

  function updateSlides() {
    var Update = $resource('json/');

    Update.get(function(data) {
      $scope.slides = data.slides;
    });

    $timeout(updateSlides, 3000);
  }

  $scope.nextSlide = nextSlide;
  $scope.isCurrentSlideIndex = isCurrentSlideIndex;
  $scope.currentIndex = -1;

  updateSlides();
  nextSlide();
}]);

signage.directive('bgImage', ['$window', function($window) {
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
  }
}]);

signage.animation('.animate', function($window) {
  return {
    enter: function(element, done) {
      TweenMax.fromTo(element, 1, {opacity: 0}, {opacity: 1, onComplete: done});
    },
    leave: function(element, done) {
      TweenMax.to(element, 1, {opacity: 0, onComplete: done});
    }
  };
});
