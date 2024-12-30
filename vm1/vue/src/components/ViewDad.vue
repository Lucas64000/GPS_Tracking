<template>
    <div>
      <div>
        <!-- Daddy 1 -->
        <div class="blue">
          <label for="startDateBlue">Start Date (Blue Polyline):</label>
          <input type="datetime-local" v-model="startDateBlue" @change="filterPoints" />
  
          <label for="endDateBlue">End Date (Blue Polyline):</label>
          <input type="datetime-local" v-model="endDateBlue" @change="filterPoints" />
          <button class="blue" @click="toggleBluePolylineVisibility">
            {{ blueVisible ? 'Hide Blue Polyline' : 'Show Blue Polyline' }}
          </button>
        </div>
  
        <!-- Daddy 2 -->
        <div class="red">
          <label for="startDateRed">Start Date (Red Polyline):</label>
          <input type="datetime-local" v-model="startDateRed" @change="filterPoints" />
  
          <label for="endDateRed">End Date (Red Polyline):</label>
          <input type="datetime-local" v-model="endDateRed" @change="filterPoints" />
          <button class="red" @click="toggleRedPolylineVisibility">
            {{ redVisible ? 'Hide Red Polyline' : 'Show Red Polyline' }}
          </button>
        </div>
      </div>
  
      <div id="map" style="height: 600px;"></div>
    </div>
  </template>
  
  <script>
  import L from "leaflet";
  import "leaflet/dist/leaflet.css";
  
  export default {
    name: "DynamicPolylineMap",
    data() {
      return {
        map: null,
        bluePolyline: null,
        redPolyline: null,
        blueCoordinates: [],
        redCoordinates: [],
        filteredBlueCoordinates: [],
        filteredRedCoordinates: [],
        updateInterval: null,
        startDateBlue: "",
        endDateBlue: "",
        startDateRed: "",
        endDateRed: "",
        blueLastPointMarker: null,
        redLastPointMarker: null,
        blueVisible: true, 
        redVisible: true, 
      };
    },
    mounted() {
      this.initializeMap();
      this.fetchCoordinates();
      this.startAddingPoints();
    },
    beforeDestroy() {
      clearInterval(this.updateInterval);   
    },
    methods: {
      initializeMap() {
        this.map = L.map("map").setView([43, -0.3], 5); // Initial map view
        L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
          attribution: "© OpenStreetMap contributors",
        }).addTo(this.map);
      },
      fetchCoordinates() {
        // Fetch initial coordinates from the server
        fetch("http://127.0.0.1:8000/coordinates/ws")
          .then((response) => response.json())
          .then((data) => {
            this.blueCoordinates = data.blue;
            this.redCoordinates = data.red;
            this.filteredBlueCoordinates = data.blue; // Initialize filtered coordinates
            this.filteredRedCoordinates = data.red;
            this.addPolylines();
          });
      },
      addPolylines() {
        // Add blue polyline to the map
        const blueLatLngs = this.filteredBlueCoordinates.map((point) => [
          point.lat,
          point.lng,
        ]);
        this.bluePolyline = L.polyline(blueLatLngs, { color: "blue" }).addTo(
          this.map
        );
  
        // Add red polyline to the map
        const redLatLngs = this.filteredRedCoordinates.map((point) => [
          point.lat,
          point.lng,
        ]);
        this.redPolyline = L.polyline(redLatLngs, { color: "red" }).addTo(
          this.map
        );
  
        // Add last point markers
        this.addLastPointMarker(this.blueCoordinates, "blue");
        this.addLastPointMarker(this.redCoordinates, "red");
      },
      startAddingPoints() {
        // Periodically fetch new points from the server every 5 seconds
        this.updateInterval = setInterval(() => {
          fetch("http://127.0.0.1:8000/add-coordinate")
            .then((response) => response.json())
            .then(({ blue, red }) => {
              // Add the new points to their respective coordinates array
              this.blueCoordinates.push(blue);
              this.redCoordinates.push(red);
  
              // If the new points are within the selected date range, add them to the polylines
              if (this.isPointInRange(blue, "blue")) {
                this.bluePolyline.addLatLng([blue.lat, blue.lng]);
                this.addLastPointMarker(this.blueCoordinates, "blue");
              }
              if (this.isPointInRange(red, "red")) {
                this.redPolyline.addLatLng([red.lat, red.lng]);
                this.addLastPointMarker(this.redCoordinates, "red");
              }
            });
        }, 5000);
      },
      filterPoints() {
        const startBlue = this.startDateBlue
          ? new Date(this.startDateBlue)
          : new Date(0);
        const endBlue = this.endDateBlue
          ? new Date(this.endDateBlue)
          : new Date();
        const startRed = this.startDateRed
          ? new Date(this.startDateRed)
          : new Date(0);
        const endRed = this.endDateRed ? new Date(this.endDateRed) : new Date();
  
        this.filteredBlueCoordinates = this.blueCoordinates.filter((point) => {
          const pointDate = new Date(point.time);
          return pointDate >= startBlue && pointDate <= endBlue;
        });
        this.filteredRedCoordinates = this.redCoordinates.filter((point) => {
          const pointDate = new Date(point.time);
          return pointDate >= startRed && pointDate <= endRed;
        });
  
        this.updatePolylines();
      },
      updatePolylines() {
        this.map.removeLayer(this.bluePolyline);
        this.map.removeLayer(this.redPolyline);
  
        // Add updated polylines
        this.addPolylines();
      },
      addLastPointMarker(coordinates, polylineColor) {
        if (polylineColor === "blue" && this.blueLastPointMarker) {
          this.map.removeLayer(this.blueLastPointMarker);
        } else if (polylineColor === "red" && this.redLastPointMarker) {
          this.map.removeLayer(this.redLastPointMarker);
        }
  
        const lastPoint = coordinates[coordinates.length - 1];
        if (lastPoint) {
          const iconOptions = L.icon({
            iconUrl: "/omar.jpeg", // Replace with the correct path to your icon
            iconSize: [40, 40],
          });
  
          const marker = L.marker([lastPoint.lat, lastPoint.lng], {
            icon: iconOptions,
          }).addTo(this.map);
  
          if (polylineColor === "blue") {
            this.blueLastPointMarker = marker;
          } else if (polylineColor === "red") {
            this.redLastPointMarker = marker;
          }
        }
      },
      isPointInRange(point, polylineColor) {
        const pointDate = new Date(point.time);
        const start =
          polylineColor === "blue"
            ? new Date(this.startDateBlue)
            : new Date(this.startDateRed);
        const end =
          polylineColor === "blue"
            ? new Date(this.endDateBlue)
            : new Date(this.endDateRed);
  
        return pointDate >= start && pointDate <= end;
      },
      toggleBluePolylineVisibility() {
        this.blueVisible = !this.blueVisible;
        if (this.blueVisible) {
          this.map.addLayer(this.bluePolyline);
          this.addLastPointMarker(this.blueCoordinates, "blue");
        } else {
          this.map.removeLayer(this.bluePolyline);
          if (this.blueLastPointMarker)
            this.map.removeLayer(this.blueLastPointMarker);
        }
      },
      toggleRedPolylineVisibility() {
        this.redVisible = !this.redVisible;
        if (this.redVisible) {
          this.map.addLayer(this.redPolyline);
          this.addLastPointMarker(this.redCoordinates, "red");
        } else {
          this.map.removeLayer(this.redPolyline);
          if (this.redLastPointMarker) this.map.removeLayer(this.redLastPointMarker);
        }
      },
    },
  };
  </script>
  
  <style>
  #map {
    width: 100%;
    height: 600px;
  }
  
  .red {
    background-color: red;
    padding: 5px;
  }
  
  .blue {
    background-color: blue;
    padding: 5px;
  }
  </style>
  