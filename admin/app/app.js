var app = angular.module('AdminApp', [
    'ngMaterial',
    'ngMdIcons',
    'ui.router',
    'ngCookies',
    'ngResource',
    'ngSanitize',
    'ui.bootstrap',
    'md.data.table',
    'angularUtils.directives.uiBreadcrumbs']);

var API_URL = '//127.0.0.1:8000/api/v1';

app.run(['$rootScope', '$state', '$stateParams', 'djangoAuth', function ($rootScope, $state, $stateParams, djangoAuth) {
        $rootScope.$state = $state;
        $rootScope.$stateParams = $stateParams;
        djangoAuth.initialize('//127.0.0.1:8000/api/v1/rest-auth', false);
    }
  ]
)
.config(['$httpProvider', '$resourceProvider', '$mdThemingProvider',
function($httpProvider, $resourceProvider, $mdThemingProvider) {
    var customBlueMap = 		$mdThemingProvider.extendPalette('light-blue', {
        'contrastDefaultColor': 'light',
        'contrastDarkColors': ['50'],
        '50': 'ffffff'
    });
    $mdThemingProvider.definePalette('customBlue', customBlueMap);
    $mdThemingProvider.theme('default')
        .primaryPalette('customBlue', {
            'default': '500',
            'hue-1': '50'
        })
        .accentPalette('pink');
    $mdThemingProvider.theme('input', 'default')
        .primaryPalette('grey')

    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';

    $resourceProvider.defaults.stripTrailingSlashes = false;
}])
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

        .state("admin.main", {
            abstract: true,
            data: {
                proxy: 'admin.main.home'
            }
        })
        .state("admin.main.home", {
            url: "/",
            views: {
                'content': {
                    templateUrl: '/app/modules/dashboard/dashboard.html'
                },
            },
            data: {
                displayName: 'Dashboard'
            }
        })
        .state("admin.main.profile", {
            url: "/profile",
            views: {
                'content': {
                    templateUrl: '/app/modules/user/profile.html',
                }
            },
            data: { displayName: 'Profile' }
        })


        .state('admin.users', {
            abstract: true,
            data: {
                proxy: 'admin.users.list'
            },
        })
        .state("admin.users.edit", {
            url: "/users/{userId:[0-9]+}",
            views: {
                'content': {
                    templateUrl: '/app/modules/user/edit.html',
                }
            },
            data: { displayName: 'Edit user' }
        })
        .state("admin.users.create", {
            url: "/users/create",
            views: {
                'content': {
                    templateUrl: '/app/modules/user/create.html',
                }
            },
            data: { displayName: 'Create user' }
        })
        .state("admin.users.list", {
            url: "/users",
            views: {
                'content': {
                    templateUrl: '/app/modules/user/list.html',
                }
            },
            data: {
                displayName: 'Users list'
            }
        })

        .state('admin.permissions', {
            abstract: true,
            data: {
                proxy: 'admin.permissions.list'
            },
        })
        .state("admin.permissions.edit", {
            url: "/permissions/{id:[0-9]+}",
            views: {
                'content': {
                    templateUrl: '/app/modules/permission/edit.html',
                }
            },
            data: { displayName: 'Edit permission' }
        })
        .state("admin.permissions.create", {
            url: "/permissions/create",
            views: {
                'content': {
                    templateUrl: '/app/modules/permission/create.html',
                }
            },
            data: { displayName: 'Create permission' }
        })
        .state("admin.permissions.list", {
            url: "/permissions",
            views: {
                'content': {
                    templateUrl: '/app/modules/permission/list.html',
                }
            },
            data: { displayName: 'Permission list' }
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

function DialogController($scope, $mdDialog) {
  $scope.hide = function() {
    $mdDialog.hide();
  };
  $scope.cancel = function() {
    $mdDialog.cancel();
  };
  $scope.answer = function(answer) {
    $mdDialog.hide(answer);
  };
};
