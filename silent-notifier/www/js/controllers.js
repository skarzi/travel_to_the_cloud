angular.module('starter.controllers', ['ngCordova'])

.controller('RecorderCtrl', function($scope, $http, $state) {
    console.log("entered RecorderCtrl");

    function onDeviceReady() {
        console.log("ready");
    };

    function uploadSuccess(response) {
        console.log("upload success");
        console.log(response);

        var data = JSON.parse(response.response);
        var clip_location = data.clip_location;
        var text = data.text;
        console.log(text, clip_location);
        document.getElementById("loader").setAttribute("class", "");
        $state.go('video', {text: text, clip_location: "http://172.16.102.47:7744/" + clip_location});
    };

    function uploadError(error) {
        console.log("upload error");
        console.log(error);
        document.getElementById("loader").setAttribute("class", "");
    }

    function captureSuccess(mediaFiles) {
        console.log("capture success");
        var file = mediaFiles[0];
        var options = new FileUploadOptions();
        options.fileKey = "audio";
        options.fileName = "audio.amr";
        options.mimeType = "audio/amr";
        options.chunkedMode = false;
        var ft = new FileTransfer();
        ft.upload(
            file.fullPath,
            encodeURI("http://172.16.102.47:5000/"),
            uploadSuccess,
            uploadError,
            options
        );
        document.getElementById("loader").setAttribute("class", "visible");
    };

    function captureError(error) {
        console.log("capture error");
        console.log(error);
    };

    $scope.record = function() {
        console.log("recording started...");
        var options = { limit: 1, duration: 30};
        navigator.device.capture.captureAudio(captureSuccess, captureError, options);
    }

    $scope.send = function () {
        console.log("sending...");
        $http({
            method: 'POST',
            url: 'http://172.16.102.47:5000/',
            data: {"text": document.getElementById("text-input").value}
        }).then(function successCallback(response) {
            console.log("sending success");
            console.log(response);
            document.getElementById("loader").setAttribute("class", "");
            $state.go('video', {text: response.data.text, clip_location: "http://172.16.102.47:7744/" + response.data.clip_location});
        }, function errorCallback(response) {
            console.log("sending error");
            console.log(response);
            document.getElementById("loader").setAttribute("class", "");
        });
        document.getElementById("loader").setAttribute("class", "visible");
    }

    document.addEventListener("deviceready", onDeviceReady, false);
})

.controller('VideoCtrl', function($scope, $state, $stateParams, $http) {

    $scope.goBack = function () {
        $state.go("default");
    };

    console.log("entered VideoCtrl");
    console.log($stateParams.text, $stateParams.clip_location);
    $scope.text = $stateParams.text;
    $scope.clip_location = $stateParams.clip_location;
    document.getElementById('text').value = $stateParams.text;
    document.getElementById('video').setAttribute('src', $stateParams.clip_location);
});