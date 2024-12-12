let map = L.map('map').setView([40.75, -73.95], 12);
let markers = {};

// Add OpenStreetMap tiles
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '© OpenStreetMap contributors'
}).addTo(map);

// Function to update markers on the map
window.updateMarkers = function(bikes) {
    // Clear existing markers
    Object.values(markers).forEach(marker => map.removeLayer(marker));
    markers = {};

    // Add new markers
    for (const [bikeId, info] of Object.entries(bikes)) {
        const popupContent = `
            <strong>${info.name}</strong><br>
            Type: ${info.type}<br>
            Speed: ${info.speed} km/h<br>
            Battery: ${info.battery}%<br>
            Last Maintenance: ${info.last_maintenance}
        `;
        
        markers[bikeId] = L.marker([info.latitude, info.longitude])
            .bindPopup(popupContent)
            .addTo(map);
    }
};

// Handle bike selection changes
document.querySelectorAll('input[name="selected_bikes"]').forEach(checkbox => {
    checkbox.addEventListener('change', () => {
        document.getElementById('bikes-data').setAttribute('hx-trigger', 'load');
    });
});