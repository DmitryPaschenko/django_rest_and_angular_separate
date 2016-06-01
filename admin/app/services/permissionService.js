'use strict';

angular.module('AdminApp').factory('permissionService', function($resource, $cookies, $q) {
    return {
        'getPermissionResource': function () {
            return $resource(API_URL + "/permissions/:id/", null, {
                'get': { method:'GET' },
                'save': { method:'POST' },
                'update': { method:'PUT' }
            });
        },

        'getContenttypeResource': function () {
            return $resource(API_URL + "/contenttypes/:id/", null, {
                'get': { method:'GET', isArray:true }
            });
        },

        'getPermissionList': function (query) {
            return this.getPermissionResource().get(query);
        },

        'getPermission': function (id) {
            return this.getPermissionResource().get({id: id});
        },

        'savePermission': function (id, data) {
            return this.getPermissionResource().update({id: id}, data);
        },

        'addPermission': function (data) {
            return this.getPermissionResource().save({}, data);
        },

        'getContenttypeList': function (query) {
            return this.getContenttypeResource().get(query);
        },

        'removePermission': function (id) {
            return this.getPermissionResource().remove({id: id});
        },

        'removePermissions': function (ids) {
            var self = this;
            var promises = [];
            ids.forEach(function(id) {
                promises.push(self.removePermission(id).$promise);
            });

            return $q.all(promises);
        }
    }
});