<template>
  <div>
    <header>
      <nav-bar />
    </header>
    <main>
      <section class="section">
        <div class="container is-fluid">
          <post-preview
            v-for="post in posts"
            :key="post.title"
            :title="post.title"
            :author="post.author"
            :date="post.date"
            :body="post.body"
          />
        </div>
      </section>
    </main>
  </div>
</template>

<script>
import PostPreview from '../components/PostPreview.vue'
import NavBar from '../components/NavBar.vue'
export default {
  components: {
    PostPreview,
    NavBar
  },
  async asyncData({ $axios, error }) {
    try {
      const { data } = await $axios.get('/post')

      return {
        posts: data.posts,
        errors: []
      }
    } catch (err) {
      return {
        posts: [],
        errors: ['There was a problem fetching posts. Try again.']
      }
    }
  }
}
</script>

<style scoped></style>
