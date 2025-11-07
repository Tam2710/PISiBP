// ⚠️ API_URL je već definisan u top_bar.html
let token = localStorage.getItem("access");
const refresh = localStorage.getItem("refresh");
const resultsFormId = localStorage.getItem("formId");
const resultsList = document.getElementById('resultsList');

// === Token Refresh ===
async function getValidToken() {
  if (token) {
    const res = await fetch(API_URL + "forms/", {
      headers: { "Authorization": `Bearer ${token}` }
    });
    if (res.status !== 401) return token;
  }

  if (refresh) {
    const res = await fetch(API_URL + "token/refresh/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ refresh })
    });
    const data = await res.json();
    if (res.ok && data.access) {
      localStorage.setItem("access", data.access);
      token = data.access;
      return token;
    }
  }

  alert("Session expired. Please log in again.");
  window.location.href = "/";
  return null;
}

// === Load Results ===
async function loadResults() {
  const validToken = await getValidToken();
  if (!validToken) return;

  try {
    const res = await fetch(`${API_URL}forms/${resultsFormId}/results/`, {
      headers: { "Authorization": `Bearer ${validToken}` }
    });

    if (!res.ok) {
      const err = await res.text();
      console.error("Error loading results:", err);
      resultsList.innerHTML = "<p style='color:red;text-align:center;'>❌ Failed to load results.</p>";
      return;
    }

    const results = await res.json();
    renderResults(results);
  } catch (err) {
    console.error("Network error:", err);
    resultsList.innerHTML = "<p style='color:red;text-align:center;'>⚠️ Network error loading results.</p>";
  }
}

// === Render Results ===
function renderResults(results) {
  if (!results || results.length === 0) {
    resultsList.innerHTML = "<p style='text-align:center;'>No responses yet.</p>";
    return;
  }

  resultsList.innerHTML = "";
  results.forEach((r, idx) => {
    const div = document.createElement("div");
    div.classList.add("result-card");

    let answersHTML = "";
    r.answers.forEach(ans => {
      let ansText = "";
      if (ans.value) ansText = ans.value;
      else if (ans.selected_options?.length)
        ansText = ans.selected_options.map(o => o.text).join(", ");
      answersHTML += `
        <div class="question">${ans.question_text || ans.question}</div>
        <div class="answer">${ansText || "<i>No answer</i>"}</div>
        <hr>
      `;
    });

    div.innerHTML = `<h4>🧾 Response #${idx + 1}</h4>${answersHTML}`;
    resultsList.appendChild(div);
  });
}

// === Export to XLSX ===
async function exportForm() {
  const validToken = await getValidToken();
  if (!validToken) return;

  try {
    const res = await fetch(`${API_URL}forms/${resultsFormId}/export/`, {
      method: "GET",
      headers: { "Authorization": `Bearer ${validToken}` }
    });

    if (!res.ok) {
      const err = await res.text();
      console.error("Export error:", err);
      alert("❌ Failed to export results.");
      return;
    }

    const blob = await res.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `form_${resultsFormId}_results.xlsx`;
    document.body.appendChild(a);
    a.click();
    a.remove();
    window.URL.revokeObjectURL(url);
  } catch (err) {
    console.error("⚠️ Network error:", err);
    alert("⚠️ Network problem while exporting.");
  }
}

loadResults();