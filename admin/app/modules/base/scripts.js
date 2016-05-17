app.controller('AppCtrl', ['$scope', '$mdBottomSheet','$mdSidenav', '$mdDialog', 'djangoAuth', '$state', function($scope, $mdBottomSheet, $mdSidenav, $mdDialog, djangoAuth, $state){
    // Assume user is not logged in until we hear otherwise
    $scope.authenticated = false;
    // Wait for the status of authentication, set scope var to true if it resolves
    djangoAuth.authenticationStatus(true).then(function(){
        $scope.authenticated = true;
    });
    // Wait and respond to the logout event.
    $scope.$on('djangoAuth.logged_out', function() {
      $scope.authenticated = false;
    });
    // Wait and respond to the log in event.
    $scope.$on('djangoAuth.logged_in', function() {
      $scope.authenticated = true;
    });
    $scope.$on('$stateChangeError', function (event, toState, toParams, fromState, fromParams, error) {
        $state.go('pages.login');
    });




    $scope.toggleSidenav = function(menuId) {
        $mdSidenav(menuId).toggle();
    };
    $scope.menu = [
    {
      sref: 'admin.home',
      srefOpts: {},
      title: 'Dashboard',
      icon: 'dashboard'
    },
    {
      sref: 'admin.profile',
      srefOpts: {},
      title: 'Profile',
      icon: 'profile'
    }
  ];
  $scope.admin = [
    {
      link : '',
      title: 'Settings',
      icon: 'settings'
    },
    {
      link : '',
      title: 'Logout',
      icon: 'logout'
    }
  ];
}]);

app.config(function($mdThemingProvider) {
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
});

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