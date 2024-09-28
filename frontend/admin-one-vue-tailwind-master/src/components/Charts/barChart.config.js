// Chart Colors Configuration
export const chartColors = {
    default: {
      profit: '#00D1B2', // Green for profit
      totalEmployeesPayment: '#209CEE', // Blue for employees' payment
      vat: '#FF3860', // Red for VAT
      prodCosts: '#FF3860'
    }
  }
  
  // Generate chart data from API response
  export const generateBarChartData = (data) => {
    return {
        labels: data.labels,  // ['Month 1', 'Month 2', 'Month 3']
        datasets: data.datasets  // Array of datasets (profit, payments, VAT)
    }
  }
  