<script setup>
import { onBeforeMount, ref } from 'vue'
import { useRouter } from 'vue-router'
import { mdiMonitorCellphone, mdiTableBorder, mdiTableOff, mdiGithub, mdiPlus } from '@mdi/js'
import { useMainStore } from '@/stores/main'
import SectionMain from '@/components/SectionMain.vue'
import NotificationBar from '@/components/NotificationBar.vue'
import TableSales from '@/components/TableSales.vue'
import CardBox from '@/components/CardBox.vue'
import LayoutAuthenticated from '@/layouts/LayoutAuthenticated.vue'
import SectionTitleLineWithButton from '@/components/SectionTitleLineWithButton.vue'
import BaseButton from '@/components/BaseButton.vue'
import CardBoxNewClient from '@/components/CardBoxNewClient.vue'

const mainStore = useMainStore()

onBeforeMount(() => {
  if(localStorage.getItem('isAdmin') == 'true'){
    mainStore.getAdminOverview()
  }else{
    mainStore.getUserInfo()
  }
})
const newSale = () => {
  router.push('/sales/new')
}
const router = useRouter()
const isModalActive = ref(false)

</script>

<template>
  <LayoutAuthenticated>
    
    <SectionMain>
      <SectionTitleLineWithButton :icon="mdiTableBorder" title="Sales" main>
        <BaseButton
          target="_blank"
          :icon="mdiPlus"
          label="New sale"
          color="success"
          rounded-full
          small
          @click="newSale"
        />
      </SectionTitleLineWithButton>

      <CardBox class="mb-6" has-table>
        <TableSales />
      </CardBox>
    </SectionMain>
  </LayoutAuthenticated>
</template>
