var app = angular.module('AdminApp', [
    'ngMaterial',
    'ngMdIcons',
    'ui.router',
    'ngCookies',
    'ngResource',
    'ngSanitize']);

var API_URL = '/api/v1/';

app.run(['$rootScope', '$state', '$stateParams', 'djangoAuth', function ($rootScope,   $state,   $stateParams, djangoAuth) {
        $rootScope.$state = $state;
        $rootScope.$stateParams = $stateParams;
        djangoAuth.initialize('//127.0.0.1:8000/api/v1/rest-auth', false);
    }
  ]
)
.config(['$stateProvider', '$urlRouterProvider', function ($stateProvider,   $urlRouterProvider) {
      $stateProvider
        .state('admin', {
            abstract: true,
            views: {
                'layout': {
                    templateUrl: '/app/modules/base/admin_view.html'
                }
            },
            resolve: {
              authenticated: ['djangoAuth', function(djangoAuth) {
                return djangoAuth.authenticationStatus(true);
              }]
            }
        })
        .state('pages', {
            abstract: true,
            views: {
                'layout': {
                    templateUrl: '/app/modules/base/blank_view.html'
                }
            }
        })
        .state("admin.home", {
            url: "/",
            views: {
                'content': {
                    templateUrl: '/app/modules/dashboard/dashboard.html'
                }
            },
            data: { pageTitle: 'Dashboard' }
        })
        .state("admin.profile", {
            url: "/profile",
            views: {
                'content': {
                    templateUrl: '/app/modules/user/profile.html',
                }
            },
            data: { pageTitle: 'Profile' }
        })
        .state("pages.login", {
            url: "/login",
            views: {
                'content': {
                    templateUrl: '/app/modules/user/login.html'
                }
            },
            controller: function($scope, $mdDialog){
                $scope.showLogin(undefined, $mdDialog);
            }
        });
    }
  ]
);
