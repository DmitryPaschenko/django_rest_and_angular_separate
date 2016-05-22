'use strict';

angular.module('AdminApp').factory('userService', function($resource, $cookies) {
    return {
        'getUserResource': function () {
            return $resource(API_URL + "/users/:id/", null, {
                'get': { method:'GET' },
                'update': { method:'PUT' }
            });
        },

        'getUserList': function (query) {
            return this.getUserResource().get(query);
        },

        'getUser': function (id) {
            return this.getUserResource().get({id: id});
        },

        'saveUser': function (id, data) {
            var savedData = data;
            return this.getUserResource().update({id: id}, savedData);
        }
    }
});