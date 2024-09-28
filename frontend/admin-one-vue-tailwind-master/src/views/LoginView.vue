<script setup>
import { reactive } from 'vue'
import { useRouter } from 'vue-router'
import { mdiAccount, mdiAsterisk } from '@mdi/js'
import axios from 'axios'
import SectionFullScreen from '@/components/SectionFullScreen.vue'
import CardBox from '@/components/CardBox.vue'
import FormCheckRadio from '@/components/FormCheckRadio.vue'
import FormField from '@/components/FormField.vue'
import FormControl from '@/components/FormControl.vue'
import BaseButton from '@/components/BaseButton.vue'
import BaseButtons from '@/components/BaseButtons.vue'
import LayoutGuest from '@/layouts/LayoutGuest.vue'

const form = reactive({
  login: '',
  pass: '',
  remember: true
})

const router = useRouter()

const submit = () => {
  const loginPayload = {
    username: form.login,
    password: form.pass,
  }

  axios
    .post('http://localhost:5000/login', loginPayload)
    .then((response) => {
      localStorage.setItem('token', response.data.token)
      localStorage.setItem('userId', response.data.user_id)
      localStorage.setItem('isAdmin', response.data.is_admin)
      localStorage.setItem('companyId', response.data.comp_id)
      localStorage.setItem('username', form.login)
      router.push('/dashboard')
    })
    .catch((error) => {
      alert(error.message);
  });
}

</script>
<template>
  <LayoutGuest>
    <SectionFullScreen v-slot="{ cardClass }" bg="purplePink">
      <CardBox :class="cardClass" is-form @submit.prevent="submit">
        <FormField label="Login" help="Please enter your login">
          <FormControl
            v-model="form.login"
            :icon="mdiAccount"
            name="login"
            autocomplete="username"
          />
        </FormField>

        <FormField label="Password" help="Please enter your password">
          <FormControl
            v-model="form.pass"
            :icon="mdiAsterisk"
            type="password"
            name="password"
            autocomplete="current-password"
          />
        </FormField>

        <FormCheckRadio
          v-model="form.remember"
          name="remember"
          label="Remember"
          :input-value="true"
        />

        <template #footer>
          <BaseButtons>
            <BaseButton type="submit" color="info" label="Login" />
            <BaseButton to="/" color="info" outline label="Back" />
          </BaseButtons>
          <div class="text-center mt-4">
            <p class="text-sm text-gray-600">
              Don’t have an account?
              <router-link to="/signup" class="text-info font-semibold">
                Sign up now
              </router-link>
            </p>
          </div>
        </template>
      </CardBox>
    </SectionFullScreen>
  </LayoutGuest>
</template>
