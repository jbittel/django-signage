angular.module('signage', ['ngAnimate'])

.config(['$httpProvider', function($httpProvider) {
  $httpProvider.defaults.headers.common["X-Requested-With"] = 'XMLHttpRequest';
}])

.controller('SignageController', ['$http', '$scope', '$timeout', function($http, $scope, $timeout) {
  $scope.isCurrentSlide = function(index) {
    return $scope.currentIndex === index;
  };

  function getSlideDuration() {
    if ($scope.slides.length) {
      return $scope.slides[$scope.currentIndex].duration * 1000;
    } else {
      return 0;
    }
  };

  $scope.nextSlide = function() {
    if ($scope.slides) {
      $scope.currentIndex = ($scope.currentIndex < $scope.slides.length - 1) ? ++$scope.currentIndex : 0;
    }
    $timeout($scope.nextSlide, getSlideDuration());
  };

  function updateSlides() {
    $http.get('/display/1/slides/').then(function(response) {
      if (!angular.equals($scope.slides, response.data)) {
        $scope.slides = response.data;
      }
    });

    $timeout(updateSlides, 10000);
  };

  $scope.currentIndex = 0;
  $scope.slides = [];

  updateSlides();
  $scope.nextSlide();
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
  }
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
