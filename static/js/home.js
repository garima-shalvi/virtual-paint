const mess="Welcome to Virtual Paint";
const btn = document.getElementById("btn");
let index=0;
const speed=100;
function typeEffect(){
if(index<mess.length){
document.getElementById("text").textContent += mess.charAt(index);
index++;
setTimeout(typeEffect,speed);}
else{
btn.classList.add("show");}

}
typeEffect();