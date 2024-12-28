let bikeMap; // Leaflet map instance
let markers = []; // Array to store marker instances
// Initialize the map
function initializeMap() {
    if (!bikeMap) {
        bikeMap = L.map('map-container').setView([-6.369028, 34.888822], 6); // Example center coordinates
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; OpenStreetMap contributors'
        }).addTo(bikeMap);
    }
}

// Function to update markers dynamically
function updateMarkers(markerData) {
    // Remove existing markers from the map
    console.log('Removing existing markers:', markers);
    markers.forEach(marker => bikeMap.removeLayer(marker));
    markers = []; // Clear the markers array
    console.log('Adding new markers:', markerData);
    // Add new markers from the fetched data
    markerData.forEach(data => {
        const marker = L.marker([data.lat, data.lng]).addTo(bikeMap)
            .bindPopup(data.popup);
        markers.push(marker); // Store marker in array
    });

}

// Polling for marker updates every 20 seconds using HTMX or fetch API
function pollMarkers() {
    fetch('update_markers')
        .then(response => {
            console.log('Response:', response);
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            return response.json();
        })
        .then(data => updateMarkers(data))
        .catch(error => console.error('Error fetching marker data:', error));
}

// Listen for custom events to activate and deactivate the map
document.addEventListener('activateMap', (event) => {
    console.log('Map activated');
    const mapContainer = document.getElementById('map-container');
    mapContainer.style.display = 'block';
    // if map is not initialized, initialize it and start polling for markers
    if (!bikeMap) {
        console.log('Initializing map');
        initializeMap();
        pollMarkers(); // Initial fetch of markers
        // Set up polling every 20 seconds
        setInterval(pollMarkers, 20000);
    }
    else {
        console.log('Map already initialized');
        pollMarkers(); // Fetch markers immediately
    }
});

document.addEventListener('deactivateMap', () => {
    const mapContainer = document.getElementById('map-container');
    mapContainer.style.display = 'none';
  
    // Clean up Leaflet instance and clear container content
    if (bikeMap) {
        bikeMap.remove();
        bikeMap = null;
        markers = [];
    }
    mapContainer.innerHTML = '';

});