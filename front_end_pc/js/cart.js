var vm = new Vue({
    el: '#apps',
    data: {
        host: 'http://127.0.0.1:8000',
        goods_list: [],         // 购物车中的商品
        origin_input: 1,        // 商品数量
    },

    computed: {
        select_all: function() {
            for (let i = 0; i < this.goods_list.length; i++) {
                let goods = this.goods_list[i];
                // 重新计算小计金额, 自动刷新界面显示
                if (!goods.selected) {
                    return false;
                }
            }
            return true;
        },

        // 获取选中的商品的数量
        selected_count: function() {
            let total_count = 0;
            for (let i = 0; i < this.goods_list.length; i++) {
                let goods = this.goods_list[i];
                // 重新计算小计金额, 自动刷新界面显示
                goods.amount = parseFloat(goods.sell_price) * parseInt(goods.count);
                if (goods.selected) {
                    total_count += parseInt(goods.count);
                }
            }
            return total_count;
        },

        // 获取选中的商品的总金额
        selected_amount: function() {
            let total_amount = 0;
            for (let i = 0; i < this.goods_list.length; i++) {
                let goods = this.goods_list[i];
                if (goods.selected) {
                    total_amount += parseFloat(goods.sell_price) * parseInt(goods.count);
                }
            }
            // 金额保存两位有效数字
            return total_amount.toFixed(2);
        },
    },

    mounted: function () {
        this.get_cart_goods();
    },

    methods: {
        // 全选和全不选
        on_select_all: function() {
            let select = !this.select_all;
            for (let i = 0; i < this.goods_list.length; i++) {
                this.goods_list[i].selected = select;
            }
        },

        // 获取购物车商品数据
        get_cart_goods: function () {
            axios.get('127.0.0.1:8000/carts/', {
                headers: {
                    'Authorization': 'JWT ' + this.token
                },
                responseType: 'json',
                withCredentials: true
            })
                .then(response =>{
                    this.goods_list = response.data;
                    //for(var i=0; i<this.cart.length; i++){
                    //this.cart[i].amount = (parseFloat(this.cart[i].price) * this.cart[i].count).toFixed(2);
                //}
                })
                .catch(error =>{
                    console.log(error.response.data);
                })
        },

        // 点击增加购买数量
        on_add: function(index) {
            let goods = this.goods_list[index];
            let count = parseInt(goods.count) + 1;

            this.update_cart_count(goods.id, count, index);
        },

        // 点击减少购买数量
        on_minus: function(index){
            let goods = this.goods_list[index];
            let count = parseInt(goods.count);
            if (count > 1) {
                count--;
                this.update_cart_count(goods.id, count, index);
            }
        },

        // 更新购物车商品购买数量
        on_input: function(index) {
            // 输入的数量不能超过最大库存
            let goods = this.goods_list[index];
            this.update_cart_count(goods.id, goods.count, index);
        },

        // 更新购物车商品数量
        update_cart_count: function(goods_id, count, index) {
            //发送请求
        },

        // 删除购物车中的一个商品
        delete_goods: function(index){
            //发送请求
            axios.delete('127.0.0.1:8000/carts/',{
                data:{
                    // delete 方法通过config的data传递参数
                    sku_id: this.goods[index].id
                },
                headers:{
                    'Authorization': 'JWT ' + this.token
                },
                responseType: 'json',
                withCredentials: true
            })
                .then(response =>{
                    alert('删除购物车成功')
                })
                .catch(error =>{
                    console.log(error.response)
                })
        },

        // 清空购物车
        clearCart: function(index){
            //发送请求
        },
    }
});