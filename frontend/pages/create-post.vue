<template>
  <main>
    <section class="section">
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
  methods: {
    submit: function(payload) {
      return this.$axios.post('/post', payload)
    }
  }
}
</script>

<style></style>
