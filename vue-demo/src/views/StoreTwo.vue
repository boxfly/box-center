<template>
	<div >
		 <h1> mapState, mapMutations </h1>
		 {{name}}
		 <button @click="setName">setName</button>
		 <hr>
		 <h1>笔记</h1>
		  <br>import { mapState, mapMutations } from 'vuex';
		  <br>mapState 获取值
		  <br>mapMutations 设置值
		  
	</div>
</template>

<script> 
	import { mapState, mapMutations } from 'vuex';
	export default {
		name: 'StoreTwo', 
		data() {
			return {
				isReg: false, 
				 
			};
		},
		computed: mapState({ name: 'username',  }),
		methods:{ ...mapMutations(['setLoginUsername']),
		setName() {
           this.setLoginUsername(this.name.split("").reverse().join(""));
         }
		},
		mounted(){			
            console.log({
				"1.init":">>>>> store Two load", 
				"2.username":this.name
			})
		},
	};
</script>
