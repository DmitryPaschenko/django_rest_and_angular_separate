app.controller('AppCtrl',
['$scope', '$mdBottomSheet','$mdSidenav', '$mdDialog', 'djangoAuth', '$state', '$mdMedia',
function($scope, $mdBottomSheet, $mdSidenav, $mdDialog, djangoAuth, $state, $mdMedia) {
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
    },
    {
      sref: 'admin.groups.list',
      srefOpts: {},
      title: 'User Groups',
      icon: 'groups'
    },
    {
      sref: 'admin.templates.list',
      srefOpts: {},
      title: 'Document Templates',
      icon: 'templates'
    },
    {
      sref: 'admin.documents.list',
      srefOpts: {},
      title: 'Documents',
      icon: 'documents'
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

    $scope.showFilterPopup = function(ev, templateUrl, ctrl) {
        var customFullscreen = $mdMedia('xs') || $mdMedia('sm');
        var useFullScreen = ($mdMedia('sm') || $mdMedia('xs'))  && customFullscreen;
        $mdDialog.show({
          controller: FilterDialogController,
          templateUrl: templateUrl,
          parent: angular.element(document.body),
          targetEvent: ev,
          clickOutsideToClose: true,
          fullscreen: useFullScreen,
          locals: {
            ctrl: ctrl
          }
        });
    };

    $scope.deleteAction = function(ev, deleteFunction) {
        var confirm = $mdDialog.confirm()
          .title('Would you like to delete this items?')
          .targetEvent(ev)
          .ok('Delete')
          .cancel('Cancel');
        $mdDialog.show(confirm).then(function() {
          deleteFunction()
        }, function() {});
    };

    $scope.merge_objects = function (obj1,obj2){
        var obj3 = {};
        for (var attrname in obj1) { obj3[attrname] = obj1[attrname]; }
        for (var attrname in obj2) { obj3[attrname] = obj2[attrname]; }
        return obj3;
    }
//    $state.transitionTo('admin.home');
}]);


function FilterDialogController($scope, $mdDialog, ctrl) {
  $scope.hide = function() {
    $mdDialog.hide();
  };
  $scope.cancel = function() {
    $mdDialog.cancel();
  };
  $scope.answer = function(answer) {
    $mdDialog.hide(answer);
  };

  $scope.listCtrl = ctrl;
};

function getListTableOptions() {
    return {
        rowSelection: true,
        multiSelect: true,
        autoSelect: true,
        decapitate: false,
        largeEditDialog: false,
        boundaryLinks: false,
        limitSelect: true,
        pageSelect: true
    };
}