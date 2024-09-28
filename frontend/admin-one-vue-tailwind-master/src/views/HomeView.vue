<script setup>
import { computed, ref, onMounted, onBeforeMount } from 'vue'
import { useMainStore } from '@/stores/main'
import {
  mdiAccountMultiple,
  mdiCartOutline,
  mdiChartTimelineVariant,
  mdiMonitorCellphone,
  mdiReload,
  mdiGithub,
  mdiChartPie
} from '@mdi/js'
import * as chartConfig from '@/components/Charts/chart.config.js'
import LineChart from '@/components/Charts/LineChart.vue'
import SectionMain from '@/components/SectionMain.vue'
import CardBoxWidget from '@/components/CardBoxWidget.vue'
import CardBox from '@/components/CardBox.vue'
import TableSampleClients from '@/components/TableSampleClients.vue'
import NotificationBar from '@/components/NotificationBar.vue'
import BaseButton from '@/components/BaseButton.vue'
import CardBoxTransaction from '@/components/CardBoxTransaction.vue'
import CardBoxClient from '@/components/CardBoxClient.vue'
import LayoutAuthenticated from '@/layouts/LayoutAuthenticated.vue'
import SectionTitleLineWithButton from '@/components/SectionTitleLineWithButton.vue'
import SectionBannerStarOnGitHub from '@/components/SectionBannerStarOnGitHub.vue'

const chartData = ref(null)

const fillChartData = () => {
  chartData.value = chartConfig.sampleChartData()
}

onMounted(() => {
  fillChartData()
})

const mainStore = useMainStore()

onBeforeMount(() => {
  mainStore.fetchSampleClients()
  mainStore.fetchSampleHistory()
  mainStore.getClients()
  if (localStorage.isAdmin == 'true')
    mainStore.getAdminOverview()
  else
    mainStore.getUserInfo()
  mainStore.calculateSalesRevenue()
})

const clientBarItems = computed(() => mainStore.clients.slice(0, 4))
const transactionBarItems = computed(() => mainStore.history)
const numberOfClients = computed(() => mainStore._clients.length)
const numberOfSales = computed(() => mainStore.sales.length)
const totalRevenue = computed(() => mainStore.totalRevenue)

function sale_value(price, quantity){
  return price * quantity
}
</script>

<template>
  <LayoutAuthenticated>
    <SectionMain>
      <SectionTitleLineWithButton :icon="mdiChartTimelineVariant" title="Overview" main>

      </SectionTitleLineWithButton>

      <div class="grid grid-cols-1 gap-6 lg:grid-cols-3 mb-6">
        <CardBoxWidget
          trend="12%"
          trend-type="up"
          color="text-emerald-500"
          :icon="mdiAccountMultiple"
          :number="numberOfClients"
          label="Clients"
        />
        <CardBoxWidget
          trend="12%"
          trend-type="down"
          color="text-blue-500"
          :icon="mdiCartOutline"
          :number="numberOfSales"
          label="Sales"
        />
        <CardBoxWidget
          trend="Overflow"
          trend-type="alert"
          color="text-red-500"
          :icon="mdiChartTimelineVariant"
          :number="totalRevenue"
          prefix="$"
          label="Performance"
        />
      </div>

      <SectionTitleLineWithButton :icon="mdiChartPie" title="Last sales">
        <BaseButton :icon="mdiReload" color="whiteDark" @click="fillChartData" />
      </SectionTitleLineWithButton>

      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        <div class="flex flex-col justify-between">
          <CardBoxTransaction
            v-for="(sales, index) in mainStore.last3Sales"
            :key="index"
            :amount="sale_value(sales.SellingPrice, sales.Quantity)"
            :product="sales.ProductName"
            :quantity="sales.Quantity"
            :name="sales.Username"
            :account="sales.account"
          />
        </div>
        <div class="flex flex-col justify-between">
          <CardBoxClient
            v-for="sales in mainStore.last3Sales"
            :key="sales.SaleID"
            :name="sales.FirstName"
            :login="sales.UserName" 
            :date="sales.SaleDate"
            :progress=50
          />
        </div>
      </div>
    </SectionMain>
  </LayoutAuthenticated>
</template>
