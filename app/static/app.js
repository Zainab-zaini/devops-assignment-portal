const form = document.getElementById("submissionForm");
const messageBox = document.getElementById("message");
const submitButton = document.getElementById("submitButton");

function showMessage(message, type) {
    messageBox.textContent = message;
    messageBox.className = `message ${type}`;
}

function clearMessage() {
    messageBox.textContent = "";
    messageBox.className = "message";
}


form.addEventListener("submit", async function(event) {

    event.preventDefault();
    clearMessage();

    if (!form.reportValidity()) {
        return;
    }

    const formData = new FormData(form);

    const payload = Object.fromEntries(formData.entries());

    submitButton.disabled = true;
    submitButton.textContent = "Submitting...";

    try {

        const response = await fetch("/api/submissions", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify(payload)

        });

        const result = await response.json();

        if (!response.ok) {

            const error = result.detail;

            const errorMessage = Array.isArray(error)
                ? error.map(item => item.msg).join(", ")
                : error || "Submission failed.";

            throw new Error(errorMessage);
        }

        showMessage(
            "Assignment submitted successfully! Your record has been saved.",
            "success"
        );

        form.reset();

        await loadSubmissions();

    } catch (error) {

        showMessage(error.message, "error");

    } finally {

        submitButton.disabled = false;
        submitButton.innerHTML =
            'Submit Assignment <span>→</span>';

    }

});


async function loadSubmissions() {

    const table = document.getElementById("submissionTable");

    try {

        const response = await fetch("/api/submissions");

        if (!response.ok) {
            throw new Error("Unable to load submissions.");
        }

        const data = await response.json();

        document.getElementById("totalCount").textContent =
            data.total;

        if (data.submissions.length === 0) {

            table.innerHTML = `
                <tr>
                    <td colspan="6" class="empty">
                        No submissions available yet.
                    </td>
                </tr>
            `;

            return;
        }

        table.replaceChildren();

        data.submissions.forEach(item => {

            const row = document.createElement("tr");

            const values = [
                item.id,
                item.student_name,
                item.registration_number,
                item.assignment_title
            ];

            values.forEach(value => {
                const cell = document.createElement("td");
                cell.textContent = value;
                row.appendChild(cell);
            });

            const linkCell = document.createElement("td");
            const link = document.createElement("a");

            link.href = item.submission_url;
            link.textContent = "View Submission";
            link.target = "_blank";
            link.rel = "noopener noreferrer";

            linkCell.appendChild(link);
            row.appendChild(linkCell);

            const dateCell = document.createElement("td");

            dateCell.textContent = item.submitted_at;

            row.appendChild(dateCell);

            table.appendChild(row);

        });

    } catch (error) {

        table.innerHTML = `
            <tr>
                <td colspan="6" class="empty">
                    Unable to retrieve submission records.
                </td>
            </tr>
        `;

    }

}


document.addEventListener("DOMContentLoaded", loadSubmissions);