'use strict';

angular.module('AdminApp')
  .controller('UserprofileCtrl', function ($scope, djangoAuth, Validate) {
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
        	$scope.complete = true;
        },function(data){
        	// error case
        	$scope.error = data;
        });
      }
    }
  });
