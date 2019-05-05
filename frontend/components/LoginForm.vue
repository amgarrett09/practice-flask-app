<template>
  <form action="">
    <div class="field">
      <label for="username" class="label">
        Username
        <input id="username" v-model="username" type="text" class="input" />
      </label>
    </div>
    <div v-if="registration" class="field">
      <label for="email" class="label">
        Email address
        <input v-model="email" type="email" class="input" />
      </label>
    </div>
    <div class="field">
      <label for="password" class="label">
        Password
        <input id="password" v-model="password" type="password" class="input" />
      </label>
    </div>
    <div v-if="registration" class="field">
      <label for="confirm-password" class="label">
        Confirm password
        <input v-model="confirmPassword" type="password" class="input" />
      </label>
    </div>
    <button class="button is-link" type="submit" @click.prevent="handleClick">
      Submit
    </button>
  </form>
</template>

<script>
export default {
  props: {
    registration: {
      type: Boolean,
      required: false,
      default: false
    }
  },
  data() {
    return {
      username: '',
      password: '',
      confirmPassword: '',
      email: '',
      errors: []
    }
  },
  methods: {
    handleClick() {
      const [validated, errors] = this.validate()

      if (!validated) {
        this.errors = errors
        this.$emit('error', this.errors)
        return
      }

      let data
      if (this.registration) {
        data = {
          username: this.username,
          password: this.password,
          email: this.email
        }
      } else {
        data = {
          username: this.username,
          password: this.password
        }
      }

      this.$emit('submit', data)
    },
    validate() {
      const errors = []

      if (this.registration) {
        if (
          this.email.length < 5 ||
          !this.email.includes('@') ||
          !this.email.includes('.')
        ) {
          errors.push('Must enter a valid email address')
        }

        if (this.password !== this.confirmPassword) {
          errors.push('Password fields do not match')
        }
      }

      if (this.username.length <= 0) {
        errors.push('Username is required')
      }

      if (this.password.length < 12) {
        errors.push('Password must be at least 12 characters')
      }

      const validated = errors.length === 0

      return [validated, errors]
    }
  }
}
</script>

<style></style>
