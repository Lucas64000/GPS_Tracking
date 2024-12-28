<template>
  <div id="app">
    <h1>WebSocket Client</h1>
    <p>Vérifiez la console du navigateur pour voir les coordonnées reçues.</p>
  </div>
</template>

<script>
export default {
  name: "App",
  data() {
    return {
      socket: null,
    };
  },
  mounted() {
    // Remplacez l'URL par celle de votre serveur WebSocket
    this.socket = new WebSocket("ws://localhost:8000/ws");

    this.socket.onopen = () => {
      console.log("WebSocket connection established.");
    };

    this.socket.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        console.log("Coordonnées reçues :", data);
      } catch (error) {
        console.error("Erreur lors du traitement du message WebSocket :", error);
      }
    };

    this.socket.onerror = (error) => {
      console.error("WebSocket error:", error);
    };

    this.socket.onclose = () => {
      console.log("WebSocket connection closed.");
    };
  },
  beforeUnmount() {
    if (this.socket) {
      this.socket.close();
    }
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
