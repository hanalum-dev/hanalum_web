import Vue from 'vue';

Vue.config.productionTip = false;

import VueFormWizard from 'vue-form-wizard';
import BootstrapVue from 'bootstrap-vue';
import JohaApplyFormWizard from './components/JohaApplyFormWizard.vue';

import 'vue-form-wizard/dist/vue-form-wizard.min.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap-vue/dist/bootstrap-vue.css';

Vue.use(BootstrapVue)
Vue.use(VueFormWizard)

var app = new Vue({
  render: h => h(JohaApplyFormWizard),
}).$mount('#app');
