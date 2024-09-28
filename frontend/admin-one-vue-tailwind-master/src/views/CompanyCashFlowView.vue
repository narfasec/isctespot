<script setup>
import { onBeforeMount, computed, ref, watch } from 'vue'
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

// Acessa o store principal
const mainStore = useMainStore()
const chartData = ref(null)
const cashflow = computed(() => mainStore.cashFlow)
const router = useRouter()

// Função para navegar para nova página de funcionário (exemplo)
const newEmployee = () => {
  router.push('/new-employee') // Substitui com a tua rota real
}

// Busca os dados de cashflow antes de montar o componente
onBeforeMount(() => {
  console.log('onBeforeMount')
  mainStore.getCompanyCashFlow()
})

// Observa mudanças em cashflow e gera dados do gráfico quando os dados estão prontos
watch(cashflow, (newCashflow) => {
  console.log('Cashflow Watch:', newCashflow)
  if (newCashflow && newCashflow.status === 'Ok') {
    const apiDataJuly = {
      profit: newCashflow.July.profit,
      totalEmployeesPayment: newCashflow.July.totalEmployeesPayment,
      vat_value: newCashflow.July.vat_value,
      prodCosts: newCashflow.July.prod_costs
    }
    const apiDataAugust = {
      profit: newCashflow.August.profit,
      totalEmployeesPayment: newCashflow.August.totalEmployeesPayment,
      vat_value: newCashflow.August.vat_value,
      prodCosts: newCashflow.August.prod_costs
    }
    const apiDataSeptember = {
      profit: newCashflow.September.profit,
      totalEmployeesPayment: newCashflow.September.totalEmployeesPayment,
      vat_value: newCashflow.September.vat_value,
      prodCosts: newCashflow.August.prod_costs
    }

    // Valores para três meses
    const dataForThreeMonths = [
      apiDataJuly.profit,
      apiDataAugust.profit,
      apiDataSeptember.profit
    ]

    const employeePaymentsForThreeMonths = [
      apiDataJuly.totalEmployeesPayment,
      apiDataAugust.totalEmployeesPayment,
      apiDataSeptember.totalEmployeesPayment
    ]

    const vatForThreeMonths = [
      parseInt(apiDataJuly.vat_value),
      parseInt(apiDataAugust.vat_value),
      parseInt(apiDataSeptember.vat_value)
    ]

    const subscription = [ 
      500,
      500,
      500
    ]

    const prodCosts = [
      apiDataJuly.prodCosts,
      apiDataAugust.prodCosts,
      apiDataSeptember.prodCosts      
    ]
    
    // Gera os dados do gráfico
    chartData.value = barChartConfig.generateBarChartData({
      labels: ['July', 'August', 'September'],  // Labels para os meses
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
        },
        {
          label: 'Production costs',
          data: prodCosts,
          backgroundColor: 'rgba(255, 159, 64, 0.2)',
          borderColor: 'rgba(255, 159, 64, 1)',
          borderWidth: 1
        }
      ]
    })
  }
}, { immediate: true }) // O watcher executa imediatamente quando cashflow está disponível

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
            <h3 class="text-lg font-semibold">Current Balance</h3>
            <p class="text-2xl font-bold text-green-600">+{{ cashflow.profit || 0 | currency }} $</p>
          </div>
        </CardBox>
      </div>

      <div class="grid grid-cols-1 gap-6">
        <CardBox class="mb-6">
          <div v-if="chartData">
            <BarChart :data="chartData" class="h-96" />
          </div>
        </CardBox>
      </div>

      <!-- Seção de Julho -->
      <div class="mt-6">
        <h3 class="text-lg font-semibold mb-4">July</h3>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <CardBox v-for="(employee, index) in cashflow.July?.employees || []" :key="index">
            <div class="p-6">
              <h4 class="font-bold">{{ employee.Username }}</h4>
              <p>Total Sales: {{ employee.TotalSales }}</p>
              <p>Total Commission: {{ employee.TotalCommission }}</p>
              <p>Commission Percentage: {{ employee.CommissionPercentage }}%</p>
            </div>
          </CardBox>
        </div>
      </div>

      <!-- Seção de Agosto -->
      <div class="mt-6">
        <h3 class="text-lg font-semibold mb-4">August</h3>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <CardBox v-for="(employee, index) in cashflow.August?.employees || []" :key="index">
            <div class="p-6">
              <h4 class="font-bold">{{ employee.Username }}</h4>
              <p>Total Sales: {{ employee.TotalSales }}</p>
              <p>Total Commission: {{ employee.TotalCommission }}</p>
              <p>Commission Percentage: {{ employee.CommissionPercentage }}%</p>
            </div>
          </CardBox>
        </div>
      </div>

      <!-- Seção de Setembro -->
      <div class="mt-6">
        <h3 class="text-lg font-semibold mb-4">September</h3>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <CardBox v-for="(employee, index) in cashflow.September?.employees || []" :key="index">
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
