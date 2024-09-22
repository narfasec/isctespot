<script setup>
import { onBeforeMount, onMounted, computed, ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import { mdiTableBorder, mdiPlus } from '@mdi/js'
import { useMainStore } from '@/stores/main'
import SectionMain from '@/components/SectionMain.vue'
import CardBox from '@/components/CardBox.vue'
import LayoutAuthenticated from '@/layouts/LayoutAuthenticated.vue'
import SectionTitleLineWithButton from '@/components/SectionTitleLineWithButton.vue'
import BaseButton from '@/components/BaseButton.vue'
import TableCompanyCashFlowEmployees from '@/components/TableCompanyCashFlowEmployees.vue'
import * as barChartConfig from '@/components/Charts/barChart.config.js'
import BarChart from '@/components/Charts/BarChart.vue'

// Access the main store
const mainStore = useMainStore()
const chartData = ref(null)
const cashflow = computed(() => mainStore.cashFlow)
const router = useRouter()

// Fetch cashflow data before mounting the component
onBeforeMount(() => {
  mainStore.getCompanyCashFlow()  // Fetch data from the API
})

// Watch for changes in the cashflow and trigger chart generation when data is ready
watch(cashflow, (newCashflow) => {
  console.log(newCashflow.vat_value)
  if (newCashflow && newCashflow.status === 'Ok') {
    const apiData = {
      profit: newCashflow.profit,
      totalEmployeesPayment: newCashflow.totalEmployeesPayment,
      vat_value: newCashflow.vat_value
    }

    // Repeat the same value for 3 months
    const dataForThreeMonths = [
      apiData.profit,
      apiData.profit,
      apiData.profit
    ]

    const employeePaymentsForThreeMonths = [
      apiData.totalEmployeesPayment,
      apiData.totalEmployeesPayment,
      apiData.totalEmployeesPayment
    ]

    const vatForThreeMonths = [
      parseInt(apiData.vat_value),
      parseInt(apiData.vat_value),
      parseInt(apiData.vat_value)
    ]

    const subscription = [
      500,
      500,
      500
    ]
    
    // Generate chart data
    chartData.value = barChartConfig.generateBarChartData({
      labels: ['Month 1', 'Month 2', 'Month 3'],  // X-axis labels for months
      datasets: [
        {
          label: 'Profit',
          data: dataForThreeMonths,
          backgroundColor: 'rgba(75, 192, 192, 0.2)',
          borderColor: 'rgba(75, 192, 192, 1)',
          borderWidth: 1
        },
        {
          label: 'Employee Payments',
          data: employeePaymentsForThreeMonths,
          backgroundColor: 'rgba(153, 102, 255, 0.2)',
          borderColor: 'rgba(153, 102, 255, 1)',
          borderWidth: 1
        },
        {
          label: 'VAT value',
          data: vatForThreeMonths,
          backgroundColor: 'rgba(255, 159, 64, 0.2)',
          borderColor: 'rgba(255, 159, 64, 1)',
          borderWidth: 1
        },
        {
          label: 'Subscription',
          data: subscription,
          backgroundColor: 'rgba(255, 159, 64, 0.2)',
          borderColor: 'rgba(255, 159, 64, 1)',
          borderWidth: 1
        }
      ]
    })
  }
}, { immediate: true }) // Watcher will run immediately when cashflow is available

</script>

<template>
  <LayoutAuthenticated>
    <SectionMain>
      <SectionTitleLineWithButton :icon="mdiTableBorder" title="Cash Flow" main>
        <BaseButton
          target="_blank"
          :icon="mdiPlus"
          label="Pay Employees"
          color="success"
          rounded-full
          small
          class="hover:shadow-lg transform hover:scale-105 transition-transform duration-200"
          @click="newEmployee"
        />
      </SectionTitleLineWithButton>

      <div class="grid grid-cols-1 gap-6 mb-6">
        <CardBox>
          <div class="p-6">
            <h3 class="text-lg font-semibold">Profit</h3>
            <p class="text-2xl font-bold text-green-600">+{{ cashflow.profit || 0 | currency }} $</p>
          </div>
        </CardBox>
      </div>

      <div class="grid grid-cols-1 gap-6">
        <CardBox class="mb-6">
          <div v-if="chartData">
            <bar-chart :data="chartData" class="h-96" />
          </div>
        </CardBox>
      </div>

      <div class="mt-6">
        <h3 class="text-lg font-semibold mb-4">Employees</h3>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <CardBox v-for="(employee, index) in cashflow.employees || []" :key="index">
            <div class="p-6">
              <h4 class="font-bold">{{ employee.Username }}</h4>
              <p>Total Sales: {{ employee.TotalSales }}</p>
              <p>Total Commission: {{ employee.TotalCommission }}</p>
              <p>Commission Percentage: {{ employee.CommissionPercentage }}%</p>
            </div>
          </CardBox>
        </div>
      </div>
    </SectionMain>
  </LayoutAuthenticated>
</template>