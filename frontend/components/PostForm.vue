<template>
  <div>
    <article v-show="errors.length > 0" class="message is-danger">
      <div class="message-header">
        <p>Error</p>
      </div>
      <div class="content message-body">
        <p>The following errors must be corrected:</p>
        <ul>
          <li v-for="error in errors" :key="error">{{ error }}</li>
        </ul>
      </div>
    </article>
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
  </div>
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
      body: '',
      errors: []
    }
  },
  methods: {
    async handleSubmit() {
      /* Reset the errors when the user submits */
      this.errors = []

      if (!this.isValid()) {
        return
      }

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
    },
    isValid() {
      let validated = true

      /* Push error messages if fields aren't valid, so they can be displayed to the user */
      if (this.title.length <= 0) {
        this.errors.push('Title is required')
        validated = false
      }

      if (this.author.length <= 0) {
        this.errors.push('Author is required')
        validated = false
      }

      if (this.body.length <= 0) {
        this.errors.push('Body is required')
        validated = false
      }

      return validated
    }
  }
}
</script>

<style></style>
