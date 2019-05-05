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
    <form action="">
      <div class="field">
        <label for="username" class="label">
          Username
          <div class="control">
            <input id="username" v-model="username" type="text" class="input" />
          </div>
        </label>
      </div>
      <div class="field">
        <label for="password" class="label">
          Password
          <input
            id="password"
            v-model="password"
            type="password"
            class="input"
          />
        </label>
      </div>
      <button class="button is-link" type="submit" @click.prevent="handleClick">
        Submit
      </button>
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
      username: '',
      password: '',
      errors: []
    }
  },
  methods: {
    async handleClick() {
      const [validated, errors] = this.validate()

      if (!validated) {
        this.errors = errors
        return
      }

      try {
        const { data } = await this.submit({
          username: this.username,
          password: this.password
        })

        this.$store.dispatch('auth/login', data)
        this.$router.push('/')
      } catch (err) {
        this.errors = [err.message]
      }
    },
    validate() {
      let validated = true
      const errors = []

      if (this.username.length <= 0) {
        validated = false
        errors.push('Username is required')
      }

      if (this.password.length <= 12) {
        validated = false
        errors.push('Password must be at least 12 characters')
      }

      return [validated, errors]
    }
  }
}
</script>

<style></style>
