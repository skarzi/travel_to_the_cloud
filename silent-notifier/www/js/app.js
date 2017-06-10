// Ionic Starter App

// angular.module is a global place for creating, registering and retrieving Angular modules
// 'starter' is the name of this angular module example (also set in a <body> attribute in index.html)
// the 2nd parameter is an array of 'requires'
angular.module('starter', ['ionic', 'ionic.cloud', 'starter.controllers'])

.config(function($stateProvider, $urlRouterProvider, $ionicCloudProvider) {
  $ionicCloudProvider
  .init({
    "core": {
      "app_id": "563737ef"
    },
    "push": {
      "sender_id": "631634326100",
      "pluginConfig": {
        "android": {
          "iconColor": "#343434"
        }
      }
    }
  });

  $stateProvider
  .state('default', {
    url: '/',
    templateUrl: 'templates/default.html',
    controller: 'RecorderCtrl'
  })
  .state('video', {
    url: '/video/:text/:clip_location/',
    templateUrl: 'templates/video.html',
    controller: 'VideoCtrl'
  });

  $urlRouterProvider.otherwise('/');
})

.filter('trusted', ['$sce', function ($sce) {
    return function(url) {
        return $sce.trustAsResourceUrl(url);
    };
}])

.run(function($ionicPlatform, $ionicPush, $state, $rootScope) {
  $ionicPlatform.ready(function() {
    if(window.cordova && window.cordova.plugins.Keyboard) {
      // Hide the accessory bar by default (remove this to show the accessory bar above the keyboard
      // for form inputs)
      cordova.plugins.Keyboard.hideKeyboardAccessoryBar(true);

      // Don't remove this line unless you know what you are doing. It stops the viewport
      // from snapping when text inputs are focused. Ionic handles this internally for
      // a much nicer keyboard experience.
      cordova.plugins.Keyboard.disableScroll(true);
    }
    if(window.StatusBar) {
      StatusBar.styleDefault();
    }
    $ionicPush.register({
      canShowAlert: true,
      canSetBadge: true,
      canPlaySound: true,
      canRunActionsOnWake: true,
      onNotification: function(n) {
        console.log(n);
        return true;
      }
    }).then(function(t) {
      return $ionicPush.saveToken(t);
    }).then(function(t) {
      console.log('Token saved:', t.token);
    });

    $rootScope.$on('cloud:push:notification', function(event, data) {
      console.log("notification received...");
      console.log(data);
      $state.go('video', {text: data.message.payload.text, clip_location: "http://172.16.102.47:7744/" + data.message.payload.clip_location});
    });

    $state.go("default");
  });
})

