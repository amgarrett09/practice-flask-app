<template>
  <main>
    <section v-if="authenticated" class="section">
      <div class="contain is-fluid">
        <h1 class="title is-1">Create a post</h1>
        <post-form :submit="submit" />
      </div>
    </section>
    <section v-if="!authenticated" class="section">
      <div class="container is-fluid">
        <h1 class="title is-1">
          This page requires a login
        </h1>
        <p><nuxt-link to="/login">Login now</nuxt-link></p>
      </div>
    </section>
  </main>
</template>

<script>
import PostForm from '../components/PostForm.vue'
export default {
  components: {
    PostForm
  },
  async asyncData({ store, $axios }) {
    // Make sure user is authenticated before displaying anything
    const token = store.state.auth.authToken
    if (!token) {
      return {
        authenticated: false
      }
    }

    try {
      const { data } = await $axios.post('/check-auth', {
        token: token
      })

      // Refresh username with the data we get back from the api
      store.dispatch('auth/login', {
        username: data.username,
        token: token
      })

      return {
        authenticated: true
      }
    } catch (err) {
      return {
        authenticated: false
      }
    }
  },
  methods: {
    submit: function(payload) {
      return this.$axios.post('/post', payload, {
        headers: {
          'x-access-token': this.$store.state.auth.authToken
        }
      })
    }
  }
}
</script>

<style></style>
