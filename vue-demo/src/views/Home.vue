<template>
	<div class="home">
		<mt-header title="XXX管理系统">
			<router-link to="/" slot="left">
				<mt-button icon="back">back</mt-button>
			</router-link>
			<mt-button icon="more" slot="right"></mt-button>
		</mt-header>

		<router-view/>
		<ul class="footer">
			<router-link class="icons" to="/home/user">个人中心</router-link>
			<router-link class="icons" to="/home/contact">通讯录</router-link>
		</ul>
	</div>
</template>

<script>
	export default {
		name: 'home',
	};
</script>

<style scoped lang="scss">
	li {
		list-style: none;
	}
	
	.footer {
		position: fixed;
		width: 100%;
		height: 60px;
		line-height: 60px;
		left: 0px;
		bottom: 0px;
		display: flex;
		flex-flow: row nowrap;
		justify-content: space-around;
	}
	
	.icons {
		font-size: 16px;
		flex: 1;
		text-align: center;
		border-top: 1px solid #42b983;
	}
	
	a {
		color: #42b983;
		&.active {
			color: #fff;
			background: #42b983;
		}
	}
</style>