<script setup>
import { computed, ref, onMounted} from 'vue'
import { useMainStore } from '@/stores/main'
import { mdiAccountCheck, mdiCheckDecagram } from '@mdi/js'
import BaseLevel from '@/components/BaseLevel.vue'
import UserAvatarCurrentUser from '@/components/UserAvatarCurrentUser.vue'
import CardBox from '@/components/CardBox.vue'
import FormCheckRadio from '@/components/FormCheckRadio.vue'
import PillTag from '@/components/PillTag.vue'

const mainStore = useMainStore()

const userName = computed(() => mainStore.userName)

const userSwitchVal = ref(false)

const isAdmin = ref(false)

onMounted(() => {
  isAdmin.value = localStorage.getItem('isAdmin') === 'true'
})
</script>

<template>
  <CardBox>
    <BaseLevel type="justify-around lg:justify-center">
      <UserAvatarCurrentUser class="lg:mx-12" />
      <div class="space-y-3 text-center md:text-left lg:mx-12">
        <div class="flex justify-center md:block">
        </div>
        <h1 class="text-2xl">
          Hello, <b>{{ userName }}</b>!
        </h1>
        <p>Last login <b>12 mins ago</b> from <b>127.0.0.1</b></p>
        <div v-if="isAdmin" class="flex justify-center md:block">
          <PillTag label="Admin" color="info" :icon="mdiAccountCheck" />
        </div>
      </div>
    </BaseLevel>
  </CardBox>
</template>
