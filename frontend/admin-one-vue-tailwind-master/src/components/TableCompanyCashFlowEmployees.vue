<script setup>
import { computed, ref } from 'vue'
import { useMainStore } from '@/stores/main'
import { mdiEye, mdiTrashCan } from '@mdi/js'
import CardBoxModalDeleteEmployee from '@/components/CardBoxModalDeleteEmployee.vue'
import CardBoxModal from '@/components/CardBoxModal.vue'
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
const items = computed(() => mainStore.cashFlow['employees'])

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

</script>

<template>
  <CardBoxModal v-model="isModalActive" title="Sample modal">
    <p>Lorem ipsum dolor sit amet <b>adipiscing elit</b></p>
    <p>This is sample modal</p>
  </CardBoxModal>

  <CardBoxModalDeleteEmployee v-model="isModalDangerActive" title="Please confirm" button="danger" has-cancel :item="selectedEmployeeId">
    <p>Are you sure you want to permanently delete employee <b>User ID: {{ selectedEmployeeId }}</b></p>
    <p>This is sample modal</p>
  </CardBoxModalDeleteEmployee>

  <table>
    <thead>
      <tr>
        <th v-if="checkable" />
        <th>Username</th>
        <th>Total Sales</th>
        <th>Total Comission</th>
        <th>Commission %</th>
        <th />
      </tr>
    </thead>
    <tbody>
      <tr v-for="employee in items" :key="employee['UserID']">
        <TableCheckboxCell v-if="checkable" @checked="checked($event, employee)"/>
        <td data-label="Name">
          {{ employee['Username'] }}
        </td>
        <td data-label="Total Sales">
          {{ employee['TotalSales'] }}
        </td>
        <td data-label="Total Commission">
          {{ employee['TotalCommission'] }}$
        </td>
        <td data-label="Commission Percentage">
          {{ employee['CommissionPercentage'] }}
        </td>
        <td class="before:hidden lg:w-1 whitespace-nowrap">
          <BaseButtons type="justify-start lg:justify-end" no-wrap>
            <BaseButton color="info" :icon="mdiEye" small @click="isModalActive = true" />
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
