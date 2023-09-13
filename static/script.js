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

function showStep() {
    if (step1.style.display === "none") {
        step1.style.display = "block";
    }
    else {
        step1.style.display = "none";
    }
}