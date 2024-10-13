

function showModal(modalId) {
    const modal = new bootstrap.Modal(document.getElementById(modalId));
    modal.show();
}

function hideModal(modalId) {
    const modal = new bootstrap.Modal(document.getElementById(modalId));
    modal.hide();
}