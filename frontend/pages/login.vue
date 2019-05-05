<template>
  <main>
    <section class="section">
      <div class="container is-fluid">
        <login-form :submit="submit" />
      </div>
    </section>
  </main>
</template>

<script>
import LoginForm from '../components/LoginForm.vue'
export default {
  components: {
    LoginForm
  },
  methods: {
    submit(payload) {
      return this.$axios.post('/login', payload)
    }
  }
}
</script>

<style></style>
