const btnAddItens   = document.getElementById("btnAddItens")
const fieldMaterialName = document.getElementById("material_name")
const fieldDetail   = document.getElementById("detail")
const fieldQuantity = document.getElementById("quantity")
const fieldCenterCost = document.getElementById("center_cost")
const fieldApproximatedValue  = document.getElementById("approximated_value")
let items = []

let btnSave = document.getElementById("btnSave")


btnAddItens.addEventListener("click", ()=>{
    const fatherElement = document.getElementById("tbody")
    let row = `
        <tr>
            <th scope="row">${fieldMaterialName.value}</th>
            <td>${fieldDetail.value}</td>
            <td>${fieldQuantity.value}</td>
            <td>${fieldCenterCost.value}</td>
            <td>${fieldApproximatedValue.value}</td>
        </tr>
    ` 
    let resp = isValid()
    if(resp ==""){
        items.push({"material_name":fieldMaterialName.value, "detail":fieldDetail.value,"quantity":fieldQuantity.value, "center_cost":fieldCenterCost.value,"approximated_value":fieldApproximatedValue.value })
        fatherElement.insertAdjacentHTML("beforeend", row)
        cleanFields()
        console.log(items);
        document.getElementById("numItems").innerHTML=items.length
        let som=total=0
        items.forEach(element => {
            som +=  parseInt(element.quantity)
            total += parseInt(element.quantity)*parseFloat(element.approximated_value)
        });
        document.getElementById("quantMaterial").innerHTML = som+"unid"
        document.getElementById("totalMaterial").innerHTML = total+"KZ"
        
    }
    else
    {
        alert(resp)
    }
})


function isValid() {
    if(fieldMaterialName.value=="")
        return "Campo Material Não Selecionado"
    else if (fieldQuantity.value=="")
        return "Campo Quantidade Vazio"
    else if (fieldCenterCost.value=="")
        return "Campo Custo de Centro Vazio"
    else if (fieldApproximatedValue.value=="")
        return "Campo Valor Aproximado Vazio"
    return ""
}

function cleanFields() {
    fieldMaterialName.value="";
    fieldDetail.value="";
    fieldQuantity.value="";
    fieldCenterCost.value="";
    fieldApproximatedValue.value="";
}

btnSave.addEventListener("click", ()=>{saveData()})


async function saveData() {
    const url = "/solicitations/new-material-requisition/";
    await fetch(url,  {
        method: 'POST', 
        headers: { 
            'Content-Type': 'application/json',
            'X-CSRFToken':getToken('csrftoken')
        },
        body: JSON.stringify(items)
    })
        .then(resp => resp.json())
        .then(resp => {
            if(resp.status =="success"){
                Swal.fire({
                    title: "Sucesso!",
                    text: resp.message,
                    icon: resp.status,
                    showConfirmButton: false,
                    footer: `<a class="btn btn-success" href="${resp.url}">Ok</a>`,
                });
                setTimeout(() => {
                    window.location.assign(resp.url)
                }, 4000);
            }
            else
            {
                Swal.fire({
                    title: "Erro!",
                    text: resp.message,
                    icon: resp.status,
                });
            }
            
        })
        .catch((error) => {
            console.error('Erro:', error);
        });
}

function getToken(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
