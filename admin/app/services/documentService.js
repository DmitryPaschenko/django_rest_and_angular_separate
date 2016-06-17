'use strict';

angular.module('AdminApp').factory('documentService', function($resource, $cookies, $q, $http) {
    return {
        'getDocumentResource': function () {
            return $resource(API_URL + "/documents/:id/:action", {id: '@id', action: '@action'}, {
                'get': { method:'GET' },
                'save': { method:'POST' },
                'post': { method:'POST' },
                'update': { method:'PUT' },
                'remove': {method: 'DELETE'}
            });
        },

        'getDocumentList': function (query) {
            return this.getDocumentResource().get(query);
        },

        'getDocument': function (id) {
            return this.getDocumentResource().get({id: id});
        },

        'saveDocument': function (id, data) {
            return this.getDocumentResource().update({id: id}, data);
        },

        'addDocument': function (data) {
            return this.getDocumentResource().save({}, data);
        },

        'removeDocument': function (id) {
            return this.getDocumentResource().remove({id: id});
        },

        'removeDocuments': function (ids) {
            var self = this;
            var promises = [];
            ids.forEach(function(id) {
                promises.push(self.removeDocument(id).$promise);
            });

            return $q.all(promises);
        },

        'setNextStep': function (id) {
            return this.getDocumentResource().post({id: id, action: 'next-step'});
        },
    }
});