document.addEventListener("DOMContentLoaded", function() {
    // Add event listener to dropdown change event
    document.getElementById("timestampDropdown").addEventListener("change", function() {
        // Get selected timestamp
        var selectedTimestamp = this.value;
        
        // Check if a timestamp is selected
        if (selectedTimestamp) {
            // Send AJAX request to fetch logs for selected timestamp
            var xhr = new XMLHttpRequest();
            xhr.open("GET", "/fetch-logs?timestamp=" + selectedTimestamp, true);
            xhr.onreadystatechange = function () {
                if (xhr.readyState === XMLHttpRequest.DONE) {
                    if (xhr.status === 200) {
                        // Parse JSON response
                        var logsData = JSON.parse(xhr.responseText);
                        // Display logs
                        displayLogs(logsData);
                    } else {
                        console.error("Error fetching logs:", xhr.status);
                    }
                }
            };
            xhr.send();
        }
    });
});

// Function to display logs on the page
function displayLogs(logsData) {
    var logsContainer = document.getElementById("logsContainer");
    // Clear previous logs
    logsContainer.innerHTML = "";
    // Loop through logs data and generate HTML
    for (var key in logsData) {
        if (logsData.hasOwnProperty(key)) {
            var logItem = document.createElement("div");
            logItem.textContent = key + ": " + logsData[key];
            logsContainer.appendChild(logItem);
        }
    }
}
