import Vue from 'vue'
import App from './App.vue'

Vue.config.productionTip = false

import VueFormWizard from 'vue-form-wizard'
import BootstrapVue from 'bootstrap-vue'

import 'vue-form-wizard/dist/vue-form-wizard.min.css'
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

Vue.use(BootstrapVue)
Vue.use(VueFormWizard)


new Vue({
  render: h => h(App),
}).$mount('#app')
