'use strict';

angular.module('AdminApp').controller('UserListCtrl', function ($scope, userService) {
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
        order: 'username',
        limit: 10,
        page: 1
    };

    self.getListData = function () {
        // Change this
        self.promise = userService.getUserList($scope.merge_objects(self.query, self.filter)).$promise;

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


angular.module('AdminApp').controller('UserCtrl', function ($scope, $stateParams, userService) {
    var self = this;
    var id = $stateParams.userId;

    $scope.preController();

    self.getObject = function (id) {
        // Change this
        self.promise = userService.getUser(id).$promise;

        function onSuccess(response) {
            self.model = response;
            $scope.userTitle = self.model.username;
        }

        function onError(response) {
            var errorText = response.data.detail === undefined ? 'Get list data error.' : response.data.detail;
            $scope.addDangerAlert('Danger! ' + errorText);
        }

        self.promise.then(onSuccess, onError);
    };


    self.updateUser = function(formData, model){
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

angular.module('AdminApp').controller('UserCreateCtrl', function ($scope, $stateParams, djangoAuth, Validate, $state) {
    var self = this;

    $scope.preController();


    self.model = {'username':'','password1':'','password2':'', 'email':''};

    self.register = function(formData){
        $scope.clearAlerts();
        Validate.form_validation(formData,$scope.errors);
        if(!formData.$invalid){
            djangoAuth.register(self.model.username,self.model.password1,self.model.password2,self.model.email)
            .then(function(data){
        	    $scope.addSuccessAlert('User created!');
                $state.go('admin.users.list');
            },function(data){
                for(var index in data) {
                    if (index !== 'status') {
                        $scope.addDangerAlert('Danger! ' + data[index]);
                    }
                }
                self.errors = data;
            });
        }
    }
});