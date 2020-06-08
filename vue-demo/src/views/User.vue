<template>
	<div class="user">
		个人中心。欢迎您: {{getLoginUsername()}}
	</div>
</template>

<script>
	import store from '@/store';

	export default {
		name: 'User',
		store,
		methods: {
			getLoginUsername() {
				console.log(this.$store)
				console.log(this.$store.username)
				var username = localStorage.getItem("username");
				var userfullname = localStorage.getItem("userfullname");
				return userfullname;
			},
		},
	};
</script>