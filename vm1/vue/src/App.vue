<template>
  <div id="app">
    <Popup v-if="showPopup" @closePopup="showPopup = false" />
    <SendMessage v-else />
  </div>
</template>

<script>
import SendMessage from './components/SendMessage.vue';
import Popup from './components/Popup.vue';

export default {
  name: 'App',
  components: {
    SendMessage,
    Popup,
  },
  data() {
    return {
      showPopup: true, // Show popup initially
    };
  },
};
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
