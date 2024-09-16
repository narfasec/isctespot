<script setup>
import { ref, watch, computed, onMounted, onBeforeUnmount } from 'vue'
import {
  Chart,
  BarElement,  // For bar chart
  BarController,
  CategoryScale,
  LinearScale,
  Tooltip
} from 'chart.js'

const props = defineProps({
  data: {
    type: Object,
    required: true
  }
})

const root = ref(null)
let chart

// Register necessary chart elements for bar chart
Chart.register(BarElement, BarController, CategoryScale, LinearScale, Tooltip)

onMounted(() => {
    chart = new Chart(root.value, {
        type: 'bar',  // Changed to 'bar' for bar chart
        data: props.data,
        options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
            y: {
            display: true,
            title: {
                display: true,
                text: 'Cash ($)'
            }
            },
            x: {
            display: true,
            title: {
                display: true,
                text: 'Month'
            }
            }
        },
        plugins: {
            legend: {
            display: true,  // Show legend
            }
        }
        }
    })
})

// Clean-up the chart when the component is unmounted to prevent memory leaks
onBeforeUnmount(() => {
  if (chart) {
    chart.destroy()
  }
})

// Computed property to reactively update chart data
const chartData = computed(() => props.data)

watch(chartData, (data) => {
  if (chart) {
    chart.data = data
    chart.update()
  }
})
</script>

<template>
  <canvas ref="root" />
</template>
