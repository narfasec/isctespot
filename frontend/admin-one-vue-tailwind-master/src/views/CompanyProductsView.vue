<script setup>
import { onBeforeMount, ref } from 'vue'
import { useRouter } from 'vue-router'
import { mdiMonitorCellphone, mdiTableBorder, mdiTableOff, mdiGithub, mdiPlus } from '@mdi/js'
import { useMainStore } from '@/stores/main'
import SectionMain from '@/components/SectionMain.vue'
import NotificationBar from '@/components/NotificationBar.vue'
import TableProducts from '@/components/TableProducts.vue'
import CardBox from '@/components/CardBox.vue'
import LayoutAuthenticated from '@/layouts/LayoutAuthenticated.vue'
import SectionTitleLineWithButton from '@/components/SectionTitleLineWithButton.vue'
import BaseButton from '@/components/BaseButton.vue'
import CardBoxNewClient from '@/components/CardBoxNewClient.vue'

const mainStore = useMainStore()

onBeforeMount(() => {
  mainStore.getCompanyProducts()
  console.log('Listing products')
})
const uploadProducts = () => {
  // router.push('/company/employees/new')
  console.log('uploading products')
}
const router = useRouter()
const isModalActive = ref(false)

</script>

<template>
  <LayoutAuthenticated>
    
    <SectionMain>
      <SectionTitleLineWithButton :icon="mdiTableBorder" title="Products" main>
        <BaseButton
          target="_blank"
          :icon="mdiPlus"
          label="Upload products"
          color="success"
          rounded-full
          small
          @click="uploadProducts"
        />
      </SectionTitleLineWithButton>

      <CardBox class="mb-6" has-table>
        <TableProducts/>
      </CardBox>
    </SectionMain>
  </LayoutAuthenticated>
</template>
