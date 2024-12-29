<template>
  <div>
    <h1>WhereIsMyDads</h1>
    <div class="map-container"><div id="map" style="height: 500px;"></div></div>
    <div>
      <button @click="toggleVisibility(1)">Afficher Papa 1</button>
      <button @click="toggleVisibility(2)">Afficher Papa 2</button>
      <button @click="focusOnPolyline(1)">Focus Papa 1</button>
      <button @click="focusOnPolyline(2)">Focus Papa 2</button>
    </div>
   
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
      visibilityById: {
        1: true, // Visibility for individual 1's polyline
        2: true, // Visibility for individual 2's polyline
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
        iconUrl: data.id === 1 ? 'omar.jpeg' : 'raph.png', // Replace with appropriate icon paths
        iconSize: [25, 41], // Adjust size as needed
        iconAnchor: [12, 41], // Anchor point
      });

      this.markersById[data.id] = L.marker(lastCoord, { icon: icon }).addTo(this.map);
    }

    // Remove fitBounds or any map adjustment logic to prevent refocusing
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
    focusOnPolyline(id) {
    if (this.polylinesById[id]) {
      this.map.fitBounds(this.polylinesById[id].getBounds());
    }
  },
  toggleVisibility(id) {
    if (this.polylinesById[id]) {
      if (this.visibilityById[id]) {
        // Hide the polyline and marker
        this.map.removeLayer(this.polylinesById[id]);
        if (this.markersById[id]) {
          this.map.removeLayer(this.markersById[id]);
        }
      } else {
        // Show the polyline and marker
        this.map.addLayer(this.polylinesById[id]);
        if (this.markersById[id]) {
          this.map.addLayer(this.markersById[id]);
        }
      }
      // Toggle the visibility state
      this.visibilityById[id] = !this.visibilityById[id];
    }
  },
  },
  mounted() {
  this.connectWebSocket();

  // Initialize the map
  this.map = L.map("map").setView([43.30761833544262, -0.373750699597043], 11);

  // Add a tile layer
  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
  }).addTo(this.map);
}



  
};
</script>

<style scoped>
/* General Styles */
body {
  font-family: 'Press Start 2P', cursive; /* Retro arcade-style font */
  background: radial-gradient(circle, #141e30, #243b55); /* Dark gradient background */
  color: #fff; /* Neon white text */
  margin: 0;
  padding: 0;
}

/* Header */
h1 {
  font-size: 3em;
  text-align: center;
  margin-bottom: 20px;
  text-shadow: 0 0 10px #00ffff, 0 0 20px #00ffff, 0 0 30px #00ffff;
  color: #00ffff; /* Neon cyan */
}

/* Buttons */
button {
  padding: 15px 30px;
  font-size: 1em;
  font-family: inherit;
  border: none;
  margin: 10px;
  cursor: pointer;
  color: #fff;
  background: linear-gradient(45deg, #ff00cc, #3333ff);
  border-radius: 5px;
  box-shadow: 0 0 5px #ff00cc, 0 0 15px #ff00cc, 0 0 20px #3333ff, 0 0 30px #3333ff;
  transition: transform 0.2s, box-shadow 0.2s;
}

button:hover {
  transform: scale(1.1);
  box-shadow: 0 0 15px #ff00cc, 0 0 25px #ff00cc, 0 0 35px #3333ff, 0 0 50px #3333ff;
}

/* Map Container */
.map-container {
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 20px 0;
}

#map {
  height: 500px;
  width: 80%;
  border: 2px solid #ff00cc;
  box-shadow: 0 0 10px #3333ff, 0 0 20px #ff00cc, 0 0 30px #ff00cc;
  border-radius: 10px;
}

/* Buttons Container */
div > div {
  text-align: center;
  margin-top: 20px;
}

/* Retro List Items (Optional) */
li {
  background: linear-gradient(45deg, #ff00cc, #3333ff);
  color: #fff;
  margin: 5px 0;
  padding: 10px;
  border-radius: 5px;
  text-shadow: 0 0 5px #00ffff, 0 0 10px #00ffff;
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
