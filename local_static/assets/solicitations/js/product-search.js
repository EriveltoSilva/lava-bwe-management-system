const inputBox = document.getElementById("productName");
const options = document.querySelector(".my-content-box");
let products = [];

window.addEventListener("load", ()=>{
    getProducts("all");
});

inputBox.addEventListener("keyup", (e) => {
    let userData = e.target.value;
    if (userData)
        getProducts(userData);
    else
        cleanFields();

});

function cleanFields() {
    inputBox.value = "";
    document.getElementById("detail").value = "";
    document.getElementById("center_cost").value = "";
    document.getElementById("price").value = document.getElementById("price").value = "";
    document.getElementById("code").value = "";
    getProducts("all");
}

function select(element) {
    for (let index = 0; index < products.length; index++) {
        if (products[index].name == element.textContent) {
            inputBox.value = products[index].name;
            document.getElementById("detail").value = products[index].detail;
            document.getElementById("code").value = products[index].code;
            document.getElementById("center_cost").value = products[index].center_cost;
            document.getElementById("price").value = products[index].price;
        }
    }
}

async function getProducts(word) {
    await fetch("/solicitations/get-products/" + word, {
        method: 'GET', headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrftoken },
    })
        .then(resp => resp.json())
        .then(resp => {
            if (resp.status == "success") {
                let emptyArray = [];
                products = resp.data;
                products.forEach(element => {
                    emptyArray.push(element.name);
                });
                emptyArray = emptyArray.map((data) => {
                    return data = '<li onclick="select(this)" class="p-2">' + data + '</li>'
                }).join('');
                options.innerHTML = emptyArray ? emptyArray : '<p> Ooops! Pesquisa não encontrada!</p>';
            }
        })
        .catch((error) => {
            console.error('Erro:', error);
        });
}
