'use strict';

angular.module('AdminApp')
  .controller('UserprofileCtrl', function ($scope, djangoAuth, Validate) {
    $scope.alerts = [];

    $scope.user_profile_model = {'first_name':'','last_name':'','email':''};
  	$scope.complete = false;
  	djangoAuth.profile().then(function(data){
  		$scope.user_profile_model = data;
  	});
    $scope.updateProfile = function(formData, model){
      $scope.errors = [];
      Validate.form_validation(formData,$scope.errors);
      if(!formData.$invalid){
        djangoAuth.updateProfile(model)
        .then(function(data){
        	// success case
        	$scope.addSuccessAlert('Well done! You successfully read this important alert message.');
        },function(data){
        	// error case
        	$scope.addDangerAlert('Danger! There are some errors');
        	$scope.error = data;
        });
      }
    }

  });
