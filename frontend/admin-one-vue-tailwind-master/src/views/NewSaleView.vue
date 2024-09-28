<script setup>
import { reactive, ref, computed, watchEffect, watch, onBeforeMount} from 'vue'
import { mdiBallotOutline, mdiAccount, mdiMail, mdiGithub, mdiFlagOutline, mdiCancel, mdiCross, mdiClose } from '@mdi/js'
import SectionMain from '@/components/SectionMain.vue'
import CardBox from '@/components/CardBox.vue'
import FormCheckRadioGroup from '@/components/FormCheckRadioGroup.vue'
import FormFilePicker from '@/components/FormFilePicker.vue'
import FormField from '@/components/FormField.vue'
import FormControl from '@/components/FormControl.vue'
import BaseDivider from '@/components/BaseDivider.vue'
import BaseButton from '@/components/BaseButton.vue'
import BaseButtons from '@/components/BaseButtons.vue'
import SectionTitle from '@/components/SectionTitle.vue'
import LayoutAuthenticated from '@/layouts/LayoutAuthenticated.vue'
import SectionTitleLineWithButton from '@/components/SectionTitleLineWithButton.vue'
import NotificationBarInCard from '@/components/NotificationBarInCard.vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
import { useMainStore } from '@/stores/main'

const router = useRouter()
const mainStore = useMainStore()
const items = computed(() => mainStore.products)

onBeforeMount(() => {
  mainStore.getCompanyProducts()
})

watchEffect(() => {
  if (!mainStore._clients || mainStore._clients.length === 0) {
    mainStore.getClients()
  }
})

const selectClientOptions = computed(() => {
  return mainStore._clients.map((client, index) => ({
    id: `${client['ClientID']}`,
    label: `${client['FirstName']} ${client['LastName']}`,
  }))
})

// TODO backend, fazer uma tabela Products e um get products by id, usar o mainStore aqui
const selectProductOptions = computed(() => {
  return items.value.map((product, index) => ({
    id: `${product['ProductID']}`,
    label: `${product['ProductName']}`
  }))
})

const form = reactive({
  clientId: 'First Name',
  product: selectProductOptions[0],
  quantity: '1',
  price: getProductPrice(selectProductOptions[0]),
  client: getClientId(selectClientOptions[0]),
})

const customElementsForm = reactive({
  checkbox: ['lorem'],
  radio: 'one',
  switch: ['one'],
  file: null
})

watch(() => form.product, (newProduct) => {
  // Update the price when the product changes
  form.price = getProductPrice(newProduct['label'])
})

const submit = () => {
  const newSalePayload = {
    client_id: form.clientId['id'],
    product_id: form.product['id'],
    quantity: form.quantity,
    token: localStorage.getItem('token'),
    user_id: localStorage.getItem('userId'),
    comp_id: localStorage.getItem('companyId')
  }

  axios
    .post('http://localhost:5000/sales/new', newSalePayload)
    .then((response) => {
      if (response.status >= 200 && response.status < 300) {
        alert('Sale created successfully!');
        router.push('/sales');
      } else {
        alert('Failed to create sale. Please try again.');
      }
    })
    .catch((error) => {
      alert(error.message);
    });
}

const formStatusWithHeader = ref(true)

const formStatusCurrent = ref(0)

const formStatusOptions = ['info', 'success', 'danger', 'warning']

const formStatusSubmit = () => {
  formStatusCurrent.value = formStatusOptions[formStatusCurrent.value + 1]
    ? formStatusCurrent.value + 1
    : 0
}

function getClientId(clientName) {
  clientName = clientName
  if(!clientName || clientName === undefined || clientName == ''){
    return null
  }
  const [firstName, lastName] = clientName.split(' ');

  const client = mainStore._clients.find(client => 
    client.FirstName === firstName && client.LastName === lastName
  );

  return client ? client.ClientID : null;
}

function getProductPrice(productName) {
  if(!productName || productName === undefined || productName == ''){
    return null
  }

  const product = items.value.find(product => 
    product.ProductName === productName
  );

  return product ? product.Price : null;
}


</script>

<template>
  <LayoutAuthenticated>
    <SectionMain>
      <SectionTitleLineWithButton :icon="mdiBallotOutline" title="New Sale" main>
        <BaseButton
          to="/sales"
          :icon="mdiClose"
          label=""
          color="danger"
          rounded-full
          small
        />
      </SectionTitleLineWithButton>
      <CardBox :class="cardClass" is-form @submit.prevent="submit">
        <FormField label="Client">
          <FormControl v-model="form.clientId" :options="selectClientOptions" />
        </FormField>

        <FormField label="Product">
          <FormControl v-model="form.product" :options="selectProductOptions" />
        </FormField>

        <FormField label="Quantity" help="Insert quantity">
          <FormControl
            v-model="form.quantity"
            :icon="mdiIdCard"
            name="last name"
          />
        </FormField>

        <template #footer>
          <BaseButtons>
            <BaseButton type="submit" color="info" label="Submit" />
            <BaseButton type="reset" color="danger" outline label="Cancel" to="/sales" />
          </BaseButtons>
        </template>
      </CardBox>
    </SectionMain>
  </LayoutAuthenticated>
</template>
