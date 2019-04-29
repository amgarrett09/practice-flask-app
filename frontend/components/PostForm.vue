<template>
  <form action="/">
    <div class="field">
      <label for="title" class="label">
        Title
        <div class="control">
          <input id="title" v-model="title" type="text" class="input" />
        </div>
      </label>
    </div>
    <div class="field">
      <label for="author" class="label">
        Author
        <div class="control">
          <input id="author" v-model="author" type="text" class="input" />
        </div>
      </label>
    </div>
    <div class="field">
      <label for="body" class="label">
        Body
        <div class="control">
          <textarea id="body" v-model="body" class="textarea" />
        </div>
      </label>
    </div>
    <div class="field">
      <div class="control">
        <button class="button is-link" @click.prevent="handleSubmit">
          Submit
        </button>
      </div>
    </div>
  </form>
</template>

<script>
export default {
  props: {
    submit: {
      type: Function,
      required: true
    }
  },
  data() {
    return {
      title: '',
      author: '',
      body: ''
    }
  },
  methods: {
    async handleSubmit() {
      try {
        const { data } = await this.submit({
          title: this.title,
          author: this.author,
          body: this.body
        })

        if (!data.statusCode) {
          this.$router.push('/')
        }
      } catch (err) {}
    }
  }
}
</script>

<style></style>
