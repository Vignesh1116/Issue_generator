const bugBtn = document.getElementById("bugBtn");
const issueBox = document.getElementById("issueBox");

bugBtn.addEventListener("click", () => {
  issueBox.classList.toggle("active");
});

document.getElementById("submitIssue").addEventListener("click", async () => {
  const issueText = document.getElementById("issueText").value.trim();

  if (!issueText) {
    alert("Please enter issue");
    return;
  }

  const res = await fetch("https://issue-generator.onrender.com/create-issue", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      issueText,
      pageUrl: window.location.href
    })
  });

  const data = await res.json();

  if (data.success) {
    alert("Issue created successfully!");
    window.open(data.issueUrl, "_blank");
  } else {
    alert("Failed to submit issue");
  }
});