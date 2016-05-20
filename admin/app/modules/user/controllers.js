'use strict';

function configureTopMenu(self) {
    self.topMenuIsOpenConf = {
        isOpen: false,
        count: 0,
        selectedDirection: 'left'
    };
    return self;
}

angular.module('AdminApp').controller('UserListCtrl', function ($scope, userService) {
    var self = this;

    self.selected = [];
    self.listData = [];
    // Change this
    self.query = {
        order: 'username',
        limit: 20,
        page: 1
    };

    self.getListData = function () {
        // Change this
        self.promise = userService.getUserList(self.query).$promise;

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


angular.module('AdminApp').controller('UserCtrl', function ($scope, $stateParams, userService) {
    var self = this;
    var id = $stateParams.userUd;

    self.getObject = function (id) {
        // Change this
        self.promise = userService.getUser(self.query).$promise;

        function onSuccess(response) {
            self.model = response;
        }

        function onError(response) {
            var errorText = response.data.detail === undefined ? 'Get list data error.' : response.data.detail;
            $scope.addDangerAlert('Danger! ' + errorText);
        }

        self.promise.then(onSuccess, onError);
    };

    self.getObject(id);
});