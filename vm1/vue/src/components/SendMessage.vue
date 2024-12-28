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
      coordinatesById: {
            1: [], // Coordinates for individual 1
            2: [], // Coordinates for individual 2
          },
      polylinesById: {
            1: null, // Polyline for individual 1
            2: null, // Polyline for individual 2
          },
    markersById: {
      1: null, // Marker for the head of individual 1's polyline
      2: null, // Marker for the head of individual 2's polyline
    },
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
  const data = JSON.parse(event.data);

  // Add the new coordinate to the appropriate individual's array
  if (this.coordinatesById[data.id]) {
    this.coordinatesById[data.id].push([data.latitude, data.longitude]);

    // Update the polyline
    if (this.polylinesById[data.id]) {
      this.polylinesById[data.id].setLatLngs(this.coordinatesById[data.id]);
    } else {
      // Create the polyline if it doesn't exist
      const color = data.id === 1 ? 'blue' : 'red';
      this.polylinesById[data.id] = L.polyline(this.coordinatesById[data.id], {
        color: color,
        weight: 4,
        opacity: 0.7,
      }).addTo(this.map);
    }

    // Update or create the marker for the head of the polyline
    const lastCoord = this.coordinatesById[data.id][this.coordinatesById[data.id].length - 1];

    if (this.markersById[data.id]) {
      this.markersById[data.id].setLatLng(lastCoord); // Move the existing marker to the new position
    } else {
      const icon = L.icon({
        iconUrl: data.id === 1 ? 'omar.jpeg' : 'zitt.png', // Replace with appropriate icon paths
        iconSize: [25, 41], // Adjust size as needed
        iconAnchor: [12, 41], // Anchor point
      });

      this.markersById[data.id] = L.marker(lastCoord, { icon: icon }).addTo(this.map);
    }

    // Optionally adjust the map bounds
    const bounds = L.latLngBounds(
      Object.values(this.polylinesById).map((polyline) => polyline.getBounds())
    );
    this.map.fitBounds(bounds);
  } else {
    console.warn(`Received coordinates for unknown ID: ${data.id}`);
  }
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

  // Initialize the map
  this.map = L.map("map").setView([43.30761833544262, -0.373750699597043], 13);

  // Add a tile layer
  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
  }).addTo(this.map);
}



  
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

#map { height: 180px; }

</style>
