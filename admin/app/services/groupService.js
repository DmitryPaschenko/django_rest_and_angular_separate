'use strict';

angular.module('AdminApp').factory('groupService', function($resource, $cookies) {
    return {
        'getGroupResource': function () {
            return $resource(API_URL + "/groups/:id/", null, {
                'get': { method:'GET' },
                'save': { method:'POST' },
                'update': { method:'PUT' }
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
        }
    }
});