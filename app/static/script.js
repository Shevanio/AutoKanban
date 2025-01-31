document.addEventListener("DOMContentLoaded", function() {
    // Handle task deletion confirmation
    document.querySelectorAll(".delete-task-form").forEach(form => {
        form.addEventListener("submit", function(event) {
            event.preventDefault();
            if (confirm("Are you sure you want to delete this task?")) {
                this.submit();
            }
        });
    });

    // Apply dark mode styles dynamically
    function applyDarkMode() {
        document.body.style.backgroundColor = "#121212";
        document.body.style.color = "#e0e0e0";
    }
    applyDarkMode();

    // Handle task status change
    document.querySelectorAll(".task-status").forEach(select => {
        select.addEventListener("change", function() {
            const taskId = this.dataset.taskId;
            const newStatus = this.value;
            fetch(`/update_status/${taskId}`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ status: newStatus })
            }).then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert("Task status updated successfully!");
                } else {
                    alert("Error updating task status.");
                }
            });
        });
    });
});
