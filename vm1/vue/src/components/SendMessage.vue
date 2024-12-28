<template>
  <div>
    <h1>Send Message to FastAPI</h1>
    <input v-model="message" placeholder="Enter your message" />
    <button @click="fetchKafkaMessages">Send</button>
    <p>{{ response }}</p>

    <h2>Messages from Kafka:</h2>
    <ul>
      <li v-for="(msg, index) in kafkaMessages" :key="index">{{ msg }}</li>
    </ul>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      message: '',
      response: '',
      kafkaMessages: []  // Ajout de cette variable pour stocker les messages de Kafka
    }
  },
  methods: {
    async sendMessage() {
      try {
        const res = await axios.post('http://0.0.0.0:8000/send', { message: this.message });
        this.response = res.data.status
      } catch (error) {
        this.response = 'Error sending message'
      }
    },
    async fetchKafkaMessages() {
      try {
        const res = await axios.get('http://0.0.0.0:8000/messages');  // Requête GET pour obtenir les messages Kafka
        this.kafkaMessages = res.data.messages  // Met à jour le tableau kafkaMessages avec les messages reçus
      } catch (error) {
        console.error('Error fetching Kafka messages:', error)
      }
    }
  },
  mounted() {
    this.fetchKafkaMessages();  // Appeler la fonction fetchKafkaMessages lorsqu'on charge le composant
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
h2 {
  margin-top: 30px;
  font-size: 1.5em;
}
ul {
  margin-top: 10px;
  list-style-type: none;
  padding-left: 0;
}
li {
  padding: 5px 0;
}
</style>
