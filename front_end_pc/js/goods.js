var vm = new Vue({
    el: '#apps',
    data: {
        recommend_goods: [],
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
                })
        },
		//获取分类商品
        get_category_goods: function () {
           //发送请求
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
