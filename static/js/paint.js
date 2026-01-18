function clearActive(){
document.querySelectorAll('.color-btn').forEach(btn=> btn.classList.remove('active'));
}
function setColor(id){
fetch(`/set-color/${id}`,{method: 'POST'});
clearActive();
document.querySelector(`.color-btn[data-id="${id}"]`).classList.add('active');
}
function setNone(){
fetch('/set-none',{method: 'POST'});
clearActive();
document.querySelector('.none-btn').classList.add('active');
}
window.onload=()=>{
setNone();
};
