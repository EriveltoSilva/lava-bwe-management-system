
window.addEventListener("load", ()=>{
    getNames()
})



async function getNames()
{
    let word ="r"
    await fetch("/get_users/"+word, {
        method: 'GET', headers: { 'Content-Type': 'application/json','X-CSRFToken': csrftoken},
    })
    .then(resp => resp.json())
    .then(resp => {
        if(resp.status == "success")
        {
            console.log(resp);
            // alert(resp.message)
        }
    })
    .catch((error) => {
        console.error('Erro:', error);
    });
}
