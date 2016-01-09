var signage = angular.module('signage', ['ngAnimate']);

signage.config(['$httpProvider', function($httpProvider) {
  $httpProvider.defaults.headers.common["X-Requested-With"] = 'XMLHttpRequest';
}]);

signage.controller('SignageController', ['$http', '$scope', '$timeout', function($http, $scope, $timeout) {
  function isCurrentSlide(index) {
    return $scope.currentIndex === index;
  }

  function getSlideDuration() {
    return $scope.slides[$scope.currentIndex].duration * 1000;
  }

  function nextSlide() {
    if ($scope.slides) {
      $scope.currentIndex = ($scope.currentIndex < $scope.slides.length - 1) ? ++$scope.currentIndex : 0;
    }
    $timeout(nextSlide, getSlideDuration());
  }

  function updateSlides() {
    $http.get('/display/1/slides/').then(function(response) {
      if (!angular.equals($scope.slides, response.data)) {
        $scope.slides = response.data;
      }
    });

    $timeout(updateSlides, 10000);
  }

  $scope.currentIndex = 0;
  $scope.slides = [];

  $scope.isCurrentSlide = isCurrentSlide;
  $scope.nextSlide = nextSlide;

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

signage.animation('.animate', function() {
  return {
    enter: function(element, done) {
      TweenMax.fromTo(element, 1, {opacity: 0}, {opacity: 1, onComplete: done});
    },
    leave: function(element, done) {
      TweenMax.to(element, 1, {opacity: 0, onComplete: done});
    }
  };
});
