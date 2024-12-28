<template>
  <div>
    <div id="map" style="height: 600px;"></div>
    <h2>Coordonnées en temps réel</h2>
    <ul>
      <li 
        v-for="(coord, index) in coordinates" 
        :key="index" 
        :class="'id-' + coord.id" >
        ID: {{ coord.id }} - Latitude: {{ coord.latitude }} - Longitude: {{ coord.longitude }}
      </li>
    </ul>
    
   
  </div>
</template>

<script>

import L from "leaflet";
import "leaflet/dist/leaflet.css";


export default {
  data() {
    return {
      messages: [], // Messages from the /messages endpoint
      coordinates: [], // Real-time coordinates from WebSocket
    };
  },
  methods: {
    async fetchMessages() {
      try {
        const response = await axios.get("http://localhost:8000/messages");
        this.messages = response.data.messages;
        console.log("Messages reçus depuis l'API :", this.messages);
      } catch (error) {
        console.error("Erreur lors de la récupération des messages :", error);
      }
    },
    connectWebSocket() {
      this.socket = new WebSocket("ws://localhost:8000/ws");

      this.socket.onopen = () => {
        console.log("WebSocket connecté !");
      };

      this.socket.onmessage = (event) => {
        console.log("Message reçu via WebSocket :", event.data);
        // Assuming the data is a JSON string, parse it
        const data = JSON.parse(event.data);
        this.coordinates.push(data); // Add the coordinates to the list
      };

      this.socket.onclose = () => {
        console.log("WebSocket déconnecté.");
      };

      this.socket.onerror = (error) => {
        console.error("Erreur WebSocket :", error);
      };
    },
  },
  mounted() {
    this.connectWebSocket();
  },
};
</script>

<style scoped>
h1 {
  font-size: 2em;
  margin-bottom: 20px;
}

button {
  padding: 10px 20px;
  font-size: 1em;
  margin-bottom: 20px;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  background: #f9f9f9;
  margin: 5px 0;
  padding: 10px;
  border-radius: 5px;
}

.id-1 {
  background-color: lightblue;
}

.id-2 {
  background-color: lightgreen;
}

.id-3 {
  background-color: lightcoral;
}

</style>
