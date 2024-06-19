document.getElementById('download-button').addEventListener('click', function() {
            const textToWrite = editor.getValue();
            const textFileAsBlob = new Blob([textToWrite], { type: 'text/plain' });
            const fileNameToSaveAs = "editor_content.txt";

            const downloadLink = document.createElement("a");
            downloadLink.download = fileNameToSaveAs;
            downloadLink.innerHTML = "Download File";
            if (window.webkitURL != null) {
                downloadLink.href = window.webkitURL.createObjectURL(textFileAsBlob);
            } else {
                downloadLink.href = window.URL.createObjectURL(textFileAsBlob);
                downloadLink.onclick = destroyClickedElement;
                downloadLink.style.display = "none";
                document.body.appendChild(downloadLink);
            }

            downloadLink.click();
        });

        function destroyClickedElement(event) {
            document.body.removeChild(event.target);
        }

