const searchWrapper = document.querySelector(".my-search-input");
const inputBox = document.getElementById("searchName");
const suggBox = document.querySelector(".autocom-box");

// if user press any key and release
inputBox.addEventListener("keyup", (e) => {
    let userData = e.target.value;
    if (userData) 
        getNames(userData);
    else 
        searchWrapper.classList.remove("active");
    
});

function select(element) {
    inputBox.value = element.textContent;
    searchWrapper.classList.remove("active");
}

function showSuggestions(list) {
    suggBox.innerHTML = (!list.length) ? '<li>' + inputBox.value + '</li>' : list.join('');
}

function makeSearch() {
    if (inputBox.value)
        window.open("https://www.google.com/search?q=" + inputBox.value, "SingleSecondaryWindowName")
    inputBox.value = ""
}

async function getNames(word) {
    await fetch("/get_users/" + word, {
        method: 'GET', headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrftoken },
    })
        .then(resp => resp.json())
        .then(resp => {
            if (resp.status == "success") {
                let emptyArray = resp.data;

                emptyArray = emptyArray.map((data) => {
                    return data = '<li>' + data + '</li>';
                });
                
                searchWrapper.classList.add("active");
                showSuggestions(emptyArray);
                suggBox.querySelectorAll("li").forEach(element => {
                    element.setAttribute("onclick", "select(this)");
                });
            }
        })
        .catch((error) => {
            console.error('Erro:', error);
        });
}