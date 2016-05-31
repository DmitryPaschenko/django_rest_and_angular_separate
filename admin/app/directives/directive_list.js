app.directive('profileAvatar', function() {
  return {
    replace: true,
    template: '<img style="width:80px; height: 80px;" src="data:image/png;base64,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"/>'
  };
});

app.directive('ngEnter', function () {
    return function (scope, element, attrs) {
        element.bind("keydown keypress", function (event) {
            if(event.which === 13) {
                scope.$apply(function (){
                    scope.$eval(attrs.ngEnter);
                });

                event.preventDefault();
            }
        });
    };
});

app.directive('dpUserChips', function () {
    return {
        replace: true,
        controller: 'userChipsCtrl',
        controllerAs: 'userChipsCtrl',
        template: '<div layout="column" ng-cloak><md-content class="md-padding autocomplete" layout="column"><md-contact-chips ng-model="userChipsCtrl.userModel" md-contacts="userChipsCtrl.delayedQuerySearch($query)" md-contact-name="username" md-contact-email="email" md-require-match="true" md-highlight-flags="i" placeholder="Related Users"> </md-contact-chips> </md-content></div>',
        scope: {
            userModel: '='
        },
        bindToController: true
    }
});

app.directive('dpPermissionChips', function () {
    return {
        replace: true,
        controller: 'permissionChipsCtrl',
        controllerAs: 'permissionChipsCtrl',
        template: '<div layout="column" ng-cloak><md-content class="md-padding autocomplete" layout="column"><md-contact-chips ng-model="permissionChipsCtrl.permissionModel" md-contacts="permissionChipsCtrl.delayedQuerySearch($query)" md-contact-name="name" md-require-match="true" md-highlight-flags="i" placeholder="Related Permission"> </md-contact-chips> </md-content></div>',
        scope: {
            permissionModel: '='
        },
        bindToController: true
    }
});

app.directive('dpGroupChips', function () {
    return {
        replace: true,
        controller: 'groupChipsCtrl',
        controllerAs: 'groupChipsCtrl',
        template: '<div layout="column" ng-cloak><md-content class="md-padding autocomplete" layout="column"><md-contact-chips ng-model="groupChipsCtrl.groupModel" md-contacts="groupChipsCtrl.delayedQuerySearch($query)" md-contact-name="name" md-require-match="true" md-highlight-flags="i" placeholder="Related Groups"> </md-contact-chips> </md-content></div>',
        scope: {
            groupModel: '='
        },
        bindToController: true
    }
});


//
//app.directive('updateTitle', ['$rootScope', '$timeout',
//  function($rootScope, $timeout) {
//    return {
//      link: function(scope, element) {
//
//        var listener = function(event, toState) {
//          var title = 'Default Title';
//          if (toState.data && toState.data.pageTitle) title = toState.data.pageTitle;
//
//          $timeout(function() {
//            element.text(title);
//          }, 0, false);
//        };
//
//        $rootScope.$on('$stateChangeSuccess', listener);
//      }
//    };
//  }
//]);