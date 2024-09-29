<script setup>
import { computed, ref } from 'vue'
import { useMainStore } from '@/stores/main'
import { mdiPencil, mdiTrashCan } from '@mdi/js'
import CardBoxModalDeleteEmployee from '@/components/CardBoxModalDeleteEmployee.vue'
import CardBoxModalEditCommission from '@/components/CardBoxModalEditCommission.vue'
import TableCheckboxCell from '@/components/TableCheckboxCell.vue'
import BaseLevel from '@/components/BaseLevel.vue'
import BaseButtons from '@/components/BaseButtons.vue'
import BaseButton from '@/components/BaseButton.vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

defineProps({
  checkable: Boolean
})

const mainStore = useMainStore()
const router = useRouter()
const items = computed(() => mainStore._employees)
const selectedNumber = ref(5) // Default value
const numbers = [5,6,7,8,9,10,15,20,25] // Predefined options

const isModalActive = ref(false)

const isModalDangerActive = ref(false)

const selectedEmployeeId = ref()

const perPage = ref(5)

const currentPage = ref(0)

const checkedRows = ref([])

const remove = (arr, cb) => {
  const newArr = []

  arr.forEach((item) => {
    if (!cb(item)) {
      newArr.push(item)
    }
  })

  return newArr
}

const checked = (isChecked, employee) => {
  if (isChecked) {
    checkedRows.value.push(employee)
  } else {
    checkedRows.value = remove(checkedRows.value, (row) => row.id === employee.id)
  }
}

// Function to handle the delete action
const deleteEmployee = async (employee) => {

  const deleteEmployeePayload = {
    employee_id: employee['UserID'],
    token: localStorage.getItem('token'),
    user_id: localStorage.getItem('userId'),
  }

  try {
    await axios.post(`http://localhost:5000/employees/delete`, deleteEmployeePayload)
    isModalDangerActive.value = false
    router.push('/employees')
  } catch (error) {
    alert(`Error: ${error.message}`)
  }
}

</script>

<template>
  <CardBoxModalEditCommission v-model="isModalActive" title="Edit Comission" :item="selectedEmployeeId" :commission="selectedNumber">
    <form>
      <label for="numberSelect" class="block text-gray-700 text-sm font-bold mb-2">Choose a number:</label>
      <select 
        id="numberSelect" 
        v-model="selectedNumber"
        class="block w-32 p-2 border border-gray-300 rounded-md shadow-sm text-sm focus:outline-none focus:ring focus:border-blue-300"
      >
        <option v-for="number in numbers" :key="number" :value="number">
          {{ number }}%
        </option>
      </select>
      <p class="mt-2 text-sm text-gray-600">Selected percentage: {{ selectedNumber }}%</p>
    </form>
  </CardBoxModalEditCommission>

  <CardBoxModalDeleteEmployee v-model="isModalDangerActive" title="Please confirm" button="danger" has-cancel :item="selectedEmployeeId">
    <p>Are you sure you want to permanently delete employee <b>User ID: {{ selectedEmployeeId }}</b></p>
    <p>This is sample modal</p>
  </CardBoxModalDeleteEmployee>

  <table>
    <thead>
      <tr>
        <th v-if="checkable" />
        <th>Username</th>
        <th>Email</th>
        <th>Commission</th>
        <th />
      </tr>
    </thead>
    <tbody>
      <tr v-for="employee in items" :key="employee['UserID']">
        <TableCheckboxCell v-if="checkable" @checked="checked($event, employee)"/>
        <td data-label="Name">
          {{ employee['Username'] }}
        </td>
        <td data-label="Email">
          {{ employee['Email'] }}
        </td>
        <td data-label="Commission">
          {{ employee['CommissionPercentage'] }}%
        </td>
        <td class="before:hidden lg:w-1 whitespace-nowrap">
          <BaseButtons type="justify-start lg:justify-end" no-wrap>
            <BaseButton color="info" :icon="mdiPencil" small @click="() => { selectedEmployeeId = employee['UserID']; isModalActive = true }" />
            <BaseButton
              color="danger"
              :icon="mdiTrashCan"
              small
              @click="() => { selectedEmployeeId = employee['UserID']; isModalDangerActive = true }"
            />
          </BaseButtons>
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
