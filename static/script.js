function myFunction() {
    var click = document.getElementById("click");
    var moreText = document.getElementById("more");
    var btnText = document.getElementById("myBtn");

    if (click.style.display === "none") {
        click.style.display = "block";
        btnText.innerHTML = "Read more";
        moreText.style.display = "none";
    } else {
        click.style.display = "none";
        btnText.innerHTML = "Read less";
        moreText.style.display = "inline";
    }
}

function showStep1() {
    let step1 = document.getElementById("step1-more");
    let dots1 = document.getElementById("dots1");
    if (dots1.style.display === "none") {
        dots1.style.display = "block";
        step1.style.display = "none";
    }
    else {
        dots1.style.display = "none";
        step1.style.display = "block";
    }
}

function showStep2() {
    let step2 = document.getElementById("step2-more");
    let dots2 = document.getElementById("dots2");
    if (dots2.style.display === "none") {
        dots2.style.display = "block";
        step2.style.display = "none";
    }
    else {
        dots2.style.display = "none";
        step2.style.display = "block";
    }
}

function showStep3() {
    let step3 = document.getElementById("step3-more");
    let dots3 = document.getElementById("dots3");
    if (dots3.style.display === "none") {
        dots3.style.display = "block";
        step3.style.display = "none";
    }
    else {
        dots3.style.display = "none";
        step3.style.display = "block";
    }
}



