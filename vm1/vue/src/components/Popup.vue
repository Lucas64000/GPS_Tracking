<template>
    <div class="popup">
      <div class="popup-content">
        <div v-if="currentStep === 1" class="popup-step">
          <img src="lucas.png" alt="First" class="popup-image" />
          <p>OuinOuin z'ai perdu mes popas. Ils sont portis acheter du lait ils sont pos revenus. OuinOuin z'ai peur aled madame !</p>
        </div>
        <div v-if="currentStep === 2" class="popup-step">
          <img src="jeremi.JPG" alt="Second" class="popup-image" style="height: 100px;"/>
          <p>Ne t'en fais pas mon petit, tata vas hacker tes papa pour les tracer. On va retrouver tes paternels</p>
        </div>
        <button v-if="currentStep === 2" class="close-button" @click="closePopup">Commencer la traque</button>
          </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        currentStep: 1, // Track the current step in the popup
      };
    },
    mounted() {
      setTimeout(() => {
        this.currentStep = 2; // Switch to the second image after 2 seconds
      }, 8000);
    },
    methods: {
      closePopup() {
        this.$emit('closePopup'); // Emit an event to close the popup
      },
    },
  };
  </script>
  
  <style scoped>
  .popup {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background: rgba(0, 0, 0, 0.8);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
  }
  
  .popup-content {
    background: #fff;
    border-radius: 10px;
    padding: 20px;
    width: 90%;
    max-width: 500px;
    text-align: center;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
  }
  
  .popup-step {
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  
  .popup-image {
    max-width: 100%;
    height: auto;
    border-radius: 10px;
    margin-bottom: 10px;
  }
  
  .close-button {
    margin-top: 20px;
    padding: 10px 20px;
    background: #e74c3c;
    color: #fff;
    border: none;
    border-radius: 5px;
    font-size: 1em;
    cursor: pointer;
    transition: background 0.3s;
  }
  
  .close-button:hover {
    background: #c0392b;
  }
  </style>
  