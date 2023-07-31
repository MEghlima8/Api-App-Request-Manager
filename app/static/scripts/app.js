var app_methods = {};

app_methods.change_panel = function(panel,admin_panel){
    // add-calc
    this.CalcNum1= '',
    this.CalcNum2= '',

    // steg newreq audio
    this.msg_newreq_audio= '',
    this.audio_newreq_audio = '',

    // steg-newreq-img
    this.msg_steg_newreq_img='',
    this.img_steg_new_req_img= '',
    
    // extract steg image 
    this.extr_steg_img='',

    // extract new req audio
    this.extr_steg_audio='',

    //  SignIn Info
    this.username= '',
    this.password= '',
    //  SignUp Info
    this.email='',

    this.progress= 0

    this.panel = panel;
    this.admin_panel = admin_panel
}


//  Admin

// Get admin dashboard info
app_methods.getAdminDashboardInfo = function(){
    var data = {
        'username':this.username,
        'password':this.password,
    }

    axios.post('/signin', data).then(response => {  
        if (response.data['status-code'] == 200) { 
            this.processing_requests = response.data["result"]["processing"]  // count of processing
            this.inQueue_requests = response.data["result"]["in queue"]     // count of queue
            this.completed_requests = response.data["result"]["done"]   // count of done
            this.all_requests = response.data["result"]["done"] + response.data["result"]["in queue"] + response.data["result"]["processing"]
            
            this.all_add_requests = response.data["result"]["all_add_reqs"]
            this.all_audio_requests = response.data["result"]["all_audio_steg_reqs"]
            this.all_img_requests = response.data["result"]["all_img_steg_reqs"]
            this.change_panel('admin','admin-dashboard')
        }})
};


app_methods.admin_resAddCalc = function(){
    axios.post('/admin-res-add-calc').then(response => {          
        this.res_queue = response.data["result"]["queue"]
        this.res_processing = response.data["result"]["processing"]
        this.res_done = response.data["result"]["done"]  
    })
    this.change_panel('admin','admin-res-add-calc');
};

app_methods.admin_resStegImg = function(){
    axios.post('/admin-res-steg-img').then(response => {          
        this.res_queue = response.data["result"]["queue"]
        this.res_processing = response.data["result"]["processing"]
        this.res_done = response.data["result"]["done"]  
    })
    this.change_panel('admin','admin-res-steg-img');
};

app_methods.admin_resExtrStegImg = function(){
    axios.post('/admin-res-extr-steg-img').then(response => {          
        this.res_queue = response.data["result"]["queue"]
        this.res_processing = response.data["result"]["processing"]
        this.res_done = response.data["result"]["done"]  
    })
    this.change_panel('admin','admin-res-extr-steg-img');
};

app_methods.admin_resStegAudio = function(){
    axios.post('/admin-res-steg-audio').then(response => {          
        this.res_queue = response.data["result"]["queue"]
        this.res_processing = response.data["result"]["processing"]
        this.res_done = response.data["result"]["done"]  
    })
    this.change_panel('admin','admin-res-steg-audio');
};

app_methods.admin_resExtrStegAudio = function(){
    axios.post('/admin-res-extr-audio').then(response => {          
        this.res_queue = response.data["result"]["queue"]
        this.res_processing = response.data["result"]["processing"]
        this.res_done = response.data["result"]["done"]  
    })
    this.change_panel('admin','admin-res-extr-audio');
};

// for all users
app_methods.admin_usersInfo = function(){
    axios.post('/admin-users-info').then(response => {
        this.users_info = response.data["result"]
        for (let i = 0; i < this.users_info.length; i++) {
            if (this.users_info[i][3] === true) {
                this.users_info[i][3] = 'فعال';
            } else {
                this.users_info[i][3] = 'غیر فعال';
            }
          }
    })
    this.change_panel('admin','admin-users-info');
};
// # Admin



// Signin
app_methods.signIn = function(){
    var data = {
        'username':this.username,
        'password':this.password,
    }
    if (this.username =='admin' && this.password == 'admin'){
        this.getAdminDashboardInfo();
        return;
    }
    axios.post('/signin', data).then(response => {  
        // Admin logged in
        
        if (response.data['status-code'] == 200) { 
            this.goToDashboard();
        }        
        else {            
            //  Login was not succesful
            if (response.data['status-code'] == 400){Swal.fire({title:'خطا' ,text:'نام کاربری یا رمز عبور اشتباه است', icon:'error', confirmButtonText:'تایید'})}
            else if (response.data['status-code'] == 403){Swal.fire({title:'ایمیل تایید نشده است' ,text:'این ایمیل هنوز تایید نشده است.برای تایید به ایمیل خود بروید و روی لینک تایید کلیک کنید', icon:'warning', confirmButtonText:'تایید'})}
            this.panel = 'sign-in'
        }
    })
};

// Signup
app_methods.signUp = function(){
    var data = {
        'username' : this.username,
        'password' : this.password,
        'email' : this.email,
    }    
    axios.post('/signup', data).then(response => {  
        if (response.data['status-code'] == 201) { 
            //  Signup was succesful
            Swal.fire({title:'تایید ثبت نام' ,text:'ثبت نام با موفقیت انجام شد. لینک تایید به ایمیل شما ارسال شد', icon:'success', confirmButtonText:'تایید'})
            this.change_panel('sign-in',null)
            this.username= '',
            this.password= ''
        }        
        else if (response.data['result'] == 'duplicate_email') {Swal.fire({title:'خطا' ,text:'ایمیل وارد شده در سیستم وجود دارد', icon:'error', confirmButtonText:'تایید'})}
        else if (response.data['result'] == 'email_length') {Swal.fire({title:'خطا' ,text:'طول ایمیل نمی تواند بیشتر از 320 کاراکتر باشد', icon:'error', confirmButtonText:'تایید'})}
        else if (response.data['result'] == 'noactive') {Swal.fire({title:'خطا' ,text:'ایمیل تایید برای شما ارسال شده است. لطفا بر روی لینک ارسال شده به ایمیل تان بزنید', icon:'warning', confirmButtonText:'تایید'})}
        else if (response.data['result'] == 'empty_email') {Swal.fire({title:'خطا' ,text:'لطفا ایمیل خود را وارد کنید', icon:'error', confirmButtonText:'تایید'})}
        else if (response.data['result'] == 'char_email') {Swal.fire({title:'خطا' ,text:'ایمیل وارد شده صحیح نیست', icon:'error', confirmButtonText:'تایید'})}
        
        else if (response.data['result'] == 'password_length') {Swal.fire({title:'خطا' ,text:'طول رمز عبور باید بیشتر از 8 حرف و حداقل شامل یک حرف کوچک و یک حرف بزرگ و یک کاراکتر خاص و یک عدد باشد', icon:'error', confirmButtonText:'تایید'})}
        else if (response.data['result'] == 'char_password') {Swal.fire({title:'خطا' ,text:'طول رمز عبور باید بیشتر از 8 حرف و حداقل شامل یک حرف کوچک و یک حرف بزرگ و یک کاراکتر خاص و یک عدد باشد', icon:'error', confirmButtonText:'تایید'})}
        else if (response.data['result'] == 'empty_password') {Swal.fire({title:'خطا' ,text:'لطفا یک رمز عبور برای خودتان انتخاب کنید', icon:'error', confirmButtonText:'تایید'})}
        else if (response.data['result'] == 'used_info_in_password') {Swal.fire({title:'خطا' ,text:'رمز عبور شما مطابقت زیادی با ایمیل یا نام کاربری تان دارد. لطفا رمز عبور دیگری را انتخاب کنید', icon:'error', confirmButtonText:'تایید'})}
        
        else if (response.data['result'] == 'duplicate_username' ) {Swal.fire({title:'خطا' ,text:'نام کاربری وارد شده از قبل در سیستم وجود دارد. لطفا نام کاربری دیگری را انتخاب کنید', icon:'error', confirmButtonText:'تایید'})}
        else if (response.data['result'] == 'length_username') {Swal.fire({title:'خطا' ,text:'طول نام کاربری شما باید بین 3 تا 30 کاراکتر باشد', icon:'error', confirmButtonText:'تایید'})}
        else if (response.data['result'] == 'char_username') {Swal.fire({title:'خطا' ,text:'نام کاربری فقط می تواند شامل حروف کوچک و بزرگ انگلیسی و اعداد و نقطه و زیرخط(آندرلاین) باشد', icon:'error', confirmButtonText:'تایید'})}
        else if (response.data['result'] == 'empty_username') {Swal.fire({title:'خطا' ,text:'لطفا یک نام کاربری برای خودتان انتخاب کنید', icon:'error', confirmButtonText:'تایید'})}
        else{ Swal.fire({title:'خطا' ,text:'خطای نامشخص', icon:'error', confirmButtonText:'تایید'}) }
    })
};


// Go to dashboard
app_methods.goToDashboard = function(){
    axios.post('/res-add-calc').then(response => {this.all_add_requests = response.data["count"]})        
    axios.post('/get-all-audio-steg-req').then(response => {this.all_audio_requests = response.data["count"]})
    axios.post('/get-all-img-steg-req').then(response => {this.all_img_requests = response.data["count"]})
    
    axios.post('/get-user-requests-status').then(response => {
        this.processing_requests = response.data["processing"]  // count of processing
        this.inQueue_requests = response.data["in queue"]     // count of queue
        this.completed_requests = response.data["done"]   // count of done
        this.all_requests = response.data["done"] + response.data["in queue"] + response.data["processing"]
    })
    this.panel= 'dashboard';

};


// Add calc
app_methods.resAddCalc = function(){
    const done = [];
    axios.post('/get-all-add-req').then(response => {  
        this.res_queue = response.data["queue"]
        this.res_processing = response.data["processing"]
        for (let i = 0; i < response.data["done"].length; i++) {
            if (response.data["done"][i][3]["result"] == 'request id is wrong'){
                this.res_queue.push(response.data["done"][i]);
            }
            else { done.push(response.data["done"][i]) }
          }
        this.res_done = done;
    })
    this.change_panel('res-add-calc',null);
};

app_methods.sendAddCalcReq = function(){
    data = {
        "params": {
            "num1": parseInt(this.CalcNum1),
            "num2": parseInt(this.CalcNum2)
        }
    }
    
    if (typeof data["params"]["num2"] !== 'number' || typeof data["params"]["num2"] !== 'number' || isNaN(data["params"]["num1"]) || isNaN(data["params"]["num2"]) || data["params"]["num1"] === '' || data["params"]["num2"] === '') {
        Swal.fire({title:'اطلاعات نامعتبر' ,text:'مقادیر وارد شده باید عدد باشند و نباید خالی باشند.', icon:'warning', confirmButtonText:'تایید'})
      }
    else {
        axios.post('/add-two-numbers', data).then(response => { 
            Swal.fire({title:'تایید درخواست' ,text:'درخواست شما با موفقیت تایید شد', icon:'success', confirmButtonText:'تایید'})
        })}
        this.resAddCalc();
};
// # Add calc



//  steg image 
app_methods.resStegImg = function(){
    const done = [];
    axios.post('/get-all-img-res').then(response => { 
        this.res_queue = response.data["queue"]
        this.res_processing = response.data["processing"]
        for (let i = 0; i < response.data["done"].length; i++) {
            if (response.data["done"][i][3]["result"] == 'request id is wrong'){
                this.res_queue.push(response.data["done"][i]);
            }
            else { done.push(response.data["done"][i]) }
          }
        this.res_done = done;
        this.change_panel('res-steg-img', null)
    })
};

app_methods.handleStegNewReqImg = function(event){
    this.img_steg_new_req_img = event.target.files[0]
};

app_methods.stegNewReqImg = function(){
    
    if (this.msg_steg_newreq_img === '' || this.img_steg_new_req_img === '') {
        Swal.fire({title:'اطلاعات نامعتبر' ,text:'لطفاً مقادیر را پر کنید و یا فایل را آپلود کنید.', icon:'warning', confirmButtonText:'تایید'})
        return ;
    }
    if (this.img_steg_new_req_img.type.startsWith('image/')) {
        const fd = new FormData();
        fd.append('img_steg_new_req_img',this.img_steg_new_req_img)
        fd.append('msg_steg_newreq_img', this.msg_steg_newreq_img)

        axios.post('/hide-text-in-image', fd, {
            headers: {
                'Content-Type': 'multipart/form-data'
            },
            onUploadProgress: (progressEvent) => {
              this.progress = Math.round((progressEvent.loaded * 100) / progressEvent.total);
              this.message = `آپلود: ${this.progress}%`;
            }
          })
        .then(response => {
            this.progress = 100;
            Swal.fire({title:'تایید درخواست' ,text:'درخواست شما با موفقیت تایید شد', icon:'success', confirmButtonText:'تایید'})
            this.message = 'آپلود با موفقیت انجام شد';
            this.resStegImg();
          })
        .catch(error => {
            this.message = 'خطا در آپلود تصویر';
          });

    }
    else {Swal.fire({title:'فرمت فایل نامعتبر' ,text:'فرمت فایل آپلود شده معتبر نمی باشد', icon:'warning', confirmButtonText:'تایید'})}
};
// # steg image 


// Extract steg image
app_methods.resExtrStegImg = function(){
    const done = [];
    axios.post('/res-extr-steg-img').then(response => { 
        this.res_queue = response.data["queue"]
        this.res_processing = response.data["processing"]
        for (let i = 0; i < response.data["done"].length; i++) {
            if (response.data["done"][i][3]["result"] == 'request id is wrong'){
                this.res_queue.push(response.data["done"][i]);
            }
            else { done.push(response.data["done"][i]) }
          }
        this.res_done = done;
        this.change_panel('res-extr-steg-img', null)
    })
};

app_methods.handleExtrStegNewImg = function(event){
    this.extr_steg_img = event.target.files[0]
};

app_methods.extrStegImg = function(){
    if (this.extr_steg_img === '' ) {
        Swal.fire({title:'نامعتبر' ,text:'لطفاً فایل را آپلود کنید.', icon:'warning', confirmButtonText:'تایید'})
        return ;
    }
    if (this.extr_steg_img.type.startsWith('image/')) {
        const fd = new FormData();
        fd.append('extr_steg_img',this.extr_steg_img)
    
        axios.post('/get-hidden-text-from-image', fd, {
            headers: {
                'Content-Type': 'multipart/form-data'
            },
            onUploadProgress: (progressEvent) => {
              this.progress = Math.round((progressEvent.loaded * 100) / progressEvent.total);
              this.message = `آپلود: ${this.progress}%`;
            }
          })
        .then(response => {
            this.progress = 100;
            Swal.fire({title:'تایید درخواست' ,text:'درخواست شما با موفقیت تایید شد', icon:'success', confirmButtonText:'تایید'})
            this.message = 'آپلود با موفقیت انجام شد';
            this.resExtrStegImg();
          })
        .catch(error => {
            this.message = 'خطا در آپلود تصویر';
          });

    }
    else {Swal.fire({title:'فرمت فایل نامعتبر' ,text:'فرمت فایل آپلود شده معتبر نمی باشد', icon:'warning', confirmButtonText:'تایید'})}
};
// # Extract steg image



// # Steg audio
app_methods.resStegAudio = function(){
    const done = [];
    axios.post('/res-steg-audio').then(response => {          
        this.res_queue = response.data["queue"]
        this.res_processing = response.data["processing"]
        for (let i = 0; i < response.data["done"].length; i++) {
            if (response.data["done"][i][3]["result"] == 'request id is wrong'){
                this.res_queue.push(response.data["done"][i]);
            }
            else { done.push(response.data["done"][i]) }
          }
        this.res_done = done;
        this.change_panel('res-steg-audio', null)
    })
};

app_methods.handleNewReqAudio = function(event){
    this.audio_newreq_audio = event.target.files[0]
};

app_methods.steg_new_req_audio = function(){
    if (this.audio_newreq_audio === '' || this.msg_newreq_audio === '') {
        Swal.fire({title:'اطلاعات نامعتبر' ,text:'لطفاً مقادیر را پر کنید و فایل را آپلود کنید', icon:'warning', confirmButtonText:'تایید'})
        return;
    }
    if (this.audio_newreq_audio.type.startsWith('audio/')) {
        const fd = new FormData();
        fd.append('msg_newreq_audio',this.msg_newreq_audio)
        fd.append('audio_newreq_audio',this.audio_newreq_audio)
        axios.post('/hide-text-in-sound', fd, {
            headers: {
                'Content-Type': 'multipart/form-data'
            },
            onUploadProgress: (progressEvent) => {
              this.progress = Math.round((progressEvent.loaded * 100) / progressEvent.total);
              this.message = `آپلود: ${this.progress}%`;
            }
          })
        .then(response => {
            this.progress = 100;
            Swal.fire({title:'تایید درخواست' ,text:'درخواست شما با موفقیت تایید شد', icon:'success', confirmButtonText:'تایید'})
            this.message = 'آپلود با موفقیت انجام شد';
            this.resStegAudio();
          })
        .catch(error => {
            this.message = 'خطا در آپلود تصویر';
          });

    }
    else {Swal.fire({title:'فرمت فایل نامعتبر' ,text:'فرمت فایل آپلود شده معتبر نمی باشد', icon:'warning', confirmButtonText:'تایید'})}
};
// # Steg audio


// Extract steg audio
app_methods.handleExtrNewAudio = function(event){
    this.extr_steg_audio = event.target.files[0]    
};

app_methods.extrNewReqAudio = function(){

    if (this.extr_steg_audio === '' ) {
        Swal.fire({title:'نامعتبر' ,text:'لطفا یک فایل را آپلود کنید', icon:'warning', confirmButtonText:'تایید'})
        return ;
    }
    if (this.extr_steg_audio.type.startsWith('audio/')) {
        const fd = new FormData();
        fd.append('extr_steg_audio',this.extr_steg_audio)
        axios.post('/get-hidden-text-from-sound', fd, {
            headers: {
                'Content-Type': 'multipart/form-data'
            },
            onUploadProgress: (progressEvent) => {
              this.progress = Math.round((progressEvent.loaded * 100) / progressEvent.total);
              this.message = `آپلود: ${this.progress}%`;
            }
        })
        .then(response => {
            this.progress = 100;
            Swal.fire({title:'تایید درخواست' ,text:'درخواست شما با موفقیت تایید شد', icon:'success', confirmButtonText:'تایید'})
            this.message = 'آپلود با موفقیت انجام شد';
            this.resExtrStegAudio();
          })
        .catch(error => {
            this.message = 'خطا در آپلود تصویر';
          });

    }
    else {Swal.fire({title:'فرمت فایل نامعتبر' ,text:'فرمت فایل آپلود شده معتبر نمی باشد', icon:'warning', confirmButtonText:'تایید'})}

};

app_methods.resExtrStegAudio = function(){
    const done = [];
    axios.post('/res-extr-steg-audio').then(response => {          
        this.res_queue = response.data["queue"]
        this.res_processing = response.data["processing"]
        for (let i = 0; i < response.data["done"].length; i++) {
            if (response.data["done"][i][3]["result"] == 'request id is wrong'){
                this.res_queue.push(response.data["done"][i]);
            }
            else { done.push(response.data["done"][i]) }
          }
        this.res_done = done;
        this.change_panel('res-extr-audio', null)
    })
};
// # Extract steg audio



Vue.createApp({

    data(){ return {
        
        panel: 'sign-in',
        admin_panel: '',

        // admin
        users_info:'' ,
        
        // add-calc
        CalcNum1: '',
        CalcNum2: '',

        // steg newreq audio
        msg_newreq_audio: '',
        audio_newreq_audio : '',

        // steg-newreq-img
        msg_steg_newreq_img:'',
        img_steg_new_req_img: '',

        // extract steg image 
        extr_steg_img:'',

        // extract new req audio
        extr_steg_audio:'',

        //  SignIn Info
        username: '',
        password: '',
        //  SignUp Info
        email:'',

        // result for all pages
        res_done: '',
        res_processing : '',
        res_queue: '',

        // Dashboard info
        all_requests: 0,
        completed_requests: 0 ,
        processing_requests: 0 ,
        inQueue_requests : 0,
        all_add_requests: 0,
        all_audio_requests: 0,
        all_img_requests: 0,

        // progress bar
        progress: 0,
    } },
    
    delimiters: ["${", "}$"],    
    methods:app_methods,
    
}).mount('#app')