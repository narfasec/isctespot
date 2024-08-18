<script setup>
import { reactive, ref } from 'vue'
import { mdiBallotOutline, mdiAccount, mdiMail, mdiGithub, mdiFlagOutline, mdiCancel, mdiCross, mdiClose } from '@mdi/js'
import SectionMain from '@/components/SectionMain.vue'
import CardBox from '@/components/CardBox.vue'
import FormCheckRadioGroup from '@/components/FormCheckRadioGroup.vue'
import FormFilePicker from '@/components/FormFilePicker.vue'
import FormField from '@/components/FormField.vue'
import FormControl from '@/components/FormControl.vue'
import BaseDivider from '@/components/BaseDivider.vue'
import BaseButton from '@/components/BaseButton.vue'
import BaseButtons from '@/components/BaseButtons.vue'
import SectionTitle from '@/components/SectionTitle.vue'
import LayoutAuthenticated from '@/layouts/LayoutAuthenticated.vue'
import SectionTitleLineWithButton from '@/components/SectionTitleLineWithButton.vue'
import NotificationBarInCard from '@/components/NotificationBarInCard.vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const router = useRouter()

const selectOptions = [
  { id: 1, label: 'Business development' },
  { id: 2, label: 'Marketing' },
  { id: 3, label: 'Sales' }
]

const form = reactive({
  firstName: 'First Name',
  lastName: 'Last Name',
  email: 'email@mail.com',
  phone: '123456789',
  address: 'address',
  city: 'city',
  country: 'country'
})

const customElementsForm = reactive({
  checkbox: ['lorem'],
  radio: 'one',
  switch: ['one'],
  file: null
})

const submit = () => {

  const newClientPayload = {
    first_name: form.firstName,
    last_name: form.lastName,
    email: form.email,
    phone_number: form.phone,
    address: form.address,
    city: form.city,
    country: form.country,
    token: localStorage.getItem('token'),
    user_id: localStorage.getItem('userId'),
    comp_id: localStorage.getItem('companyId')

  }

  axios
    .post('http://localhost:5000/clients/new', newClientPayload)
    .then((response) => {
      if (response.status >= 200 && response.status < 300) {
        alert('Client created successfully!');
        router.push('/clients');
      } else {
        alert('Failed to create client. Please try again.');
      }
    })
    .catch((error) => {
      alert(error.message);
    });
}

const formStatusWithHeader = ref(true)

const formStatusCurrent = ref(0)

const formStatusOptions = ['info', 'success', 'danger', 'warning']

const formStatusSubmit = () => {
  formStatusCurrent.value = formStatusOptions[formStatusCurrent.value + 1]
    ? formStatusCurrent.value + 1
    : 0
}

</script>

<template>
  <LayoutAuthenticated>
    <SectionMain>
      <SectionTitleLineWithButton :icon="mdiBallotOutline" title="Forms example" main>
        <BaseButton
          to="/clients"
          target="_blank"
          :icon="mdiClose"
          label=""
          color="danger"
          rounded-full
          small
        />
      </SectionTitleLineWithButton>
      <CardBox :class="cardClass" is-form @submit.prevent="submit">
        <FormField label="First name and last name" help="Please enter client's first name and last name">
          <FormControl
            v-model="form.firstName"
            :icon="mdiIdCard"
            name="first name"
            size="small"
          />
          <FormControl
            v-model="form.lastName"
            :icon="mdiIdCard"
            name="last name"
          />
        </FormField>
        <FormField label="Email and phone number" help="Please enter client's email and phone number">
          <FormControl
            v-model="form.email"
            :icon="mdiEmail"
            name="email"
          /> 
          <FormControl
            v-model="form.phone"
            :icon="mdiPhone"
            name="phone number"
          /> 
        </FormField>
        <FormField label="Location" help="Please enter client's location">
          <FormControl
            v-model="form.address"
            :icon="mdiMail"
            name="address"
          /> 
          <FormControl
            v-model="form.city"
            :icon="mdiMail"
            name="city"
          />
          <FormControl
            v-model="form.country"
            :icon="mdiFlagOutline"
            name="country"
          /> 
        </FormField>

        <template #footer>
          <BaseButtons>
            <BaseButton type="submit" color="info" label="Submit" />
            <BaseButton type="reset" color="danger" outline label="Cancel" to="/clients" />
          </BaseButtons>
        </template>
      </CardBox>
    </SectionMain>

    <SectionTitle>Custom elements</SectionTitle>

    <SectionMain>
      <CardBox>
        <FormField label="Checkbox">
          <FormCheckRadioGroup
            v-model="customElementsForm.checkbox"
            name="sample-checkbox"
            :options="{ lorem: 'Lorem', ipsum: 'Ipsum', dolore: 'Dolore' }"
          />
        </FormField>

        <BaseDivider />

        <FormField label="Radio">
          <FormCheckRadioGroup
            v-model="customElementsForm.radio"
            name="sample-radio"
            type="radio"
            :options="{ one: 'One', two: 'Two' }"
          />
        </FormField>

        <BaseDivider />

        <FormField label="Switch">
          <FormCheckRadioGroup
            v-model="customElementsForm.switch"
            name="sample-switch"
            type="switch"
            :options="{ one: 'One', two: 'Two' }"
          />
        </FormField>

        <BaseDivider />

        <FormFilePicker v-model="customElementsForm.file" label="Upload" />
      </CardBox>

      <SectionTitle>Form with status example</SectionTitle>

      <CardBox
        class="md:w-7/12 lg:w-5/12 xl:w-4/12 shadow-2xl md:mx-auto"
        is-form
        is-hoverable
        @submit.prevent="formStatusSubmit"
      >
        <NotificationBarInCard
          :color="formStatusOptions[formStatusCurrent]"
          :is-placed-with-header="formStatusWithHeader"
        >
          <span
            ><b class="capitalize">{{ formStatusOptions[formStatusCurrent] }}</b> state</span
          >
        </NotificationBarInCard>
        <FormField label="Fields">
          <FormControl
            v-model="form.name"
            :icon-left="mdiAccount"
            help="Your full name"
            placeholder="Name"
          />
        </FormField>

        <template #footer>
          <BaseButton label="Trigger" type="submit" color="info" />
        </template>
      </CardBox>
    </SectionMain>
  </LayoutAuthenticated>
</template>
