const selectBtn = document.getElementById("productName");

const searchBox = document.querySelector(".my-search-box");
const contentBox = document.querySelector(".my-content-box");

const options = document.querySelector(".options");
const textSpan = document.querySelector("#textSpan")
const searchInput = document.getElementById("searchCountry");
const realField = document.getElementById("realField");


// function addCountry(selectedCountry) {
//     options.innerHTML="";
//     countries.forEach(country =>{
//         let isSelected = country == selectedCountry ? "selected" : "";
//         let li = `<li onclick="updateName(this)" class="${isSelected}">${country}</li>`;
//         options.insertAdjacentHTML("beforeend", li);
//     });
// }

// function updateName(selectedLi) {
    
//     searchInput.value =  "";
//     addCountry(selectedLi.innerText);
//     textSpan.innerHTML = selectedLi.innerText;
//     realField.value = selectedLi.innerText;
//     contentBox.classList.remove("active");
//     console.log(realField.value);
// }
// addCountry();


// searchInput.addEventListener("keyup", (e)=>{
//     let arr = [];
//     let searchedVal = e.target.value;
    
//     arr = countries.filter(data =>{
//         return data.toLowerCase().includes(searchedVal.toLowerCase());
//     });

//     arr = arr.map((data)=>{
//         return data= '<li onclick="updateName(this)">'+data+'</li>'
//     }).join('');
//     options.innerHTML = arr ? arr : '<p> Ooops! Pesquisa não encontrada!</p>';
// });

selectBtn.addEventListener("click", ()=>{
    searchBox.classList.toggle("active");
    console.log("sad");
});