<template>
	<div class="store">
		 <h1>store 练习</h1>
		 {{username}}
		 <button @click="setName">setName</button>
		 <hr>
		 <h1>store 常见拆分</h1>
		  <br>store 的4大模块分别分为各大模块或者如下区分
		  <br>model1.js // export default { state:{ },  mutatons:{},actions:{},getters:{} }
		  <br>index.js //  vuex.Store({ modules:{ mod1:mod1, mod2:mod1 }});
	</div>
</template>

<script>
	import store from '@/store';
	export default {
		name: 'Store',
		store,
		data() {
			return {
				isReg: false,
				username: '',
				 
			};
		},
		methods: { 
			setName() { 
				this.username = `${this.$store.getters.getDemoValue}-${Date.now()}`;
				console.log({
							"setName":this.$store._mutations, 
				})
				// this.$store._mutations.setDemoValue[0](this.username )
				this.$store.commit('setDemoValue', this.username );   


			}
		},
		mounted(){			
            console.log({
				"1.init":">>>>> store load",
				"2.store":this.$store, 
				"3.getDemoValue":this.$store.getters.getDemoValue,
			})
			this.username = this.$store.getters.getDemoValue

			//setTimeout(()=>{location.reload()},5000)
		},
	};
</script>
