<script setup>
import { computed, ref } from 'vue'
import { useMainStore } from '@/stores/main'
import { mdiEye, mdiTrashCan } from '@mdi/js'
import CardBoxModal from '@/components/CardBoxModal.vue'
import TableCheckboxCell from '@/components/TableCheckboxCell.vue'
import BaseLevel from '@/components/BaseLevel.vue'
import BaseButtons from '@/components/BaseButtons.vue'
import BaseButton from '@/components/BaseButton.vue'
import UserAvatar from '@/components/UserAvatar.vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

defineProps({
  checkable: Boolean
})

const mainStore = useMainStore()
const router = useRouter()
const items = computed(() => mainStore.sales)

const isModalActive = ref(false)

const isModalDangerActive = ref(false)

const selectedClientId = ref()

const perPage = ref(5)

const currentPage = ref(0)

const checkedRows = ref([])

// const itemsPaginated = computed(() =>
//   items.slice(perPage.value * currentPage.value, perPage.value * (currentPage.value + 1))
// )

// const numPages = computed(() => Math.ceil(items..length / perPage.value))

// const currentPageHuman = computed(() => currentPage.value + 1)

// const pagesList = computed(() => {
//   const pagesList = []

//   for (let i = 0; i < numPages.value; i++) {
//     pagesList.push(i)
//   }

//   return pagesList
// })

const remove = (arr, cb) => {
  const newArr = []

  arr.forEach((item) => {
    if (!cb(item)) {
      newArr.push(item)
    }
  })

  return newArr
}

const checked = (isChecked, client) => {
  if (isChecked) {
    checkedRows.value.push(client)
  } else {
    checkedRows.value = remove(checkedRows.value, (row) => row.id === client.id)
  }
}

// Function to handle the delete action
const deleteClient = async (client) => {

  const deleteClientPayload = {
    client_id: client['ClientID'],
    token: localStorage.getItem('token'),
    user_id: localStorage.getItem('userId'),

  }
  try {
    await axios.post(`http://localhost:5000/clients/delete`, deleteClientPayload)
    // Assuming you refetch the client list after deletion
    mainStore.fetchClients()
    isModalDangerActive.value = false
    router.push('/clients')
  } catch (error) {
    alert(`Error: ${error.message}`)
  }
}

</script>

<template>
  <CardBoxModal v-model="isModalActive" title="Sample modal">
    <p>Lorem ipsum dolor sit amet <b>adipiscing elit</b></p>
    <p>This is sample modal</p>
  </CardBoxModal>

  <CardBoxModal v-model="isModalDangerActive" title="Please confirm" button="danger" has-cancel>
    <p>Are you sure you want to permanently delete client <b>User ID: {{ selectedClientId }}</b></p>
    <p>This is sample modal</p>
  </CardBoxModal>

  <table>
    <thead>
      <tr>
        <th v-if="checkable" />
        <th>Product Name</th>
        <th>Seller</th>
        <th>Client</th>
        <th>Quantity</th>
        <th>Price</th>
        <th>Sale date</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="client in items" :key="client['SaleID']">
        <TableCheckboxCell v-if="checkable" @checked="checked($event, client)"/>
        <td data-label="Product Name">
          {{ client['ProductName'] }} 
        </td>
        <td data-label="Seller">
          {{ client['Username'] }}
        </td>
        <td data-label="Client">
          {{ client['FirstName'] }}
        </td>
        <td data-label="Quantity">
          {{ client['Quantity'] }}
        </td>
        <td data-label="Price $"> 
          {{ client['SellingPrice'] }}
        </td>
        <td data-label="Sale Date">
          {{ client['SaleDate'] }}
        </td>
      </tr>
    </tbody>
  </table>
  <div class="p-3 lg:px-6 border-t border-gray-100 dark:border-slate-800">
    <BaseLevel>
      <BaseButtons>
        <BaseButton
          v-for="page in pagesList"
          :key="page"
          :active="page === currentPage"
          :label="page + 1"
          :color="page === currentPage ? 'lightDark' : 'whiteDark'"
          small
          @click="currentPage = page"
        />
      </BaseButtons>
      <small>Page {{ currentPageHuman }} of {{ numPages }}</small>
    </BaseLevel>
  </div>
</template>
