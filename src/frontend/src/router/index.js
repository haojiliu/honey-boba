import Vue from 'vue'
import Router from 'vue-router'
import DesignViewer from '@/components/DesignViewer'
import DesignUploader from '@/components/DesignUploader'
import Uploaded from '@/components/Uploaded'
import NotFound from '@/components/NotFound'
import FAQ from '@/components/FAQ'
Vue.use(Router)

const routes = [
  { path: '/', component: DesignViewer },
  { path: '/designs', component: DesignViewer },
  { path: '/upload', component: DesignUploader },
  { path: '/uploaded/:uri', component: Uploaded },
  { path: '/faq', component: FAQ },
  { path: '*', component: NotFound }
]

export default new Router({
  routes,
  mode: 'history'
})
