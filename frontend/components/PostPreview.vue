<template>
  <article class="post-preview">
    <h2 class="title is-2">{{ title }}</h2>
    <p>{{ date }}</p>
    <br />
    <p>by {{ author }}</p>
    <br />
    <div class="post-body">
      {{ body }}
    </div>
  </article>
</template>

<script>
export default {
  props: {
    title: {
      type: String,
      required: true
    },
    date: {
      type: String,
      required: true
    },
    body: {
      type: String,
      required: true
    },
    author: {
      type: String,
      required: true
    }
  }
}
</script>

<style scoped>
.post-preview {
  margin-bottom: 30px;
}
</style>
