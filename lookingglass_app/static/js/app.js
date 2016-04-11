// create the module and name it phpro
// also include ngRoute for all our routing needs
var phpro = angular.module('phpro', ['ngRoute']);

// configure our routes
phpro.config(function($routeProvider) {

$routeProvider
        // route for the index page
        .when('/', {
                templateUrl : 'templates/index.html',
                controller  : 'mainCtrl'
        })

        // route for the FAQ page
        .when('/faq', {
        templateUrl : 'templates/faq.html',
        controller  : 'faqCtrl'
        })

        // route for the contact page
        .when('/contact', {
                templateUrl : 'templates/contact.html',
                controller  : 'contactCtrl'
        });
});

// create the controller and inject Angular's $scope
phpro.controller('mainCtrl', function($scope) {
        // create a message to display in our view
        $scope.heading = 'Welcome to The Looking Glass!';
        $scope.message = 'We bring pictures into your life!';
});

phpro.controller('faqCtrl', function($scope) {
        $scope.heading = 'The Looking Mirror FAQ';
        $scope.message = 'Here are answers to some of the most frequently asked questions!';
});

phpro.controller('contactCtrl', function($scope) {
        $scope.heading = 'The Looking Glass Team';
        $scope.message = 'Contact "the.looking.glass@gmail.com"';
});