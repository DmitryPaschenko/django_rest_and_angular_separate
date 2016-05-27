'use strict';

angular.module('AdminApp').controller('GroupListCtrl', function ($scope, groupService) {
    var self = this;

    $scope.preController();

    self.selected = [];
    self.listData = [];
    self.filter = {};

    self.options = getListTableOptions();

    // Change this
    self.query = {
        order: 'name',
        limit: 10,
        page: 1
    };

    self.getListData = function () {
        // Change this
        self.promise = groupService.getGroupList($scope.merge_objects(self.query, self.filter)).$promise;

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

    self.getListData();
});

angular.module('AdminApp').controller('GroupCtrl', function ($scope, $stateParams, groupService) {
    var self = this;
    var id = $stateParams.id;

    $scope.preController();

    self.getObject = function (id) {
        // Change this
        self.promise = groupService.getGroup(id).$promise;

        function onSuccess(response) {
            self.model = response;
        }

        function onError(response) {
            var errorText = response.data.detail === undefined ? 'Get group data error.' : response.data.detail;
            $scope.addDangerAlert('Danger! ' + errorText);
        }

        self.promise.then(onSuccess, onError);
    };


    self.updateObject = function(formData, model){

        function onSuccess(response) {
            self.model = response;
            $scope.addSuccessAlert('Group data saved!')
        }

        function onError(response) {
            var errorText = response.data.detail === undefined ? 'Save group data error.' : response.data.detail;
            $scope.addDangerAlert('Danger! ' + errorText);
        }
        groupService.saveGroup(id, model).$promise.then(onSuccess, onError);

    }

    self.getObject(id);
});

angular.module('AdminApp').controller('GroupCreateCtrl', function ($scope, $stateParams, groupService, $state) {
    var self = this;

    $scope.preController();

    self.model = {'name': ''};

    self.addObject = function(formData, model){
        $scope.clearAlerts();

        function onSuccess(response) {
            $scope.addSuccessAlert('User data saved!')
            $state.go('admin.groups.list');
        }

        function onError(response) {
            var errorText = 'Save group data error.';
            if (response.data.detail !== undefined) {
                if (typeof response.data.detail === 'string')
                    errorText = response.data.detail;

                self.errors = response.data.detail;
            }
            $scope.addDangerAlert('Danger! ' + errorText);
        }
        groupService.addGroup(model).$promise.then(onSuccess, onError);
    }
});