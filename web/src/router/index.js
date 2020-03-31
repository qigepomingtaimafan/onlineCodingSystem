import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '@/components/HelloWorld'
import Hello from '@/components/Hello'
import CodeEditor from '@/components/CodeEditor'

Vue.use(Router)

export default new Router({
  routes: [
    /*{
      path: '/',
      name: 'HelloWorld',
      component: HelloWorld
    },*/
    {
      path: '/',
      name: 'Hello',
      component: Hello
      //name: 'CodeEditor',
      //component: CodeEditor
    }
  ],
  mode: 'history'
})
