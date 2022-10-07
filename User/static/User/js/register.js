function show(){
    var e=document.querySelector("#id_consultant");
    var c=document.querySelector(".ab");
    console.log(e.checked);
    console.log(c);
    if(e.checked){
        console.log("k")
        c.removeAttribute("hidden")
    }
    else{
        console.log("kl")
        c.hidden=true;
    }
}