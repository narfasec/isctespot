<script setup>
import { computed, ref, onMounted, onBeforeMount } from 'vue'
import { useMainStore } from '@/stores/main'
import {
  mdiAccountMultiple,
  mdiCartOutline,
  mdiChartTimelineVariant,
  mdiChartPie
} from '@mdi/js'
import * as chartConfig from '@/components/Charts/chart.config.js'
import SectionMain from '@/components/SectionMain.vue'
import CardBoxWidget from '@/components/CardBoxWidget.vue'
import CardBoxTransaction from '@/components/CardBoxTransaction.vue'
import CardBoxClient from '@/components/CardBoxClient.vue'
import LayoutAuthenticated from '@/layouts/LayoutAuthenticated.vue'
import SectionTitleLineWithButton from '@/components/SectionTitleLineWithButton.vue'

const chartData = ref(null)

const fillChartData = () => {
  chartData.value = chartConfig.sampleChartData()
}

onMounted(() => {
  fillChartData()
})

const mainStore = useMainStore()
const username = localStorage.username

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
          color="text-emerald-500"
          :icon="mdiAccountMultiple"
          :number="numberOfClients"
          label="Company Clients"
        />
        <CardBoxWidget
          color="text-blue-500"
          :icon="mdiCartOutline"
          :number="numberOfSales"
          label="Your Sales"
        />
        <CardBoxWidget
          color="text-red-500"
          :icon="mdiChartTimelineVariant"
          :number="totalRevenue"
          prefix="$"
          label="Your Revenue"
        />
      </div>

      <SectionTitleLineWithButton :icon="mdiChartPie" title="Last sales">
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
            :date="sales.SaleDate"
            :seller="username"
          />
        </div>
      </div>
    </SectionMain>
  </LayoutAuthenticated>
</template>
