<template>
	<div class="login">
		<form v-if="!isReg">
			<h1>欢迎来到XXX系统</h1>
			<br/>
			<mt-field label="用户名" placeholder="Input username" v-model="username"></mt-field>
			<mt-field label="密    码" placeholder="Input password" type="password" v-model="password"></mt-field>
			<mt-button size="large" type="primary" @click.prevent="login()" key="login">登录</mt-button>
			<br/>
			<mt-button size="large" type="default" @click.prevent="reg()" key="reg" plain>注册</mt-button>
			<br/>
      <x-button type="warn">vux按钮</x-button>
		</form>
		<div v-else>
			<h1>注册</h1>
			<mt-field label="用户名" placeholder="Input username" v-model="username"></mt-field>
			<mt-field label="用户姓名" placeholder="Input userfullname" v-model="userfullname"></mt-field>
			<mt-field label="密    码" placeholder="Input password" type="password" v-model="password"></mt-field>
			<mt-field label="电    话" placeholder="Input phone" v-model="phone"></mt-field>
			<mt-radio title="性    别" v-model="sex" :options="sexOptions" align="right">
			</mt-radio>
			<mt-button size="large" type="primary" @click="addUser()" key="doReg">注册</mt-button>
			<br/>
			<mt-button size="large" type="default" @click="cancel()" key="cancel" plain>取消</mt-button>
		</div>

	</div>
</template>

<script>
	import store from '@/store';
	import { MessageBox } from 'mint-ui';
	import { Toast } from 'mint-ui';
	import axios from "@/axios";

	var login = {
		name: 'login',
		store,
		data() {
			return {
				isReg: false,
				username: '',
				userfullname: '',
				password: '',
				phone: '',
				sex: '',
				sexOptions: [{
						label: '男性',
						value: '男'
					},
					{
						label: '女性',
						value: '女'
					}
				]
			};
		},
		methods: {
			async login() {
				this.isReg = false;
				if(this.username == "" || this.password == "") {
					MessageBox.alert("账号密码必须输入");
					return;
				}

				// 异步登录
				var response = await axios.post('/doLoginJSON.html', {
					username: this.username,
					password: this.password
				});

				if(response.success) {
					Toast("登录成功");

					// 将用户存入localStorage
					localStorage.setItem("username", response.data.username);
					localStorage.setItem("userfullname", response.data.userfullname);

					// 跳转路由
					this.$router.replace("/home");
				}
			},
			reg() {
				this.username = '';
				this.password = '';
				this.isReg = true;
			},
			async addUser() {
				if(this.username == '' || this.password == '' || this.userfullname == '' || this.phone == '' || this.sex == '') {
					MessageBox.alert("请检查必填字段!!!");
					return;
				}

				// 异步注册
				var response = await axios.post('/user/addUserJSON.html', {
					username: this.username,
					userfullname: this.userfullname,
					password: this.password,
					phone: this.phone,
					sex: this.sex,
				});

				if(response.success) {
					this.isReg = false;

					Toast("注册成功");
				}
			},
			cancel() {
				this.isReg = false;
			}
		}
	}
	export default login;
</script>
