<script setup>
import { useRouter } from 'vue-router'
import { useDarkModeStore } from '@/stores/darkMode.js'
import { gradientBgPurplePink } from '@/colors.js'
import SectionMain from '@/components/SectionMain.vue'
import CardBox from '@/components/CardBox.vue'
import LayoutGuest from '@/layouts/LayoutGuest.vue'
import BaseButton from '@/components/BaseButton.vue'

const styles = ['white', 'basic']

const darkModeStore = useDarkModeStore()

darkModeStore.set(false)

const router = useRouter()

</script>

<template>
  <LayoutGuest>
    <!-- Top Navigation Bar -->

    <div :class="gradientBgPurplePink" class="flex min-h-screen items-center justify-center">
      <SectionMain>
        <h1 class="text-4xl md:text-5xl text-center text-white font-bold mt-12 mb-3 lg:mt-0">
          IscteSpot
        </h1>
        <h2 class="text-xl md:text-xl text-center text-white mb-12">
          Sales management easier than ever
        </h2>
        <div class="grid gap-6 grid-cols-1 lg:grid-cols-2 px-6 max-w-6xl mx-auto">
          <CardBox
            v-for="style in styles"
            :key="style"
          >
            <div class="mb-3 md:mb-6">
              <img
                :src="`https://static.justboil.me/templates/one/small/${style}-v3.png`"
                width="1280"
                height="720"
              />
            </div>

            <h1 class="text-xl md:text-2xl font-black capitalize">
              {{ style }}
            </h1>
            <h2 class="text-lg md:text-xl">& Dark mode</h2>
          </CardBox>
        </div>
        <div class="grid gap-6 grid-cols-1 lg:grid-cols-3 px-6 max-w-6xl mx-auto mb-3 md:mb-6">
          <div class="col-span-full flex justify-center mt-6">
              <BaseButton
                color="info"
                label="Start Now"
                :rounded-full=true
                to="/login"
              />
          </div>
        </div>
        <div class="flex justify-center mt-6">
          <img
            :src="`https://imatch.pt/wp-content/uploads/2020/12/logo-iscte.png`"
            width="500"
            height="100"
            alt="ISCTE Logo"
          />
        </div>
      </SectionMain>
    </div>
  </LayoutGuest>
</template>

<style scoped>
/* Styles for the Navbar */
.navbar {
  background-color: #2d3748; /* Dark background color */
  padding: 1rem;
}

.nav-links {
  display: flex;
  justify-content: center;
  list-style-type: none;
  margin: 0;
  padding: 0;
}

.nav-links li {
  margin: 0 1rem;
}

.nav-links a {
  color: white;
  text-decoration: none;
  font-size: 1.2rem;
  font-weight: bold;
  transition: color 0.3s ease;
}

.nav-links a:hover {
  color: #63b3ed; /* Light blue on hover */
}
</style>
