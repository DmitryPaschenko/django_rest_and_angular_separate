'use strict';

function configureTopMenu(self) {
    self.topMenuIsOpenConf = {
        isOpen: false,
        count: 0,
        selectedDirection: 'left'
    };
    return self;
}

angular.module('AdminApp').controller('PermissionListCtrl', function ($scope, permissionService) {
    var self = this;

    $scope.preController();

    self.selected = [];
    self.listData = [];
    // Change this
    self.query = {
        order: 'name',
        limit: 20,
        page: 1
    };

    self.getListData = function () {
        // Change this
        self.promise = permissionService.getPermissionList(self.query).$promise;

        function onSuccess(response) {
            self.listData = response;
        }

        function onError(response) {
            var errorText = response.data.detail === undefined ? 'Get list data error.' : response.data.detail;
            $scope.addDangerAlert('Danger! ' + errorText);
        }

        self.promise.then(onSuccess, onError);
    };

    self.getListData();

    // Top menu block
    self = configureTopMenu(self);
});

angular.module('AdminApp').controller('PermissionCtrl', function ($scope, $stateParams, permissionService) {
    var self = this;
    var id = $stateParams.userId;

    $scope.preController();

    self.getObject = function (id) {
        // Change this
        self.promise = userService.getUser(id).$promise;

        function onSuccess(response) {
            self.model = response;
        }

        function onError(response) {
            var errorText = response.data.detail === undefined ? 'Get list data error.' : response.data.detail;
            $scope.addDangerAlert('Danger! ' + errorText);
        }

        self.promise.then(onSuccess, onError);
    };


    self.updateUser = function(formData, model){
        console.log(formData, model);
        function onSuccess(response) {
            self.model = response;
            $scope.addSuccessAlert('User data saved!')
        }

        function onError(response) {
            var errorText = response.data.detail === undefined ? 'Save user data error.' : response.data.detail;
            $scope.addDangerAlert('Danger! ' + errorText);
        }
        userService.saveUser(id, model).$promise.then(onSuccess, onError);

    }

    self.getObject(id);
});

angular.module('AdminApp').controller('PermissionCreateCtrl', function ($scope, $stateParams, permissionService) {
    var self = this;

    $scope.preController();

    self.contentTypes = [{
        "id": 8,
        "app_label": "account",
        "model": "emailaddress"
      },
      {
        "id": 9,
        "app_label": "account",
        "model": "emailconfirmation"
      }];

    self.model = {'name': '', 'codename': '', 'content_type': ''};

    self.addPermission = function(formData, model){
        $scope.clearAlerts();

        function onSuccess(response) {
            $scope.addSuccessAlert('User data saved!')
            $state.go('admin.permissions');
        }

        function onError(response) {
            var errorText = response.data.detail === undefined ? 'Save permission data error.' : response.data.detail;
            $scope.addDangerAlert('Danger! ' + errorText);
        }
        permissionService.addPermission(model).$promise.then(onSuccess, onError);

    }
});