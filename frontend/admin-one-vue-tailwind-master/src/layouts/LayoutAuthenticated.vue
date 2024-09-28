<script setup>
import { mdiForwardburger, mdiBackburger, mdiMenu } from '@mdi/js'
import { ref, onBeforeMount } from 'vue'
import { useRouter } from 'vue-router'
import menuAside from '@/menuAside.js'
import menuNavBar from '@/menuNavBar.js'
import { useDarkModeStore } from '@/stores/darkMode.js'
import BaseIcon from '@/components/BaseIcon.vue'
import NavBar from '@/components/NavBar.vue'
import NavBarItemPlain from '@/components/NavBarItemPlain.vue'
import AsideMenu from '@/components/AsideMenu.vue'
import FooterBar from '@/components/FooterBar.vue'
import axios from 'axios'
import { useMainStore } from '@/stores/main'


const mainStore = useMainStore()
onBeforeMount(async () => {
  try {
    const isAdmin = await waitForIsAdmin()

    console.log('isAdmin found:', isAdmin)
    mainStore.isAdmin = isAdmin

  } catch (error) {
    console.error(error.message)
    // Handle the failure case, such as redirecting or showing an error
  }
})

function checkIsAdmin() {
  return localStorage.getItem('isAdmin')
}

function waitForIsAdmin(retryDelay = 500, maxRetries = 10) {
  return new Promise((resolve, reject) => {
    let attempts = 0

    const check = () => {
      const isAdmin = checkIsAdmin()
      if (isAdmin) {
        resolve(isAdmin)
      } else {
        attempts++
        if (attempts < maxRetries) {
          setTimeout(check, retryDelay)
        } else {
          reject(new Error('isAdmin value not found after multiple attempts'))
        }
      }
    }

    check()
  })
}

const layoutAsidePadding = 'xl:pl-60'

const darkModeStore = useDarkModeStore()

const router = useRouter()

const isAsideMobileExpanded = ref(false)
const isAsideLgActive = ref(false)

router.beforeEach(() => {
  isAsideMobileExpanded.value = false
  isAsideLgActive.value = false
})

const menuClick = (event, item) => {
  if (item.isToggleLightDark) {
    darkModeStore.set()
  }

  if (item.isLogout) {
    const url = "http://localhost:5000/logout"
    const userLogoutPayload = {
      user_id: Number(localStorage.getItem('userId')),
    };
    axios
      .post(url, userLogoutPayload)
      .then((r) => {
        localStorage.clear()
        router.push('/')
      })
      .catch((error) => {
        alert(error.message);
    });
  }
}
</script>

<template>
  <div
    :class="{
      'overflow-hidden lg:overflow-visible': isAsideMobileExpanded
    }"
  >
    <div
      :class="[layoutAsidePadding, { 'ml-60 lg:ml-0': isAsideMobileExpanded }]"
      class="pt-14 min-h-screen w-screen transition-position lg:w-auto bg-gray-50 dark:bg-slate-800 dark:text-slate-100"
    >
      <NavBar
        :menu="menuNavBar"
        :class="[layoutAsidePadding, { 'ml-60 lg:ml-0': isAsideMobileExpanded }]"
        @menu-click="menuClick"
      >
        <NavBarItemPlain
          display="flex lg:hidden"
          @click.prevent="isAsideMobileExpanded = !isAsideMobileExpanded"
        >
          <BaseIcon :path="isAsideMobileExpanded ? mdiBackburger : mdiForwardburger" size="24" />
        </NavBarItemPlain>
        <NavBarItemPlain display="hidden lg:flex xl:hidden" @click.prevent="isAsideLgActive = true">
          <BaseIcon :path="mdiMenu" size="24" />
        </NavBarItemPlain>
      </NavBar>
      <AsideMenu
        :is-aside-mobile-expanded="isAsideMobileExpanded"
        :is-aside-lg-active="isAsideLgActive"
        :menu="menuAside"
        @menu-click="menuClick"
        @aside-lg-close-click="isAsideLgActive = false"
      />
      <slot />
      <FooterBar>
        Get more with
        <a href="https://tailwind-vue.justboil.me/" target="_blank" class="text-blue-600"
          >Premium version</a
        >
      </FooterBar>
    </div>
  </div>
</template>
