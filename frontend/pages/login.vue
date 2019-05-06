<template>
  <main>
    <section class="section">
      <div class="container is-fluid">
        <error-card v-show="errors.length > 0" :errors="errors" />
        <login-form @error="onError" @submit="onSubmit" />
      </div>
    </section>
  </main>
</template>

<script>
import LoginForm from '../components/LoginForm.vue'
import ErrorCard from '../components/ErrorCard.vue'
export default {
  components: {
    LoginForm,
    ErrorCard
  },
  data() {
    return {
      errors: []
    }
  },
  methods: {
    async onSubmit(payload) {
      try {
        const { data } = await this.$axios.post('/login', payload)
        this.$store.dispatch('auth/login', data)
        this.$router.push('/')
      } catch (err) {
        this.errors = ['There was a network error. Try again.']
      }
    },
    onError(errors) {
      this.errors = errors
    }
  }
}
</script>

<style></style>
