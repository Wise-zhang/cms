var vm = new Vue({
    el: '#app',
    data: {
        host: 'http://127.0.0.1:8000',
        goods: null,
        recommend_goods: null,
        token : sessionStorage.token || localStorage.token,

        count: 1,            // 添加到购物车的商品数量
        goods_id: 0,         // 当前显示的商品id

        category: null,
    },

    mounted: function() {
        this.goods_id = get_query_string('id');
        this.get_goods_detail(this.goods_id);
        this.get_recommend_goods();
    },

    methods:{
        // 判断用户是否已经登录
        is_login: function() {
            var token = sessionStorage.token || localStorage.token;
            return token !== undefined
        },

        // 获取商品详情数据
        get_goods_detail: function(id) {
			//发送请求
            axios.get('http://127.0.0.1:8000/goods/' + id + '/detail/')
                .then(response => {
                    this.goods = response.data;
                })
                .catch(function (error) {
                    console.log(error.response)
                });

            // 面包屑导航请求
            axios.get("http://127.0.0.1:8000/goods/detail/nav/" + id)
                    .then(function (response) {
                        console.log(response.data);
                        vm.category = response.data
                    })
                    .catch(function (error) {
                        console.log(error.response)
                    })
        },

        // 获取推荐商品
        get_recommend_goods: function () {
			//发送请求
            axios.get('http://127.0.0.1:8000/goods/detail/recommendation')
                .then(response => {
                    this.recommend_goods = response.data;
                })
                .catch(function (error) {
                    console.log(error.response)
                });


        },

        addToCart: function() {
            // 添加商品到购物车
            if (this.is_login()) {  // 已经登录
                //发送登录请求   这里末尾必须加/，post请求不会补全url
                axios.post('http://127.0.0.1:8000/carts/',{
                    sku_id: parseInt(this.goods_id),
                    count: this.count,
                },{
                    headers: {
                        'Authorization': 'JWT ' + this.token
                    },
                    responseType: 'json',
                    withCredentials: true
                })
                    .then(response =>{
                    alert('添加购物车成功');
                   // this.cart_total_count += response.data.count;
                        })
                    .catch(function(error){
                        console.log(error.response)
                    });





            } else {
                // 如果没有登录,跳转到登录界面,引导用户登录
                window.location.href = 'login.html'
            }
        },

        on_increment: function(){
            // 点击增加购买数量
            this.count ++
        },

        on_decrement: function(){
            // 点击减少购买数量
            if (this.count > 1) {
                this.count--;
            }
        },
    },

    filters: {
        formatDate: function (time) {
            return dateFormat(time, "yyyy-mm-dd");
        },

        formatDate2: function (time) {
            return dateFormat(time, "yyyy-mm-dd HH:MM:ss");
        },
    },
});