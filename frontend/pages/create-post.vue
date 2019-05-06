<template>
  <main>
    <section v-if="authenticated" class="section">
      <div class="container is-fluid">
        <h1 class="title is-1">Create a post</h1>
        <error-card v-show="errors.length > 0" :errors="errors" />
        <post-form :submit="submit" @submit="onSubmit" @error="onError" />
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
import ErrorCard from '../components/ErrorCard.vue'
export default {
  components: {
    PostForm,
    ErrorCard
  },
  data() {
    return {
      errors: []
    }
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
    async onSubmit(payload) {
      try {
        await this.$axios.post('/post', payload, {
          headers: {
            'x-access-token': this.$store.state.auth.authToken
          }
        })

        this.$router.push('/')
      } catch (err) {
        if (err.message.includes('409')) {
          this.errors = ['A post with that title already exists']
        } else if (err.message.includes('401')) {
          this.errors = ['Login required']
        } else {
          this.errors = ['There was a network error. Try again.']
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
