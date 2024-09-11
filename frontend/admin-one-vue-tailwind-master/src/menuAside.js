import {
  mdiAccountCircle,
  mdiMonitor,
  mdiGithub,
  mdiLock,
  mdiAlertCircle,
  mdiSquareEditOutline,
  mdiTable,
  mdiViewList,
  mdiTelevisionGuide,
  mdiResponsive,
  mdiPalette,
  mdiReact,
  mdiCash100,
  mdiSalesforce,
  mdiNaturePeople,
  mdiGroup,
  mdiSeatIndividualSuite,
  mdiTarget,
  mdiVlc,
  mdiMustache,
  mdiMagicStaff,
  mdiImageFilterCenterFocus,
  mdiHatFedora,
  mdiBookAccount,
  mdiBookPlay,
  mdiBook,
  mdiCash
} from '@mdi/js'

const menuItems = [
  {
    to: '/dashboard',
    icon: mdiMonitor,
    label: 'Dashboard'
  },
  {
    to: '/clients',
    icon: mdiHatFedora,
    label: 'Clients'
  },
  {
    to: '/sales',
    icon: mdiCash,
    label: 'Sales'
  },
  // {
  //   to: '/tables',
  //   label: 'Tables',
  //   icon: mdiTable
  // },
  // {
  //   to: '/forms',
  //   label: 'Forms',
  //   icon: mdiSquareEditOutline
  // },
  // {
  //   to: '/ui',
  //   label: 'UI',
  //   icon: mdiTelevisionGuide
  // },
  // {
  //   to: '/responsive',
  //   label: 'Responsive',
  //   icon: mdiResponsive
  // },
  // {
  //   to: '/',
  //   label: 'Styles',
  //   icon: mdiPalette
  // },
  // {
  //   to: '/profile',
  //   label: 'Profile',
  //   icon: mdiAccountCircle
  // },
  // {
  //   to: '/error',
  //   label: 'Error',
  //   icon: mdiAlertCircle
  // }
]

// Check if the user is an admin
if (localStorage.getItem('isAdmin') === 'true') {
  menuItems.push({
    label: 'Company',
    icon: mdiViewList,
    menu: [
      {
        to: '/company/employees',
        label: 'Employees'
      },
      {
        to: '/company/cash-flow',
        label: 'Cash Flow'
      },
      {
        to: '/company/products',
        label: 'Products'
      }
    ]
  })
}

// Add the remaining static menu items
// menuItems.push(
//   {
//     href: 'https://github.com/justboil/admin-one-vue-tailwind',
//     label: 'GitHub',
//     icon: mdiGithub,
//     target: '_blank'
//   },
//   {
//     href: 'https://github.com/justboil/admin-one-react-tailwind',
//     label: 'React version',
//     icon: mdiReact,
//     target: '_blank'
//   }
// )

export default menuItems
