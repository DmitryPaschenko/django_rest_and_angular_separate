app.controller('AppCtrl',
['$scope', '$mdBottomSheet','$mdSidenav', '$mdDialog', 'djangoAuth', '$state',
function($scope, $mdBottomSheet, $mdSidenav, $mdDialog, djangoAuth, $state) {
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
      sref: 'admin.main.home',
      srefOpts: {},
      title: 'Dashboard',
      icon: 'dashboard'
    },
    {
      sref: 'admin.main.profile',
      srefOpts: {},
      title: 'Profile',
      icon: 'profile'
    }
  ];
  $scope.admin = [
    {
      sref: 'admin.users.list',
      srefOpts: {},
      title: 'Users',
      icon: 'groups'
    },
    {
      sref: 'admin.permissions.list',
      srefOpts: {},
      title: 'User Permissions',
      icon: 'groups'
    }
//    {
//      link : '',
//      title: 'Logout',
//      icon: 'logout'
//    }
  ];

  $scope.alerts = [];

  $scope.addSuccessAlert = function(message) {
      $scope.alerts.push({ type: 'success', msg: message });
  };
  $scope.addDangerAlert = function(message) {
      $scope.alerts.push({ type: 'danger', msg: message });
  };

  $scope.addAlert = function(type, message) {
      // success, danger
      $scope.alerts.push({ type: type, msg: message });
  };

  $scope.clearAlerts = function() {
      // success, danger
      $scope.alerts = [];
  };

  $scope.closeAlert = function(index) {
      $scope.alerts.splice(index, 1);
  };

  $scope.preController = function() {
      $scope.clearAlerts();
  };

//    $state.transitionTo('admin.home');
}]);