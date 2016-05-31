angular.module('AdminApp').controller('userChipsCtrl', userChipsCtrl);
angular.module('AdminApp').controller('permissionChipsCtrl', permissionChipsCtrl);
angular.module('AdminApp').controller('groupChipsCtrl', groupChipsCtrl);

function userChipsCtrl ($timeout, $q, userService, $scope) {
     var self = this;
    var pendingSearch, cancelSearch = angular.noop;
    var cachedQuery, lastSearch;
    self.allContacts = [];
    self.filterSelected = true;
    self.querySearch = querySearch;
    self.delayedQuerySearch = delayedQuerySearch;

    function querySearch (criteria) {
      cachedQuery = cachedQuery || criteria;
      return cachedQuery ? self.allContacts : [];
    }

    function delayedQuerySearch(criteria) {
      cachedQuery = criteria;
      if ( !pendingSearch || !debounceSearch() )  {
        cancelSearch();
        pendingSearch = $q(function(resolve, reject) {
          cancelSearch = reject;

          var params = {'search': criteria};
          if (self.userModel != undefined && self.userModel.length) {
            params.exclude_ids = self.userModel.map(function(user) {
                return user.id;
            }).join(',');
          }
          userService.getUserList(params).$promise.then(function (response) {
            self.allContacts = response.results;
            resolve( self.querySearch() );
            refreshDebounce();
          });

        });
        return pendingSearch;
      }
      return pendingSearch;
    }
    function refreshDebounce() {
      lastSearch = 0;
      pendingSearch = null;
      cancelSearch = angular.noop;
    }

    function debounceSearch() {
      var now = new Date().getMilliseconds();
      lastSearch = lastSearch || now;
      return ((now - lastSearch) < 300);
    }
};

function permissionChipsCtrl ($timeout, $q, permissionService, $scope) {
     var self = this;
    var pendingSearch, cancelSearch = angular.noop;
    var cachedQuery, lastSearch;
    self.allPermissions = [];
    self.filterSelected = true;
    self.querySearch = querySearch;
    self.delayedQuerySearch = delayedQuerySearch;

    function querySearch (criteria) {
      cachedQuery = cachedQuery || criteria;
      return cachedQuery ? self.allPermissions : [];
    }

    function delayedQuerySearch(criteria) {
      cachedQuery = criteria;
      if ( !pendingSearch || !debounceSearch() )  {
        cancelSearch();
        pendingSearch = $q(function(resolve, reject) {
          cancelSearch = reject;

          var params = {'search': criteria, 'fields': 'id,name'};
          if (self.permissionModel != undefined && self.permissionModel.length) {
            params.exclude_ids = self.permissionModel.map(function(permission) {
                return permission.id;
            }).join(',');
          }
          permissionService.getPermissionList(params).$promise.then(function (response) {
            self.allPermissions = response.results;
            resolve( self.querySearch() );
            refreshDebounce();
          });

        });
        return pendingSearch;
      }
      return pendingSearch;
    }
    function refreshDebounce() {
      lastSearch = 0;
      pendingSearch = null;
      cancelSearch = angular.noop;
    }

    function debounceSearch() {
      var now = new Date().getMilliseconds();
      lastSearch = lastSearch || now;
      return ((now - lastSearch) < 300);
    }
};

function groupChipsCtrl ($timeout, $q, groupService, $scope) {
     var self = this;
    var pendingSearch, cancelSearch = angular.noop;
    var cachedQuery, lastSearch;
    self.allGroups = [];
    self.filterSelected = true;
    self.querySearch = querySearch;
    self.delayedQuerySearch = delayedQuerySearch;

    function querySearch (criteria) {
      cachedQuery = cachedQuery || criteria;
      return cachedQuery ? self.allGroups : [];
    }

    function delayedQuerySearch(criteria) {
      cachedQuery = criteria;
      if ( !pendingSearch || !debounceSearch() )  {
        cancelSearch();
        pendingSearch = $q(function(resolve, reject) {
          cancelSearch = reject;

          var params = {'name': criteria};
          if (self.groupModel != undefined && self.groupModel.length) {
            params.exclude_ids = self.groupModel.map(function(group) {
                return group.id;
            }).join(',');
          }
          groupService.getGroupList(params).$promise.then(function (response) {
            self.allGroups = response.results;
            resolve( self.querySearch() );
            refreshDebounce();
          });

        });
        return pendingSearch;
      }
      return pendingSearch;
    }
    function refreshDebounce() {
      lastSearch = 0;
      pendingSearch = null;
      cancelSearch = angular.noop;
    }

    function debounceSearch() {
      var now = new Date().getMilliseconds();
      lastSearch = lastSearch || now;
      return ((now - lastSearch) < 300);
    }
};