const socket = io();

// Flag to indicate if the user is a customer
const isCustomer = true; // Set this flag according to the user's role

if (navigator.geolocation) {
    navigator.geolocation.watchPosition(
        (position) => {
            const { latitude, longitude } = position.coords;
            console.log("Sending location:", latitude, longitude);  // Debug log
            socket.emit("send-location", { latitude, longitude, isCustomer });
        },
        (error) => {
            console.error("Geolocation error:", error);
        },
        {
            enableHighAccuracy: true,
            timeout: 5000,
            maximumAge: 0
        }
    );
} else {
    console.error("Geolocation is not supported by this browser.");
}

// Initialize the map
const map = L.map("map").setView([0, 0], 10);

// Add the tile layer to the map
L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution: "OpenStreetMap"
}).addTo(map);

const markers = {};

// Listen for 'receive-location' event from the server
socket.on("receive-location", (data) => {
    console.log("Received location from server:", data);  // Debug log
    const { id, latitude, longitude, isCustomer } = data;

    // Center the map on the received location with zoom
    map.setView([latitude, longitude], 13);  // Adjust zoom level for visibility

    // Add or update marker for each user
    if (isCustomer) {
        // For customers, add the marker only if it doesn't exist
        if (!markers[id]) {
            markers[id] = L.marker([latitude, longitude]).addTo(map);
        }
    } else {
        // For non-customers (e.g., drivers), update the marker position
        if (markers[id]) {
            markers[id].setLatLng([latitude, longitude]);
        } else {
            markers[id] = L.marker([latitude, longitude]).addTo(map);
        }
    }
});

// Handle when a user disconnects and remove their marker
socket.on("user-disconnected", (id) => {
    console.log("User disconnected, removing marker:", id);  // Debug log
    if (markers[id]) {
        map.removeLayer(markers[id]);
        delete markers[id];
    }
});
