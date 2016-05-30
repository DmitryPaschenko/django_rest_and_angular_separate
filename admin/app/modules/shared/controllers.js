angular.module('AdminApp').controller('userChipsCtrl', userChipsCtrl);

function userChipsCtrl ($timeout, $q, userService, $scope) {
     var self = this;
    var pendingSearch, cancelSearch = angular.noop;
    var cachedQuery, lastSearch;
    self.allContacts = [];
    self.contacts = $scope.userModel;
    self.asyncContacts = [];
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
      console.log(pendingSearch);
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
}