let myMeeting = "";

function showModalEliminate(id) {
    myMeeting = id;
    const modal = new bootstrap.Modal(
        document.getElementById("eliminateModal")
    );
    modal.show();
}

async function showDetails(slug) {
    await fetch("/maquinas/detalhes/" + slug, {
        method: "GET",
        headers: {
            "Content-Type": "application/json" /*'X-CSRFToken': csrftoken*/,
        },
    })
        .then((resp) => resp.json())
        .then((resp) => {
            if (resp.status == "error") alert("Erro processando a resposta!");
            else {
                const modal = new bootstrap.Modal(
                    document.getElementById("detailsModal")
                );
                modal.show();
                document.getElementById("name").innerHTML = resp.data.name;
                document.getElementById("description").innerHTML =
                    resp.data.description;
                document.getElementById("purchase_value").innerHTML =
                    resp.data.purchase_value;
                document.getElementById("state").innerHTML = resp.data.state;
                document.getElementById("created_by").innerHTML =
                    resp.data.created_by;
                document.getElementById("created_at").innerHTML =
                    resp.data.created_at;
                document.getElementById("updated_at").innerHTML =
                    resp.data.updated_at;
            }
        })
        .catch((error) => {
            console.error("Erro:", error);
        });
}
