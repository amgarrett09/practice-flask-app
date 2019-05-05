<template>
  <div>
    <article v-show="errors.length > 0" class="message is-danger">
      <div class="message-header">
        <p>Error</p>
      </div>
      <div class="content message-body">
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
      const [inputIsValid, errors] = this.validate()

      if (!inputIsValid) {
        this.errors = errors
        return
      }

      try {
        // Pass data to the submit function that as provided in props
        const { data } = await this.submit({
          title: this.title,
          author: this.author,
          body: this.body
        })

        if (data.statusCode === 201) {
          this.$router.push('/')
        }
      } catch (err) {
        if (err.message === 'Request failed with status code 409') {
          this.errors = [
            'There is already a post with that title. Title must be unique.'
          ]
        } else {
          this.errors = ['There was a network error. Please try again.']
        }
      }
    },
    // Returns a pair of a boolean and an array of errors
    validate() {
      let validated = true
      const errors = []

      if (this.title.length <= 0) {
        errors.push('Title is required')
        validated = false
      }

      if (this.author.length <= 0) {
        errors.push('Author is required')
        validated = false
      }

      if (this.body.length <= 0) {
        errors.push('Body is required')
        validated = false
      }

      return [validated, errors]
    }
  }
}
</script>

<style></style>
