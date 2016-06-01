'use strict';

angular.module('AdminApp').controller('PermissionListCtrl', function ($scope, permissionService) {
    var self = this;

    $scope.preController();

    self.selected = [];
    self.listData = [];
    self.filter = {};

    self.options = {
        rowSelection: true,
        multiSelect: true,
        autoSelect: true,
        decapitate: false,
        largeEditDialog: false,
        boundaryLinks: false,
        limitSelect: true,
        pageSelect: true
    };

    // Change this
    self.query = {
        order: 'name',
        limit: 10,
        page: 1,
        fields: 'id,name'
    };

    self.getListData = function () {
        // Change this
        self.promise = permissionService.getPermissionList($scope.merge_objects(self.query, self.filter)).$promise;

        function onSuccess(response) {
            self.listData = response;
        }

        function onError(response) {
            var errorText = response.data.detail === undefined ? 'Get list data error.' : response.data.detail;
            $scope.addDangerAlert('Danger! ' + errorText);
        }

        self.promise.then(onSuccess, onError);
    };

    self.clearFilter = function (filterName) {
        if (filterName == undefined) {
            self.filter = {};
        } else {
            self.filter[filterName] = '';
        }
        self.getListData();
    };

    self.batchDelete = function () {
        $scope.clearAlerts();
        var ids = self.selected.map(function(item) {
            return item.id;
        });

        var success = permissionService.removePermissions(ids).then(function(data) {
            $scope.addSuccessAlert('Permissions deleted!');
            self.getListData();
            self.selected = [];
        }, function(err) {
            $scope.addDangerAlert('Danger! Permissions deleted error!');
            self.getListData();
        });
    };

    self.getListData();
});

angular.module('AdminApp').controller('PermissionCtrl', function ($scope, $stateParams, permissionService) {
    var self = this;
    var id = $stateParams.id;

    $scope.preController();

    self.contentTypes = [];
    permissionService.getContenttypeList({}).$promise.then(function (response){
        self.contentTypes = response;
    });

    self.getObject = function (id) {
        // Change this
        self.promise = permissionService.getPermission(id).$promise;

        function onSuccess(response) {
            self.model = response;
        }

        function onError(response) {
            var errorText = response.data.detail === undefined ? 'Get permission data error.' : response.data.detail;
            $scope.addDangerAlert('Danger! ' + errorText);
        }

        self.promise.then(onSuccess, onError);
    };


    self.updateObject = function(formData, model){

        function onSuccess(response) {
            self.model = response;
            $scope.addSuccessAlert('User data saved!')
        }

        function onError(response) {
            var errorText = response.data.detail === undefined ? 'Save user data error.' : response.data.detail;
            $scope.addDangerAlert('Danger! ' + errorText);
        }

        self.model.user_set = self.model.users.map(function(user) {
            return user.id;
        });

        permissionService.savePermission(id, model).$promise.then(onSuccess, onError);

    }

    self.getObject(id);
});

angular.module('AdminApp').controller('PermissionCreateCtrl', function ($scope, $stateParams, permissionService, $state) {
    var self = this;

    $scope.preController();

    self.contentTypes = [];
    permissionService.getContenttypeList({}).$promise.then(function (response){
        self.contentTypes = response;
    });

    self.model = {'name': '', 'codename': '', 'content_type': '', 'users': []};

    self.addPermission = function(formData, model){
        $scope.clearAlerts();

        function onSuccess(response) {
            $scope.addSuccessAlert('User data saved!')
            $state.go('admin.permissions.list');
        }

        function onError(response) {
            var errorText = response.data.detail === undefined ? 'Save permission data error.' : response.data.detail;
            $scope.addDangerAlert('Danger! ' + errorText);
        }

        self.model.user_set = self.model.users.map(function(user) {
            return user.id;
        });

        permissionService.addPermission(model).$promise.then(onSuccess, onError);

    }
});