<template>
  <main>
    <section class="section">
      <error-card v-show="errors.length > 0" :errors="errors" />
      <div class="container is-fluid">
        <login-form :registration="true" @error="onError" @submit="onSubmit" />
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
    async onSubmit(data) {
      try {
        await this.$axios.post('/register', data)
        this.$router.push('/login')
      } catch (err) {
        if (err.message === 'Request failed with status code 409') {
          this.errors = ['A user with that username or email already exists']
        } else {
          this.errors = ['There was a network problem. Try again.']
        }
      }
    },
    onError(errors) {
      this.errors = errors
    }
  }
}
</script>

<style></style>
