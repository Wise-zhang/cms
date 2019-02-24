var vm = new Vue({
    el: '#loginform',
    data: {
        host: 'http://127.0.0.1:8000',
        username: '',
        password: '',
        remember: false,

        error_username: false,
        error_pwd: false,

        error_msg: '',    // 提示信息
    },

    methods: {
        // 检查数据
        check_username: function(){
            if (!this.username) {
                this.error_username = true;
                this.error_msg = '请填写用户名';
            } else {
                this.error_username = false;
                this.error_msg = '';
            }
        },
        check_pwd: function(){
            if (!this.password) {
                this.error_msg = '请填写密码';
                this.error_pwd = true;
            } else {
                this.error_pwd = false;
                this.error_msg = '';
            }
        },

        // 表单提交
        on_submit: function(){
            this.check_username();
            this.check_pwd();

            if (this.error_username === false
                && this.error_pwd === false) {
				//发送登录请求
            }
        },
    }
});