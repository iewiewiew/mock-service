import { createApp } from "vue";
import { createPinia } from "pinia";
import App from "./App.vue";
import router from "./router";
import ElementPlus from "element-plus";
import "element-plus/dist/index.css";
import "./styles/main.css"; // 导入全局样式
import './styles/common.css' // 导入全局样式
import { permissionDirective } from '@/directives/permission'

const app = createApp(App);

app.use(createPinia());
app.use(router);
app.use(ElementPlus);

// 全局注册权限指令
app.directive('permission', permissionDirective)

app.mount("#app");
