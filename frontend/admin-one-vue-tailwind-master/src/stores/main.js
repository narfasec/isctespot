import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import axios from 'axios'

export const useMainStore = defineStore('main', () => {
  const userName = ref(localStorage.getItem('username'))
  const userEmail = ref('doe.doe.doe@example.com')
  const userAvatar = computed(
    () =>
      `https://api.dicebear.com/7.x/avataaars/svg?seed=${userEmail.value.replace(
        /[^a-z0-9]+/gi,
        '-'
      )}`
  )

  const isFieldFocusRegistered = ref(false)
  const clients = ref([])
  const history = ref([])
  const sales = ref([])
  const _clients = ref([])
  const _employees = ref([])
  const products = ref([])
  const totalRevenue = ref([])
  const cashFlow = ref([])
  const last3Sales = ref([])
  // const userName = ref()

  function setUser(payload) {
    if (payload.name) {
      userName.value = payload.name
    }
    if (payload.email) {
      userEmail.value = payload.email
    }
  }

  function fetchSampleClients() {
    axios
      .get(`data-sources/clients.json?v=3`)
      .then((result) => {
        clients.value = result?.data?.data
      })
      .catch((error) => {
        alert(error.message)
      })
  }

  function fetchSampleHistory() {
    axios
      .get(`data-sources/history.json`)
      .then((result) => {
        history.value = result?.data?.data
      })
      .catch((error) => {
        alert(error.message)
      })
  }

  function getUserInfo() {
    const url = "http://localhost:5000/user/overview"
    const userOverviewPayload = {
      user_id: Number(localStorage.getItem('userId')),
      token: localStorage.getItem('token'),
    };
    axios
      .post(url, userOverviewPayload)
      .then((r) => {
        this.sales = r.data.sales
        this.last3Sales = r.data.last_3_sales
      })
      .catch((error) => {
        alert(error.message);
    });
  }

  function getAdminOverview() {
    const url = "http://localhost:5000/analytics"
    const adminOverviewPayload = {
      user_id: Number(localStorage.getItem('userId')),
      token: localStorage.getItem('token'),
      comp_id: Number(localStorage.getItem('companyId'))
    };
    axios
      .post(url, adminOverviewPayload)
      .then((r) => {
        this.sales = r.data.sales
        this.totalRevenue = r.data.revenue
        this.last3Sales = r.data.last_3_sales
      })
      .catch((error) => {
        alert(error.message);
    });
  }

  function getClients() {
    const url = "http://localhost:5000/clients"
    const clientsPayload = {
      user_id: Number(localStorage.getItem('userId')),
    };
    axios
      .post(url, clientsPayload)
      .then((r) => {
        this._clients = r.data.clients
      })
      .catch((error) => {
        alert(error.message);
    });
  }

  function getCompanyEmployees() {
    const url = "http://localhost:5000/employees"
    const employeesPayload = {
      user_id: localStorage.getItem('userId'),
      token: localStorage.getItem('token'),
      comp_id: localStorage.getItem('companyId')
    };
    axios
      .post(url, employeesPayload)
      .then((r) => {
        this._employees = r.data.employees
      })
      .catch((error) => {
        alert(error.message);
    });
  }

  function getCompanyProducts() {
    const url = "http://localhost:5000/products"
    const productsPayload = {
      user_id: localStorage.getItem('userId'),
      token: localStorage.getItem('token'),
      comp_id: localStorage.getItem('companyId')
    };
    axios
      .post(url, productsPayload)
      .then((r) => {
        this.products = r.data.products
      })
      .catch((error) => {
        alert(error.message);
    });
  }

  function getCompanyCashFlow() {
    const url = "http://localhost:5000/cash-flow"
    const cashFlowPayload = {
      country_code: 'PT',
      token: localStorage.getItem('token'),
      comp_id: localStorage.getItem('companyId')
    };
    axios
      .post(url, cashFlowPayload)
      .then((r) => {
        this.cashFlow = r.data
        console.log(r.data)
        console.log('fftcvhgj')
      })
      .catch((error) => {
        alert(error.message);
    });
    
    
  }

  function deleteEmployee(employee_id){
    const url = "http://localhost:5000/employee/delete"
    const employeesPayload = {
      user_id: localStorage.getItem('userId'),
      token: localStorage.getItem('token'),
      employee_id: employee_id
    };
    axios
      .post(url, employeesPayload)
      .then((r) => {
        router.push('/employees')
      })
      .catch((error) => {
        alert(error.message);
    });
  }

  function calculateSalesRevenue() {
    let totalRevenue = 0;
    // Iterate through each sale and calculate revenue
    this.sales.forEach((sale) => {
      const revenue = sale.SellingPrice * sale.Quantity;
      totalRevenue += revenue;
    });
  
    this.totalRevenue = totalRevenue;
  }

  return {
    userName,
    userEmail,
    userAvatar,
    isFieldFocusRegistered,
    clients,
    history,
    sales,
    _clients,
    _employees,
    products,
    totalRevenue,
    cashFlow,
    setUser,
    fetchSampleClients,
    fetchSampleHistory,
    getUserInfo,
    getAdminOverview,
    getClients,
    getCompanyEmployees,
    getCompanyProducts,
    getCompanyCashFlow,
    deleteEmployee,
    calculateSalesRevenue
  }
})
