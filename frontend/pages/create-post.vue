<template>
  <main>
    <section v-if="authenticated" class="section">
      <div class="contain is-fluid">
        <h1 class="title is-1">Create a post</h1>
        <post-form :submit="submit" />
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
      await $axios.post('/check-auth', {
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
