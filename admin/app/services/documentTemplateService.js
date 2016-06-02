'use strict';

angular.module('AdminApp').factory('documentTemplateService', function($resource, $cookies, $q) {
    return {
        'getTemplateResource': function () {
            return $resource(API_URL + "/templates/:id/", null, {
                'get': { method:'GET' },
                'save': { method:'POST' },
                'update': { method:'PUT' },
                'remove': {method: 'DELETE'}
            });
        },

        'getTemplateList': function (query) {
            return this.getTemplateResource().get(query);
        },

        'getTemplate': function (id) {
            return this.getTemplateResource().get({id: id});
        },

        'saveTemplate': function (id, data) {
            return this.getTemplateResource().update({id: id}, data);
        },

        'addTemplate': function (data) {
            return this.getTemplateResource().save({}, data);
        },

        'removeTemplate': function (id) {
            return this.getTemplateResource().remove({id: id});
        },

        'removeTemplates': function (ids) {
            var self = this;
            var promises = [];
            ids.forEach(function(id) {
                promises.push(self.removeTemplate(id).$promise);
            });

            return $q.all(promises);
        }
    }
});