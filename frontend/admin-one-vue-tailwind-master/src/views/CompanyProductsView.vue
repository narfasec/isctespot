<script setup>
import { ref, onBeforeMount } from 'vue'
import { useRouter } from 'vue-router'
import { mdiTableBorder, mdiPlus } from '@mdi/js'
import { useMainStore } from '@/stores/main'
import SectionMain from '@/components/SectionMain.vue'
import TableProducts from '@/components/TableProducts.vue'
import CardBox from '@/components/CardBox.vue'
import LayoutAuthenticated from '@/layouts/LayoutAuthenticated.vue'
import SectionTitleLineWithButton from '@/components/SectionTitleLineWithButton.vue'
import BaseButton from '@/components/BaseButton.vue'

const mainStore = useMainStore()
const router = useRouter()
const isModalActive = ref(false)
const fileInput = ref(null) // Reference to the file input element

onBeforeMount(() => {
  mainStore.getCompanyProducts()
  console.log('Listing products')
})

// Trigger file input to select a file
const uploadProducts = () => {
  fileInput.value.click()
} 

// Handle file selection and upload
const handleFileChange = async (event) => {
  const file = event.target.files[0]
  if (!file) return

  console.log('Selected file:', file)

  // Create FormData object for the payload
  const formData = new FormData()
  formData.append('file', file)
  formData.append('comp_id', localStorage.getItem('companyId')) // Your company ID
  formData.append('token', localStorage.getItem('token')) // Replace with actual admin auth token

  try {
    const response = await fetch('http://localhost:5000/update_products', {
      method: 'POST',
      body: formData,
    })

    // Parse JSON response
    const data = await response.json()

    if (data.status === 'Ok') {
      console.log('Products update success')
      alert('Products updated successfully!')
    } else {
      console.error('Products update failed')
      alert('Failed to update products.')
    }
  } catch (error) {
    console.error('Error uploading file:', error)
    alert('Error uploading file.')
  }
}

// const submit = () => {
//   if(form.pass != form.confirmPassword){
//     alert("Passwords don't match")
//     return;
//   }

//   const signupPayload = {
//     username: form.username,
//     password: form.pass,
//     email: form.email,
//     comp_name: form.companyName,
//     num_employees: selectedCompanySize.value
//   }

//   axios
//     .post('http://localhost:5000/signup', signupPayload)
//     .then((response) => {
//       localStorage.setItem('token', response.data.token)
//       localStorage.setItem('userId', response.data.user_id)
//       localStorage.setItem('companyId', response.data.comp_id)
//       localStorage.setItem('isAdmin', response.data.is_admin)
//       router.push('/dashboard')
//     })
//     .catch((error) => {
//       alert(error.message);
//   });
// }
</script>

<template>
  <LayoutAuthenticated>
    <SectionMain>
      <SectionTitleLineWithButton :icon="mdiTableBorder" title="Products" main>
        <BaseButton
          :icon="mdiPlus"
          label="Upload products"
          color="success"
          rounded-full
          small
          @click="uploadProducts"
        />
        <!-- Hidden file input for selecting a file -->
        <input
          type="file"
          ref="fileInput"
          @change="handleFileChange"
          style="display: none"
        />
      </SectionTitleLineWithButton>

      <CardBox class="mb-6" has-table>
        <TableProducts />
      </CardBox>
    </SectionMain>
  </LayoutAuthenticated>
</template>
