$(document).ready(function() {

    const api_url = '/update';
    const post_url1 = '/post1';
    const post_url2 = '/post2';
    const post_url3 = '/post3';
    const val1 = document.getElementById("formControlRange");
    const val2 = document.getElementById("formControlRange2");
    const val3 = document.getElementById("formControlRange3");
    const output1 = document.getElementById("out1");
    const output2 = document.getElementById("out2");
    const output3 = document.getElementById("out3");
    const but1 = document.getElementById("but1");
    const but2 = document.getElementById("but2");
    const but3 = document.getElementById("but3");
    const but4 = document.getElementById("but4");

    async function getISS() {
        const response = await fetch(api_url);
        const data = await response.json();
        const { servoval, servo1val, servo2val, photocellval, majuval, pompaval } = data;

        document.getElementById('valueservo').textContent = servoval;
        document.getElementById('valueservo1').textContent = servo1val;
        document.getElementById('valueservo2').textContent = servo2val;
        document.getElementById('valuephotocell').textContent = photocellval;
    };

    async function postVal1() {

        const value1 = val1.value;
        
        output1.textContent = value1;

        req = $.ajax({
            url : post_url1,
            type : 'POST',
            data : { value1 : value1 }
        });
    };

    async function postVal2() {

        const value2 = val2.value;
        
        output2.textContent = value2;

        req = $.ajax({
            url : post_url2,
            type : 'POST',
            data : { value2 : value2 }
        });
    };

    async function postVal3() {

        const value3 = val3.value;
        
        output3.textContent = value3;

        req = $.ajax({
            url : post_url3,
            type : 'POST',
            data : { value3 : value3 }
        });
    };

    async function maju() {

        req = $.ajax({
            url : '/maju',
            type : 'POST',
            data : { maju : 1 }
        });
    };

    async function mundur() {

        req = $.ajax({
            url : '/maju',
            type : 'POST',
            data : { maju : 0 }
        });
    };

    async function pompaon() {

        req = $.ajax({
            url : '/pompa',
            type : 'POST',
            data : { pompa : 1 }
        });
    };

    async function pompaoff() {

        req = $.ajax({
            url : '/pompa',
            type : 'POST',
            data : { pompa : 0 }
        });
    };

    async function setData() {
        const response = await fetch(api_url);
        const data = await response.json();
        const { servoval, servo1val, servo2val, photocellval, majuval, pompaval } = data;
        value1 = servoval;
        value2 = servo1val;
        value3 = servo2val;
        output1.textContent = value1;
        output2.textContent = value2;
        output3.textContent = value3;
        val1.value = value1;
        val2.value = value2;
        val3.value = value3;
        $(".loader-wrapper").fadeOut("slow");

    };

    setData();
    setTimeout(setData, 7000);
    
    getISS();

    setInterval(getISS, 5000);
    
    val1.onchange = function() {
        postVal1();
        getISS();
    };

    val1.oninput = function() {
        output1.textContent = this.value;
    };

    val2.onchange = function() {
        postVal2();
        getISS();
    };

    val2.oninput = function() {
        output2.textContent = this.value;
    };

    val3.onchange = function() {
        postVal3();
        getISS();
    };

    val3.oninput = function() {
        output3.textContent = this.value;
    };

    but1.onclick = function() {
        maju();
    };

    but2.onclick = function() {
        mundur();
    };

    but3.onclick = function() {
        pompaon();
    };

    but4.onclick = function() {
        pompaoff();
    };
});