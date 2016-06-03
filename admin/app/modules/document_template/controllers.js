'use strict';

angular.module('AdminApp').controller('DocumentTemplateListCtrl', function ($scope, documentTemplateService) {
    var self = this;

    $scope.preController();

    self.selected = [];
    self.listData = [];
    self.filter = {};

    self.options = getListTableOptions();

    // Change this
    self.query = {
        order: 'name',
        limit: 10,
        page: 1
    };

    self.getListData = function () {
        // Change this
        self.promise = documentTemplateService.getTemplateList($scope.merge_objects(self.query, self.filter)).$promise;

        function onSuccess(response) {
            self.listData = response;
        }

        function onError(response) {
            var errorText = response.data.detail === undefined ? 'Get list data error.' : response.data.detail;
            $scope.addDangerAlert('Danger! ' + errorText);
        }

        self.promise.then(onSuccess, onError);
    };

    self.clearFilter = function (filterName) {
        if (filterName == undefined) {
            self.filter = {};
        } else {
            self.filter[filterName] = '';
        }
        self.getListData();
    };

    self.batchDelete = function () {
        $scope.clearAlerts();
        var ids = self.selected.map(function(item) {
            return item.id;
        });

        var success = documentTemplateService.removeTemplates(ids).then(function(data) {
            $scope.addSuccessAlert('Templates deleted!');
            self.getListData();
            self.selected = [];
        }, function(err) {
            $scope.addDangerAlert('Danger! Templates deleted error!');
            self.getListData();
        });
    };

    self.getListData();
});

angular.module('AdminApp').controller('DocumentTemplateCtrl', function ($scope, $stateParams, documentTemplateService, groupService) {
    var self = this;
    var id = $stateParams.id;

    $scope.preController();

    self.field_widgets = getTemplateWidgets();

    /* GET GROUP DATA */
    self.groups = [];
    groupService.getAllGroups({}).$promise.then(
        function (response) {
            self.groups = response;
        },
        function (response) {
            $scope.addDangerAlert('Danger! Group list did not retrieve');
        }
    );

    self.getObject = function (id) {
        // Change this
        self.promise = documentTemplateService.getTemplate(id).$promise;

        function onSuccess(response) {
            self.model = response;
        }

        function onError(response) {
            var errorText = response.data.detail === undefined ? 'Get template data error.' : response.data.detail;
            $scope.addDangerAlert('Danger! ' + errorText);
        }

        self.promise.then(onSuccess, onError);
    };


    self.updateObject = function(formData, model){
        $scope.clearAlerts();

        function onSuccess(response) {
            self.model = response;
            $scope.addSuccessAlert('Template data saved!')
        }

        function onError(response) {
            var errorText = response.data.detail === undefined ? 'Save template data error.' : response.data.detail;
            $scope.addDangerAlert('Danger! ' + errorText);
        }
        documentTemplateService.saveTemplate(id, model).$promise.then(onSuccess, onError);

    }

    self.getObject(id);
});

angular.module('AdminApp').controller('DocumentTemplateCreateCtrl', function ($scope, $stateParams, documentTemplateService, $state, groupService) {
    var self = this;

    $scope.preController();

    self.model = {
        'name': '',

        'template_fields': [{name: '', widget: ''}],
        'template_steps': [{name: '', members_group: '', editors_group: '', viewers_group: ''}]
    };

    self.field_widgets = getTemplateWidgets();

    /* GET GROUP DATA */
    self.groups = [];
    groupService.getAllGroups({}).$promise.then(
        function (response) {
            self.groups = response;
        },
        function (response) {
            $scope.addDangerAlert('Danger! Group list did not retrieve');
        }
    );

    self.addObject = function(formData, model){
        $scope.clearAlerts();

        function onSuccess(response) {
            $scope.addSuccessAlert('User data saved!')
            $state.go('admin.templates.list');
        }

        function onError(response) {
            var errorText = 'Save template data error.';
            if (response.data.detail !== undefined) {
                if (typeof response.data.detail === 'string')
                    errorText = response.data.detail;

                self.errors = response.data.detail;
            }
            $scope.addDangerAlert('Danger! ' + errorText);
        }
        documentTemplateService.addTemplate(model).$promise.then(onSuccess, onError);
    };

    self.addField = function(){
        var newField = {name: '', template: ''};
        self.model.template_fields.push(newField);
    };

    self.addStep = function(){
        var newStep = {name: '', members_group: '', editors_group: '', viewers_group: ''};
        self.model.template_steps.push(newStep);
    };
});

function getTemplateWidgets() {
    return self.field_widgets = [
        {
            key: 'string',
            title: 'String'
        },
        {
            key: 'text',
            title: 'Text'
        },
        {
            key: 'calculated',
            title: 'Calculated'
        }
    ];
}