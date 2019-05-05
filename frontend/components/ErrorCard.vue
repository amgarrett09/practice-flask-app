<template>
  <article class="message is-danger">
    <div class="message-header">
      <p>Error</p>
    </div>
    <div class="content message-body">
      <ul>
        <li v-for="error in errors" :key="error">{{ error }}</li>
      </ul>
    </div>
  </article>
</template>

<script>
export default {
  props: {
    errors: {
      type: Array,
      required: true
    }
  }
}
</script>

<style></style>
