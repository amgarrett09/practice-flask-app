<template>
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
</template>

<script>
import PostPreview from '../components/PostPreview.vue'
export default {
  components: {
    PostPreview
  },
  async asyncData({ $axios, error }) {
    try {
      const { data } = await $axios.get('/post')

      return {
        posts: data.posts
      }
    } catch (err) {
      error({
        statusCode: 503,
        message: err.message
      })
    }
  }
}
</script>

<style scoped></style>
