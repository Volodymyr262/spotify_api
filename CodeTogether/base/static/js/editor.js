document.getElementById('download-button').addEventListener('click', function() {
    // Get the current value from the editor
    const textToWrite = editor.getValue();

    // Create a new Blob object containing the text, with type 'text/plain'
    const textFileAsBlob = new Blob([textToWrite], { type: 'text/plain' });

    const fileNameToSaveAs = "editor_content.txt";

    // Create a new anchor element to facilitate the download
    const downloadLink = document.createElement("a");
    downloadLink.download = fileNameToSaveAs;

    downloadLink.innerHTML = "Download File";

    // Check if the browser supports the webkitURL API
    if (window.webkitURL != null) {
        // Use webkitURL to create an object URL for the Blob and set it as the href attribute
        downloadLink.href = window.webkitURL.createObjectURL(textFileAsBlob);
    } else {
        // Use the standard URL API to create an object URL for the Blob and set it as the href attribute
        downloadLink.href = window.URL.createObjectURL(textFileAsBlob);

        downloadLink.onclick = destroyClickedElement;

        // Hide the anchor element from view
        downloadLink.style.display = "none";
        document.body.appendChild(downloadLink);
    }

    // Programmatically click the anchor element to trigger the download
    downloadLink.click();
});

// Function to remove the clicked element from the document body
function destroyClickedElement(event) {
    document.body.removeChild(event.target);
}