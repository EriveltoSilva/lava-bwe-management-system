let notification = ""
let userId = ""
const btnNotification = document.getElementById("btnNotification")

window.addEventListener("load", ()=>{
    userId = document.getElementById("userId").value 
    btnNotification.addEventListener("click", ()=>{
        getNotifications()
        // showNotifications
        // const modal = new bootstrap.Modal(document.getElementById("notificationModal"));
        // modal.show();
        
    });
})

async function getNotifications()
{
    await fetch("/get_notifications/" + userId, {
        method: 'GET', headers: { 'Content-Type': 'application/json','X-CSRFToken': csrftoken},
    })
    .then(resp => resp.json())
    .then(resp => {
        if (resp.status == "error")
            alert(resp.message)

        else {
            // document.getElementById("date").innerHTML = resp.data.date;
            // document.getElementById("markedBy").innerHTML = resp.data.marked_by;
            // document.getElementById("room").innerHTML = resp.data.room;
            // document.getElementById("status").innerHTML = resp.data.status;
        //     document.getElementById("subject").innerHTML = resp.data.subject;
        //     document.getElementById("timeFinish").innerHTML = resp.data.time_finish;
        //     document.getElementById("timeStart").innerHTML = resp.data.time_start;
        //     document.getElementById("periodo").innerHTML = resp.data.periodo;
        //     document.getElementById("participants").innerHTML = resp.data.participants;
        }
    })
    .catch((error) => {
        console.error('Erro:', error);
    });
}

async function showNotifications(id) {
    console.log(`Notifications:${id}`)
//     await fetch("/get-notifications/" + id, {
//         method: 'GET', headers: { 'Content-Type': 'application/json',/*'X-CSRFToken': csrftoken*/ },
//     })
//         .then(resp => resp.json())
//         .then(resp => {
//             if (resp.status == "error")
//                 alert("Erro processando a resposta!")
//             else {
//                 const modal = new bootstrap.Modal(document.getElementById("detailsModal"));
//                 modal.show();
//                 document.getElementById("date").innerHTML = resp.data.date;
//                 document.getElementById("markedBy").innerHTML = resp.data.marked_by;
//                 document.getElementById("room").innerHTML = resp.data.room;
//                 document.getElementById("status").innerHTML = resp.data.status;
//                 document.getElementById("subject").innerHTML = resp.data.subject;
//                 document.getElementById("timeFinish").innerHTML = resp.data.time_finish;
//                 document.getElementById("timeStart").innerHTML = resp.data.time_start;
//                 document.getElementById("periodo").innerHTML = resp.data.periodo;
//                 document.getElementById("participants").innerHTML = resp.data.participants;
//             }
//         })
//         .catch((error) => {
//             console.error('Erro:', error);
        // });
}


// function showModalEliminate(id) {
//     notification = id
//     const modal = new bootstrap.Modal(document.getElementById("eliminateModal"));
//     modal.show();
// }

// function showModalCancel(id) {
//     notification = id
//     const modal = new bootstrap.Modal(document.getElementById("cancelModal"));
//     modal.show();
// }

// document.getElementById("btnEliminateMeeting").addEventListener("click", () => {
//     window.location.assign("/delete-meeting/" + myMeeting)
// })

// document.getElementById("btnCancelMeeting").addEventListener("click", () => {
//     window.location.assign("/cancel-meeting/" + myMeeting)
// })
