angular.module('signage.slide', ['djng.urls'])

.controller('SignageController', ['$scope', '$timeout', 'slideService', function($scope, $timeout, slideService) {
  $scope.isCurrentSlide = function(index) {
    return $scope.currentIndex === index;
  };

  function getSlideDuration() {
    if ($scope.slides.length) {
      return $scope.slides[$scope.currentIndex].duration * 1000;
    } else {
      return 0;
    }
  }

  $scope.nextSlide = function() {
    if ($scope.slides) {
      $scope.currentIndex = ($scope.currentIndex < $scope.slides.length - 1) ? ++$scope.currentIndex : 0;
    }
    $timeout($scope.nextSlide, getSlideDuration());
  };

  function updateSlides() {
    slideService.getSlides()
      .then(function(slides) {
        if (!angular.equals($scope.slides, slides)) {
          $scope.slides = slides;
        }
      });
    $timeout(updateSlides, 10000);
  }

  $scope.currentIndex = 0;
  $scope.slides = [];

  updateSlides();
  $scope.nextSlide();
}])

.service('slideService', ['$http', 'djangoUrl', 'displayContext', function($http, djangoUrl, displayContext) {
  this.getSlides = function() {
    return $http.get(djangoUrl.reverse('signage:display_slides', {'pk': displayContext.pk}))
      .then(function(response) {
        return response.data;
      });
  };
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
