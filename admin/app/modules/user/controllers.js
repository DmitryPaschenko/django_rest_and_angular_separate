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

    $scope.preController();

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
                $state.go('admin.users');
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