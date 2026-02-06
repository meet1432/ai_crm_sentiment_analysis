const inputEl = document.getElementById("inputText");
const analyzeBtn = document.getElementById("analyzeBtn");
const statusEl = document.getElementById("status");
const resultEl = document.getElementById("result");
const labelEl = document.getElementById("label");
const scoreEl = document.getElementById("score");
const reasonEl = document.getElementById("reason");

async function analyze() {
  const text = inputEl.value.trim();
  if (!text) {
    statusEl.textContent = "Please paste some text.";
    return;
  }
  statusEl.textContent = "Analyzing...";
  analyzeBtn.disabled = true;
  try {
    const res = await fetch("/sentiment", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text }),
    });
    const data = await res.json();
    if (!res.ok) {
      statusEl.textContent = data.detail || "Request failed";
      return;
    }
    labelEl.textContent = `Label: ${data.label}`;
    scoreEl.textContent = `Score: ${data.score}`;
    reasonEl.textContent = data.brief_reason || "";
    resultEl.style.display = "block";
    statusEl.textContent = "";
  } catch (err) {
    statusEl.textContent = "Network error.";
  } finally {
    analyzeBtn.disabled = false;
  }
}

analyzeBtn.addEventListener("click", analyze);
