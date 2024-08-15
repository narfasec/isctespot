import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import axios from 'axios'

export const useMainStore = defineStore('main', () => {
  const userName = ref('John Doe')
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
  const userOverview = ref([])
  const adminOverview = ref([])

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
4
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
        this.userOverview = r.data
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
      company_id: Number(localStorage.getItem('companyId'))
    };
    axios
      .post(url, adminOverviewPayload)
      .then((r) => {
        this.adminOverview = r.data
      })
      .catch((error) => {
        alert(error.message);
    });
  }

  return {
    userName,
    userEmail,
    userAvatar,
    isFieldFocusRegistered,
    clients,
    history,
    userOverview,
    adminOverview,
    setUser,
    fetchSampleClients,
    fetchSampleHistory,
    getUserInfo,
    getAdminOverview,
  }
})
