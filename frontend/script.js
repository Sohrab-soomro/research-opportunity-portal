// =============================================================
// University Research Opportunity Portal - frontend logic
// All data comes from the backend REST API (no hard-coded data).
// =============================================================

// If the page is served by Flask (http://localhost:5000) use the same origin,
// otherwise (index.html opened directly as a file) use the default backend address.
const API_URL = window.location.protocol.startsWith("http")
    ? `${window.location.origin}/api/opportunities`
    : "http://localhost:5000/api/opportunities";

const FIELDS = [
    "research_title", "research_description", "research_area", "faculty_name",
    "department", "required_skills", "available_positions", "application_deadline", "status"
];

// ---------- Element references ----------
const views = {
    list: document.getElementById("listView"),
    details: document.getElementById("detailsView"),
    form: document.getElementById("formView"),
};
const messageBox = document.getElementById("message");
const tableEl = document.getElementById("opportunityTable");
const tableBody = document.getElementById("opportunityBody");
const listInfo = document.getElementById("listInfo");
const form = document.getElementById("opportunityForm");
const idInput = document.getElementById("opportunityId");
const navList = document.getElementById("navList");
const navCreate = document.getElementById("navCreate");

let messageTimer = null;

// =============================================================
// Helpers
// =============================================================

/** Show a success or error message at the top of the page. */
function showMessage(text, type = "success") {
    messageBox.textContent = text;
    messageBox.className = `message ${type}`;
    clearTimeout(messageTimer);
    messageTimer = setTimeout(() => messageBox.classList.add("hidden"), 6000);
    window.scrollTo({ top: 0, behavior: "smooth" });
}

function hideMessage() {
    messageBox.classList.add("hidden");
}

/** Switch between list, details and form views. */
function showView(name) {
    Object.values(views).forEach(v => v.classList.add("hidden"));
    views[name].classList.remove("hidden");
    navList.classList.toggle("active", name === "list");
    navCreate.classList.toggle("active", name === "form" && !idInput.value);
}

/** Turn an API error response into a readable message. */
function errorText(status, body) {
    if (status === 400) {
        const details = body && body.details ? `: ${body.details.join(", ")}` : "";
        return `Invalid input${details}`;
    }
    if (status === 404) return "Research opportunity not found. It may have been deleted.";
    if (status >= 500) return "Server error. Please check that the backend and database are running.";
    return (body && body.error) || `Request failed (HTTP ${status})`;
}

/**
 * Send a request to the API and return the parsed JSON.
 * Throws an Error with a user-friendly message if something goes wrong.
 */
async function apiRequest(method, url, body) {
    const options = { method, headers: {} };
    if (body !== undefined) {
        options.headers["Content-Type"] = "application/json";
        options.body = JSON.stringify(body);
    }

    let response;
    try {
        response = await fetch(url, options);
    } catch (err) {
        throw new Error("Cannot connect to the server. Make sure the backend is running on http://localhost:5000.");
    }

    let data = null;
    try { data = await response.json(); } catch (err) { /* response had no JSON */ }

    if (!response.ok) {
        throw new Error(errorText(response.status, data));
    }
    return data;
}

/** Format "2026-11-30" as "30 Nov 2026". */
function formatDate(isoDate) {
    const [y, m, d] = isoDate.split("-").map(Number);
    return new Date(y, m - 1, d).toLocaleDateString("en-GB", {
        day: "numeric", month: "short", year: "numeric"
    });
}

/** Create an element with optional class and text (text is never parsed as HTML). */
function make(tag, className, text) {
    const el = document.createElement(tag);
    if (className) el.className = className;
    if (text !== undefined) el.textContent = text;
    return el;
}

function statusBadge(status) {
    return make("span", `badge ${status === "Open" ? "open" : "closed"}`, status);
}

/** Build the View / Edit / Close / Delete buttons for one opportunity. */
function actionButtons(opp, includeView = true) {
    const buttons = [];
    if (includeView) {
        const view = make("button", "btn btn-view", "View");
        view.onclick = () => viewOpportunity(opp.id);
        buttons.push(view);
    }

    const edit = make("button", "btn btn-edit", "Edit");
    edit.onclick = () => openEditForm(opp.id);
    buttons.push(edit);

    const close = make("button", "btn btn-close", "Close");
    close.title = opp.status === "Closed" ? "Already closed" : "Change status to Closed";
    close.disabled = opp.status === "Closed";
    close.onclick = () => closeOpportunity(opp.id);
    buttons.push(close);

    const del = make("button", "btn btn-delete", "Delete");
    del.onclick = () => deleteOpportunity(opp.id, opp.research_title);
    buttons.push(del);

    return buttons;
}

// =============================================================
// 1. Display all opportunities  (GET /api/opportunities)
// =============================================================
async function loadOpportunities() {
    listInfo.textContent = "Loading opportunities...";
    try {
        const result = await apiRequest("GET", API_URL);
        renderTable(result.data);
    } catch (err) {
        tableEl.classList.add("hidden");
        listInfo.textContent = "Could not load opportunities.";
        showMessage(err.message, "error");
    }
}

function renderTable(opportunities) {
    tableBody.innerHTML = "";

    if (opportunities.length === 0) {
        tableEl.classList.add("hidden");
        listInfo.textContent = "No research opportunities yet. Click \"+ New Opportunity\" to add one.";
        return;
    }

    listInfo.textContent = `${opportunities.length} opportunit${opportunities.length === 1 ? "y" : "ies"} found.`;
    tableEl.classList.remove("hidden");

    opportunities.forEach(opp => {
        const row = document.createElement("tr");
        row.appendChild(make("td", "title-cell", opp.research_title));
        row.appendChild(make("td", "", opp.research_area));
        row.appendChild(make("td", "", opp.faculty_name));
        row.appendChild(make("td", "", opp.department));
        row.appendChild(make("td", "", opp.available_positions));
        row.appendChild(make("td", "", formatDate(opp.application_deadline)));

        const statusCell = make("td");
        statusCell.appendChild(statusBadge(opp.status));
        row.appendChild(statusCell);

        const actionsCell = make("td", "actions");
        actionButtons(opp).forEach(b => actionsCell.appendChild(b));
        row.appendChild(actionsCell);

        tableBody.appendChild(row);
    });
}

// =============================================================
// 2. Display details of one opportunity  (GET /api/opportunities/:id)
// =============================================================
async function viewOpportunity(id) {
    try {
        const result = await apiRequest("GET", `${API_URL}/${id}`);
        renderDetails(result.data);
        hideMessage();
        showView("details");
    } catch (err) {
        showMessage(err.message, "error");
        loadOpportunities();
    }
}

function renderDetails(opp) {
    const list = document.getElementById("detailsList");
    list.innerHTML = "";

    const rows = [
        ["ID", opp.id],
        ["Research Title", opp.research_title],
        ["Description", opp.research_description],
        ["Research Area", opp.research_area],
        ["Faculty Member", opp.faculty_name],
        ["Department", opp.department],
        ["Required Skills", opp.required_skills],
        ["Available Positions", opp.available_positions],
        ["Application Deadline", formatDate(opp.application_deadline)],
    ];

    rows.forEach(([label, value]) => {
        list.appendChild(make("dt", "", label));
        list.appendChild(make("dd", "", value));
    });

    list.appendChild(make("dt", "", "Status"));
    const statusDd = make("dd");
    statusDd.appendChild(statusBadge(opp.status));
    list.appendChild(statusDd);

    const actions = document.getElementById("detailsActions");
    actions.innerHTML = "";
    actionButtons(opp, false).forEach(b => actions.appendChild(b));
}

// =============================================================
// 3 & 4. Create / Update form  (POST and PUT)
// =============================================================
function openCreateForm() {
    form.reset();
    clearFieldErrors();
    idInput.value = "";
    document.getElementById("formTitle").textContent = "New Research Opportunity";
    document.getElementById("submitBtn").textContent = "Create Opportunity";
    hideMessage();
    showView("form");
}

async function openEditForm(id) {
    try {
        // Load the latest data from the database before editing
        const result = await apiRequest("GET", `${API_URL}/${id}`);
        const opp = result.data;

        form.reset();
        clearFieldErrors();
        idInput.value = opp.id;
        FIELDS.forEach(f => { document.getElementById(f).value = opp[f]; });

        document.getElementById("formTitle").textContent = `Edit Opportunity #${opp.id}`;
        document.getElementById("submitBtn").textContent = "Save Changes";
        hideMessage();
        showView("form");
    } catch (err) {
        showMessage(err.message, "error");
        loadOpportunities();
    }
}

function clearFieldErrors() {
    form.querySelectorAll(".field-error").forEach(e => (e.textContent = ""));
    form.querySelectorAll(".invalid").forEach(e => e.classList.remove("invalid"));
}

function setFieldError(fieldId, text) {
    const input = document.getElementById(fieldId);
    input.classList.add("invalid");
    input.parentElement.querySelector(".field-error").textContent = text;
}

/** Basic validation of required form fields. Returns true if valid. */
function validateForm() {
    clearFieldErrors();
    let valid = true;

    const required = {
        research_title: "Research title is required",
        research_description: "Description is required",
        research_area: "Research area is required",
        faculty_name: "Faculty name is required",
        department: "Department is required",
        required_skills: "Required skills are required",
    };

    Object.entries(required).forEach(([id, msg]) => {
        if (document.getElementById(id).value.trim() === "") {
            setFieldError(id, msg);
            valid = false;
        }
    });

    const positions = document.getElementById("available_positions").value.trim();
    if (!/^\d+$/.test(positions) || Number(positions) < 1) {
        setFieldError("available_positions", "Enter a whole number of 1 or more");
        valid = false;
    }

    if (!document.getElementById("application_deadline").value) {
        setFieldError("application_deadline", "Application deadline is required");
        valid = false;
    }

    if (!["Open", "Closed"].includes(document.getElementById("status").value)) {
        setFieldError("status", "Status must be Open or Closed");
        valid = false;
    }

    return valid;
}

form.addEventListener("submit", async (event) => {
    event.preventDefault();

    if (!validateForm()) {
        showMessage("Please fix the highlighted fields before submitting.", "error");
        return;
    }

    const payload = {};
    FIELDS.forEach(f => { payload[f] = document.getElementById(f).value.trim(); });
    payload.available_positions = Number(payload.available_positions);

    const id = idInput.value;
    const submitBtn = document.getElementById("submitBtn");
    submitBtn.disabled = true;

    try {
        if (id) {
            await apiRequest("PUT", `${API_URL}/${id}`, payload);
            showMessage("Research opportunity updated successfully.");
        } else {
            await apiRequest("POST", API_URL, payload);
            showMessage("Research opportunity created successfully.");
        }
        form.reset();
        showView("list");
        loadOpportunities();
    } catch (err) {
        showMessage(err.message, "error");
    } finally {
        submitBtn.disabled = false;
    }
});

// =============================================================
// 5. Close an opportunity  (PUT /api/opportunities/:id  {status: "Closed"})
// =============================================================
async function closeOpportunity(id) {
    try {
        const result = await apiRequest("PUT", `${API_URL}/${id}`, { status: "Closed" });
        showMessage(`"${result.data.research_title}" is now Closed.`);
        if (!views.details.classList.contains("hidden")) {
            renderDetails(result.data);
        }
        loadOpportunities();
    } catch (err) {
        showMessage(err.message, "error");
        loadOpportunities();
    }
}

// =============================================================
// 6. Delete an opportunity  (DELETE /api/opportunities/:id)
// =============================================================
async function deleteOpportunity(id, title) {
    if (!confirm(`Are you sure you want to delete "${title}"?\nThis cannot be undone.`)) {
        return;
    }
    try {
        await apiRequest("DELETE", `${API_URL}/${id}`);
        showMessage("Research opportunity deleted successfully.");
    } catch (err) {
        showMessage(err.message, "error");
    }
    showView("list");
    loadOpportunities();
}

// =============================================================
// Navigation
// =============================================================
navList.addEventListener("click", () => { showView("list"); loadOpportunities(); });
navCreate.addEventListener("click", openCreateForm);
document.getElementById("refreshBtn").addEventListener("click", loadOpportunities);
document.querySelectorAll("[data-back]").forEach(btn =>
    btn.addEventListener("click", () => { showView("list"); loadOpportunities(); })
);

// Load the list when the page opens
loadOpportunities();
