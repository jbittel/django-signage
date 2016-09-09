'use strict';

angular.module('signage', [
  'ngAnimate',
  'signage.slide',
])

.config(['$httpProvider', function($httpProvider) {
  $httpProvider.defaults.headers.common["X-Requested-With"] = 'XMLHttpRequest';
}]);
