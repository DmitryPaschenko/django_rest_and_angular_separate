'use strict';

angular.module('AdminApp').controller('DocumentListCtrl', function ($scope, documentService, documentTemplateService) {
    var self = this;

    $scope.preController();

    self.selected = [];
    self.listData = [];
    self.filter = {};
    self.availableTemplates = [];

    self.options = getListTableOptions();

    // Change this
    self.query = {
        order: 'name',
        limit: 10,
        page: 1
    };

    self.getListData = function () {
        // Change this
        self.promise = documentService.getDocumentList($scope.merge_objects(self.query, self.filter)).$promise;

        function onSuccess(response) {
            self.listData = response;
        }

        function onError(response) {
            var errorText = response.data.detail === undefined ? 'Get list data error.' : response.data.detail;
            $scope.addDangerAlert('Danger! ' + errorText);
        }

        self.promise.then(onSuccess, onError);
    };

    self.getAvailableTemplates = function () {
        // Change this
        self.promise = documentTemplateService.getAvailableTemplateList([]).$promise;

        function onSuccess(response) {
            self.availableTemplates = response;
        }

        function onError(response) {
            var errorText = response.data.detail === undefined ? 'Get available templates error.' : response.data.detail;
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

        var success = documentService.removeDocuments(ids).then(function(data) {
            $scope.addSuccessAlert('Documents deleted!');
            self.getListData();
            self.selected = [];
        }, function(err) {
            $scope.addDangerAlert('Danger! Documents deleted error!');
            self.getListData();
        });
    };

    var originatorEv;
    self.openAddMenu = function($mdOpenMenu, ev) {
      originatorEv = ev;
      $mdOpenMenu(ev);
    };
    self.notificationsEnabled = true;
    self.toggleNotifications = function() {
      self.notificationsEnabled = !self.notificationsEnabled;
    };

    self.getListData();
    self.getAvailableTemplates();
});

angular.module('AdminApp').controller('DocumentCtrl', function ($scope, $stateParams, documentService, documentTemplateService) {
    var self = this;
    var id = $stateParams.id;

    $scope.preController();

    self.getObject = function (id) {
        // Change this
        self.promise = documentService.getDocument(id).$promise;

        function onSuccess(response) {

            $.each(response.document_values, function( index, item ) {
                if (item.field.widget == 'date') {
                    response.document_values[index].value = moment(item.value).toDate();
                }
                if (item.field.widget == 'number') {
                    response.document_values[index].value = Number(item.value);
                }
            });


            self.model = response;
        }

        function onError(response) {
            var errorText = response.data.detail === undefined ? 'Get document data error.' : response.data.detail;
            $scope.addDangerAlert('Danger! ' + errorText);
        }

        self.promise.then(onSuccess, onError);
    };


    self.updateObject = function(formData, model){
        $scope.clearAlerts();

        function onSuccess(response) {
            $.each(response.document_values, function( index, item ) {
                if (item.field.widget == 'date') {
                    response.document_values[index].value = moment(item.value).toDate();
                }
                if (item.field.widget == 'number') {
                    response.document_values[index].value = Number(item.value);
                }
            });
            self.model = response;
            $scope.addSuccessAlert('Document data saved!')
        }

        function onError(response) {
            var errorText = response.data.detail === undefined ? 'Save document data error.' : response.data.detail;
            $scope.addDangerAlert('Danger! ' + errorText);
        }
        documentService.saveDocument(id, model).$promise.then(onSuccess, onError);
    }

    self.approve = function () {
        // Change this
        self.promise = documentService.setNextStep(id).$promise;

        function onSuccess(response) {
            $scope.addSuccessAlert('User data saved!')
            $state.go('admin.documents.list');
        }

        function onError(response) {
            var errorText = response.detail === undefined ? 'Get document data error.' : response.detail;
            $scope.addDangerAlert('Danger! ' + errorText);
        }

        self.promise.then(onSuccess, onError);
    };

    self.getObject(id);
});

angular.module('AdminApp').controller('DocumentCreateCtrl', function ($scope, $stateParams, documentService, $state, documentTemplateService) {
    var self = this;
    var templateId = $stateParams.template_id;

    $scope.preController();

    self.model = {'name': '', 'template': templateId};

    self.addObject = function(formData, model){
        $scope.clearAlerts();

        function onSuccess(response) {
            $scope.addSuccessAlert('User data saved!')
            $state.go('admin.documents.list');
        }

        function onError(response) {
            var errorText = 'Save document data error.';
            if (response.data.detail !== undefined) {
                if (typeof response.data.detail === 'string')
                    errorText = response.data.detail;

                self.errors = response.data.detail;
            }
            $scope.addDangerAlert('Danger! ' + errorText);
        }
        documentService.addDocument(model).$promise.then(onSuccess, onError);
    }

    self.getAvailableFields = function () {
        // Change this
        self.promise = documentTemplateService.getAvailableTemplateFields(templateId, []).$promise;

        function onSuccess(response) {
            self.availableTemplateFields = response;
            self.model.document_values = self.availableTemplateFields.map(function(field) {
                return {
                    field: {
                        id: field.id,
                        name: field.name,
                        widget_metadata: field.widget_metadata,
                    },
                    name: field.name,
                    widget: field.widget,
                    value: field.widget == 'date' ? new Date() : ''
                };
            });
        }

        function onError(response) {
            var errorText = response.data.detail === undefined ? 'Get template error.' : response.data.detail;
            $scope.addDangerAlert('Danger! ' + errorText);
        }

        self.promise.then(onSuccess, onError);
    };

    self.getAvailableFields();
});