let myMeeting = ""

function showModalEliminate(id) {
    myMeeting = id
    const modal = new bootstrap.Modal(document.getElementById("eliminateModal"));
    modal.show();
}

function showModalCancel(id) {
    myMeeting = id
    const modal = new bootstrap.Modal(document.getElementById("cancelModal"));
    modal.show();
}

document.getElementById("btnEliminateMeeting").addEventListener("click", () => {
    window.location.assign("/room-reservation/delete-meeting/" + myMeeting)
})

document.getElementById("btnCancelMeeting").addEventListener("click", () => {
    window.location.assign("/room-reservation/cancel-meeting/" + myMeeting)
})

async function showDetails(id) {
    console.log(`Vendo meeting:${id}`)
    await fetch("/room-reservation/detais_meetings/" + id, {
        method: 'GET', headers: { 'Content-Type': 'application/json',/*'X-CSRFToken': csrftoken*/ },
    })
        .then(resp => resp.json())
        .then(resp => {
            if (resp.status == "error")
                alert("Erro processando a resposta!")
            else {
                const modal = new bootstrap.Modal(document.getElementById("detailsModal"));
                modal.show();
                document.getElementById("date").innerHTML = resp.data.date;
                document.getElementById("markedBy").innerHTML = resp.data.marked_by;
                document.getElementById("room").innerHTML = resp.data.room;
                document.getElementById("status").innerHTML = resp.data.status;
                document.getElementById("subject").innerHTML = resp.data.subject;
                document.getElementById("timeFinish").innerHTML = resp.data.time_finish;
                document.getElementById("timeStart").innerHTML = resp.data.time_start;
                document.getElementById("periodo").innerHTML = resp.data.periodo;
                document.getElementById("participants").innerHTML = resp.data.participants;

            }
        })
        .catch((error) => {
            console.error('Erro:', error);
        });
}