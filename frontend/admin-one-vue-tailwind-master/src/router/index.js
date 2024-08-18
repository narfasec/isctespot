import { createRouter, createWebHashHistory } from 'vue-router'
import Style from '@/views/StyleView.vue'
import Home from '@/views/HomeView.vue'

const routes = [
  {
    meta: {
      title: 'Select style'
    },
    path: '/',
    name: 'style',
    component: Style
  },
  {
    // Document title tag
    // We combine it with defaultDocumentTitle set in `src/main.js` on router.afterEach hook
    meta: {
      title: 'Dashboard',
      requiresAuth: true
    },
    path: '/dashboard',
    name: 'dashboard',
    component: Home
  },
  {
    meta: {
      title: 'Clients',
      requiresAuth: true
    },
    path: '/clients',
    name: 'clients',
    component: () => import('@/views/ClientsView.vue')
  },
  {
    meta: {
      title: 'New Client',
      requiresAuth: true
    },
    path: '/clients/new',
    name: 'new clients',
    component: () => import('@/views/NewClientView.vue')
  },
  {
    meta: {
      title: 'Sales',
      requiresAuth: true
    },
    path: '/sales',
    name: 'sales',
    component: () => import('@/views/SalesView.vue')
  },
  {
    meta: {
      title: 'Employees',
      requiresAuth: true
    },
    path: '/company/employees',
    name: 'employees',
    component: () => import('@/views/CompanyEmployeesView.vue')
  },
  {
    meta: {
      title: 'New mployee',
      requiresAuth: true
    },
    path: '/company/employees/new',
    name: 'new employee',
    component: () => import('@/views/NewEmployeeView.vue')
  },
  {
    meta: {
      title: 'Cash flow',
      requiresAuth: true
    },
    path: '/company/cash-flow',
    name: 'cash-flow',
    component: () => import('@/views/CompanyCashFlowView.vue')
  },
  ////////////////////////////////////////////////////////////////////////////////////////////////////////
  {
    meta: {
      title: 'Tables'
    },
    path: '/tables',
    name: 'tables',
    component: () => import('@/views/TablesView.vue')
  },
  {
    meta: {
      title: 'Forms'
    },
    path: '/forms',
    name: 'forms',
    component: () => import('@/views/FormsView.vue')
  },
  {
    meta: {
      title: 'Profile'
    },
    path: '/profile',
    name: 'profile',
    component: () => import('@/views/ProfileView.vue')
  },
  {
    meta: {
      title: 'Ui'
    },
    path: '/ui',
    name: 'ui',
    component: () => import('@/views/UiView.vue')
  },
  {
    meta: {
      title: 'Responsive layout'
    },
    path: '/responsive',
    name: 'responsive',
    component: () => import('@/views/ResponsiveView.vue')
  },
  {
    meta: {
      title: 'Login'
    },
    path: '/login',
    name: 'login',
    component: () => import('@/views/LoginView.vue')
  },
  {
    meta: {
      title: 'Signup'
    },
    path: '/signup',
    name: 'signup',
    component: () => import('@/views/SignupView.vue')
  },
  {
    meta: {
      title: 'Error'
    },
    path: '/error',
    name: 'error',
    component: () => import('@/views/ErrorView.vue')
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    return savedPosition || { top: 0 }
  }
})

router.beforeEach((to, from, next) => {
  // Check if the route requires authentication
  if (to.matched.some(record => record.meta.requiresAuth)) {
    const token = localStorage.getItem('token');
    
    // Regex pattern to match the token
    const regex = /^[A-Z0-9]{6}$/; // Simplified regex without quotes

    // If the token is not valid, redirect to login
    if (!token || !regex.test(token)) {
      next({
        path: '/login',
        query: { redirect: to.fullPath } // Save the intended route for after login
      });
    } else {
      next(); // Token is valid, allow navigation
    }
  } else {
    next(); // Route does not require authentication
  }
});

export default router
