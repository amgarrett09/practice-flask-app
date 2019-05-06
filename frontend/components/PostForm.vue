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
  data() {
    return {
      title: '',
      body: '',
      errors: []
    }
  },
  methods: {
    handleSubmit() {
      const [inputIsValid, errors] = this.validate()

      if (!inputIsValid) {
        this.errors = errors
        this.$emit('error', this.errors)
        return
      }

      const data = {
        title: this.title,
        body: this.body,
        author: this.$store.state.auth.loggedInUser
      }

      this.$emit('submit', data)
    },
    // Returns a pair of a boolean and an array of errors
    validate() {
      let validated = true
      const errors = []

      if (this.title.length <= 0) {
        errors.push('Title is required')
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
