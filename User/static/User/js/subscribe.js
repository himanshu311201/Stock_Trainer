console.log("hrl")


function mouseOn(e){
    
    let r=e
    console.log(e.children)
    r.children[1].classList.remove("content-hide")
    console.log(r)
}

function mouseOff(e){
    let r=e
    console.log(e.children)
    r.children[1].classList.add("content-hide")
    console.log(r)
}
