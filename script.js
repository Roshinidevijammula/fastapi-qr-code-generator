document.getElementById("btnGenerate").addEventListener("click", async () => {
  const urlInput = document.getElementById("urlInput");
  const btnGenerate = document.getElementById("btnGenerate");
  const emptyState = document.getElementById("empty-state");
  const loadingState = document.getElementById("loading-state");
  const qrDisplay = document.getElementById("qr-display");
  const result = document.getElementById("result");
  const btnDownload = document.getElementById("btnDownload");
  const btnCopyLink = document.getElementById("btnCopyLink");

  const url = urlInput.value.trim();
  if (!url) {
    alert("Please enter a URL");
    return;
  }

  // Set loading state
  emptyState.classList.add("hidden");
  qrDisplay.classList.add("hidden");
  loadingState.classList.remove("hidden");
  btnGenerate.disabled = true;
  urlInput.disabled = true;

  try {
    const response = await fetch("/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url })
    });

    const data = await response.json();
    
    if (data.error) {
      alert(data.error);
      emptyState.classList.remove("hidden");
      loadingState.classList.add("hidden");
      return;
    }

    // Build the image element
    const img = document.createElement("img");
    img.src = data.qr_url;
    img.id = "qrImage";
    img.alt = "Generated QR Code";

    // Inject image
    result.innerHTML = "";
    result.appendChild(img);

    // Setup actions
    btnDownload.href = data.qr_url;
    
    // Copy link handler
    btnCopyLink.onclick = async () => {
      try {
        await navigator.clipboard.writeText(data.qr_url);
        const originalText = btnCopyLink.innerHTML;
        btnCopyLink.innerHTML = `
          <svg class="action-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="20 6 9 17 4 12"></polyline>
          </svg>
          <span>Copied!</span>
        `;
        setTimeout(() => {
          btnCopyLink.innerHTML = originalText;
        }, 2000);
      } catch (err) {
        console.error("Failed to copy link: ", err);
      }
    };

    // Show result
    loadingState.classList.add("hidden");
    qrDisplay.classList.remove("hidden");

  } catch (error) {
    console.error("Error generating QR code:", error);
    alert("An error occurred while generating the QR code. Please try again.");
    emptyState.classList.remove("hidden");
    loadingState.classList.add("hidden");
  } finally {
    // Re-enable controls
    btnGenerate.disabled = false;
    urlInput.disabled = false;
  }
});
