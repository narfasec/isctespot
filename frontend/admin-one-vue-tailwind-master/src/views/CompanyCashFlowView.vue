<script setup>
import { onBeforeMount, ref } from 'vue'
import { useRouter } from 'vue-router'
import { mdiMonitorCellphone, mdiTableBorder, mdiTableOff, mdiGithub, mdiPlus } from '@mdi/js'
import { useMainStore } from '@/stores/main'
import SectionMain from '@/components/SectionMain.vue'
import NotificationBar from '@/components/NotificationBar.vue'
import TableEmployees from '@/components/TableEmployees.vue'
import CardBox from '@/components/CardBox.vue'
import LayoutAuthenticated from '@/layouts/LayoutAuthenticated.vue'
import SectionTitleLineWithButton from '@/components/SectionTitleLineWithButton.vue'
import BaseButton from '@/components/BaseButton.vue'
import CardBoxNewClient from '@/components/CardBoxNewClient.vue'

const mainStore = useMainStore()

onBeforeMount(() => {
  mainStore.getCompanyEmployees()
})
const newEmployee = () => {
  router.push('/company/employees/new')
}
const router = useRouter()
const isModalActive = ref(false)

</script>

<template>
  <LayoutAuthenticated>
    
    <SectionMain>
      <SectionTitleLineWithButton :icon="mdiTableBorder" title="Employees" main>
        <BaseButton
          target="_blank"
          :icon="mdiPlus"
          label="New Employee"
          color="success"
          rounded-full
          small
          @click="newEmployee"
        />
      </SectionTitleLineWithButton>

      <CardBox class="mb-6" has-table>
        <TableEmployees/>
      </CardBox>
    </SectionMain>
  </LayoutAuthenticated>
</template>
