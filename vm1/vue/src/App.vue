<template>
    <div id="app">
      <SendMessage />
    </div>
  </template>
  
  <script>
  import SendMessage from './components/SendMessage.vue'
  
  export default {
    name: 'App',
    components: {
      SendMessage
    }
  }
  </script>
  
  <style>
  #app {
    font-family: Avenir, Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
    margin-top: 60px;
  }
  </style>