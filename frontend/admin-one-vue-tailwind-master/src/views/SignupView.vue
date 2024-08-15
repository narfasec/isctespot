<script setup>
import { reactive, computed } from 'vue'
import { useRouter } from 'vue-router'
import { mdiAccount, mdiAsterisk, mdiEmail, mdiOfficeBuilding } from '@mdi/js'
import axios from 'axios'
import SectionFullScreen from '@/components/SectionFullScreen.vue'
import CardBox from '@/components/CardBox.vue'
import FormCheckRadioGroup from '@/components/FormCheckRadioGroup.vue'
import FormField from '@/components/FormField.vue'
import FormControl from '@/components/FormControl.vue'
import BaseButton from '@/components/BaseButton.vue'
import BaseButtons from '@/components/BaseButtons.vue'
import LayoutGuest from '@/layouts/LayoutGuest.vue'

const form = reactive({
  username: '',
  pass: '',
  confirmPassword: '',
  email: '',
  companyName:'',
  companySize: ''
})

const companySizeOptions = {
  one: '1-10',
  two: '10-50',
  three: '50-100',
  four: '+100'
}
const selectedCompanySize = computed(() => companySizeOptions[form.companySize])
const router = useRouter()

const submit = () => {
  if(form.pass != form.confirmPassword){
    alert("Passwords don't match")
    return;
  }

  const signupPayload = {
    username: form.username,
    password: form.pass,
    email: form.email,
    comp_name: form.companyName,
    num_employees: selectedCompanySize.value
  }

  axios
    .post('http://localhost:5000/signup', signupPayload)
    .then((response) => {
      localStorage.setItem('token', response.data.token)
      localStorage.setItem('userId', response.data.user_id)
      localStorage.setItem('companyId', response.data.comp_id)
      localStorage.setItem('isAdmin', response.data.is_admin)
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
        <FormField label="Email" help="Please enter your email">
          <FormControl
            v-model="form.email"
            :icon="mdiEmail"
            name="email"
          />
        </FormField>

        <FormField label="Company Name" help="Please enter your company name">
          <FormControl
            v-model="form.companyName"
            :icon="mdiOfficeBuilding"
            name="company name"
          />
        </FormField>

        <FormField label="Username" help="Please enter your username">
          <FormControl
            v-model="form.username"
            :icon="mdiAccount"
            name="username"
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
        <FormField label="Confirm Password" help="Please enter your password">
          <FormControl
            v-model="form.confirmPassword"
            :icon="mdiAsterisk"
            type="password"
            name="password"
            autocomplete="current-password"
          />
        </FormField>

        <FormField label="Company Size" help="Number of employees">
          <FormCheckRadioGroup
            v-model="form.companySize"
            name="sample-radio"
            type="radio"
            :options="companySizeOptions"
          />
        </FormField>

        <template #footer>
          <BaseButtons>
            <BaseButton type="submit" color="info" label="Signup" />
            <BaseButton to="/" color="info" outline label="Back" />
          </BaseButtons>
          <div class="text-center mt-4">
            <p class="text-sm text-gray-600">
              Already have an account?
              <router-link to="/login" class="text-info font-semibold">
                Login now
              </router-link>
            </p>
          </div>
        </template>
      </CardBox>
    </SectionFullScreen>
  </LayoutGuest>
</template>
