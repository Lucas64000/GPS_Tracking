<template>
    <div>
      <h1>Send Message to FastAPI</h1>
      <input v-model="message" placeholder="Enter your message" />
      <button @click="sendMessage">Send</button>
      <p>{{ response }}</p>
    </div>
  </template>
  
  <script>
  import axios from 'axios'
  
  export default {
    data() {
      return {
        message: '',
        response: ''
      }
    },
    methods: {
      async sendMessage() {
        try {
          const res = await axios.post('http://localhost:8000/send', { message: this.message })
          this.response = res.data.status
        } catch (error) {
          this.response = 'Error sending message'
        }
      }
    }
  }
  </script>
  
  <style scoped>
  h1 {
    font-size: 2em;
    margin-bottom: 20px;
  }
  input {
    padding: 10px;
    font-size: 1em;
    margin-right: 10px;
  }
  button {
    padding: 10px;
    font-size: 1em;
  }
  p {
    margin-top: 20px;
    font-size: 1.2em;
  }
  </style>