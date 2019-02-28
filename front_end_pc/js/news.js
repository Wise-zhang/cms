var vm = new Vue({
    el: '#app',
    data: {
        messages: [1, 2, 3],
        slide_news: [],
        top_news: [],
        image_news: [],
        categories: []
    },

    mounted: function () {
        this.init_top_news();
        this.init_category_news();
    },

    methods: {
        // 初始化显示顶部的新闻数据
        init_top_news: function () {
            axios.get("http://127.0.0.1:8000/news/top/")
                .then(response => {
                    this.slide_news = response.data.slide_news;
                    this.top_news = response.data.top_news;
                    this.image_news = response.data.image_news;
                    console.log(this.slide_news);
                    console.log(this.top_news);
                    console.log(this.image_news);
                })
                .catch(error => {
                    console.log(error.response)
                })
        },

        // 初始化显示类别新闻数据
        init_category_news: function () {

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

    // 数据发生改变并渲染刷新完成后调用
    updated: function () {
        // 界面刷新后开始轮播
        $("#focus-box").flexslider({
            directionNav: false,
            pauseOnAction: false
        });
    }
});
