var vm = new Vue({
    el: '#app',
    data: {
        top_goods: [],
        categories: [],
    },

    mounted: function () {
        this.get_recommend_goods();
        this.get_category_goods();
    },

    methods: {
		//获取推荐商品
        get_recommend_goods: function () {
           //发送请求
            axios.get('http://127.0.0.1:8000/goods/top/')
                .then(response => {
                    this.top_goods = response.data;
                })
                .catch(function (error) {
                    console.log(error.response)
                })
        },
		//获取分类商品
        get_category_goods: function () {
           //发送请求
            axios.get('http://127.0.0.1:8000/goods/sub/')
                .then(response => {
                    this.categories = response.data;
                })
                .catch(function (error) {
                    console.log(error.response)
                })
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
