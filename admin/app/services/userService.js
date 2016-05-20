'use strict';

angular.module('AdminApp').factory('userService', function($resource, $cookies) {
    return {
        'getUserResource': function () {
            return $resource(API_URL + "/users/:id/");
        },

        'getUserList': function (query) {
            return this.getUserResource().get(query);
        },

        'getUser': function (id) {

            return this.getUserResource().get({id: id});
        }
    }
});