<template>
  <nav>
    <template v-if="loggedInUser">
      <nuxt-link to="/create-post">
        Create a post
      </nuxt-link>
    </template>
    <template v-if="!loggedInUser">
      <nuxt-link to="/login">Login</nuxt-link>
      |
      <nuxt-link to="/register">Register</nuxt-link>
    </template>
  </nav>
</template>

<script>
import { mapState } from 'vuex'
export default {
  computed: {
    ...mapState('auth', ['loggedInUser'])
  }
}
</script>

<style></style>
