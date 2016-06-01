'use strict';

angular.module('AdminApp').factory('groupService', function($resource, $cookies, $q) {
    return {
        'getGroupResource': function () {
            return $resource(API_URL + "/groups/:id/", null, {
                'get': { method:'GET' },
                'save': { method:'POST' },
                'update': { method:'PUT' },
                'remove': {method: 'DELETE'}
            });
        },

        'getGroupList': function (query) {
            return this.getGroupResource().get(query);
        },

        'getGroup': function (id) {
            return this.getGroupResource().get({id: id});
        },

        'saveGroup': function (id, data) {
            return this.getGroupResource().update({id: id}, data);
        },

        'addGroup': function (data) {
            return this.getGroupResource().save({}, data);
        },

        'removeGroup': function (id) {
            return this.getGroupResource().remove({id: id});
        },

        'removeGroups': function (ids) {
            var self = this;
            var promises = [];
            ids.forEach(function(id) {
                promises.push(self.removeGroup(id).$promise);
            });

            return $q.all(promises);
        }
    }
});