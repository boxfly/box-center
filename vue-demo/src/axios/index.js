import axios from "axios";
import { MessageBox } from 'mint-ui';

// 引入常量模块
import Constants from '@/Constants.vue';

// 修改axios请求的默认配置(配置会以一个优先顺序进行合并。这个顺序是：在 lib/defaults.js 找到的库的默认值，然后是实例的 defaults 属性，最后是请求的 config 参数。)
//` baseURL` 将自动加在 `url` 前面，除非 `url` 是一个绝对 URL。
axios.defaults.baseURL = Constants.projectBaseAddress;

// 添加请求拦截器
axios.interceptors.request.use(function(config) {
	// 模拟处理前增加token
	return config;
}, function(error) {
	// 对请求错误做些什么
	return Promise.reject(error);
});

// 添加响应拦截器
axios.interceptors.response.use(function(response) {
	// 对响应数据做点什么
	if(response.data.success) {
		// 如果是成功返回信息之后提取出来返回以供后面的调用链使用(后台返回的JSON数据)
		return response.data;
	} else {
		MessageBox.alert(response.data.msg);
		return new Promise(function(resolve, reject) {
			//                    resolve('success1');
			//                  reject('error');
		});
	}
}, function(error) {
	// 对响应错误做点什么
	return Promise.reject(error);
});

export default axios;