document.addEventListener('DOMContentLoaded', () => {
    const socket = io();

    // // Configurar drag and drop
    // ['todo', 'doing', 'done'].forEach(colId => {
    //     new Sortable(document.getElementById(colId), {
    //         group: 'kanban',
    //         animation: 150,
    //         onEnd: (evt) => {
    //             const taskId = evt.item.dataset.taskId;
    //             const newStatus = evt.to.dataset.status;
    //             fetch(`/update_task/${taskId}/${newStatus}`, { method: 'GET' });
    //         }
    //     });
    // });
    
    // Drag and drop
    new Sortable(document.getElementById('todo'), {
        group: 'kanban',
        animation: 150,
        onEnd: (evt) => updateTaskStatus(evt.item.dataset.taskId, evt.to.dataset.status)
    });

    new Sortable(document.getElementById('doing'), {
        group: 'kanban',
        animation: 150,
        onEnd: (evt) => updateTaskStatus(evt.item.dataset.taskId, evt.to.dataset.status)
    });

    new Sortable(document.getElementById('done'), {
        group: 'kanban',
        animation: 150,
        onEnd: (evt) => updateTaskStatus(evt.item.dataset.taskId, evt.to.dataset.status)
    });

    // Notificaciones en tiempo real
    socket.on('task_updated', (data) => {
        showNotification(`Tarea ${data.task_id} actualizada a: ${data.status}`);
    });

    function showNotification(message) {
        const toast = document.createElement('div');
        toast.className = 'toast align-items-center text-white bg-primary border-0';
        toast.innerHTML = `
            <div class="d-flex">
                <div class="toast-body">${message}</div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        `;
        document.getElementById('notifications').appendChild(toast);
        new bootstrap.Toast(toast).show();
        setTimeout(() => toast.remove(), 5000);
    }

    async function updateTaskStatus(taskId, newStatus) {
        await fetch(`/update_task/${taskId}/${newStatus}`);
        // No es necesario recargar la página
    }
});