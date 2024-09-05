const express = require("express");
const app = express();
const http = require("http");
const path = require("path");
const socketio = require("socket.io");

const server = http.createServer(app);
const io = socketio(server);

// Set view engine to EJS
app.set("view engine", "ejs");

// Serve static files from the "public" directory
app.use(express.static(path.join(__dirname, "public")));

io.on("connection", function (socket) {
    console.log("A user connected with id:", socket.id); // Debug log

    // Listen for 'send-location' from the client
    socket.on("send-location", function (data) {
        console.log("Location received from client:", data); // Debug log

        // Broadcast the location to all clients, including the sender
        io.emit("receive-location", { id: socket.id, ...data });
    });

    // Log when the user disconnects
    socket.on("disconnect", function () {
        console.log("User disconnected:", socket.id);
        io.emit("user-disconnected", socket.id);
    });
});

// Basic route handler
app.get("/", function (req, res) {
    res.render("index");
});

// Start the server
server.listen(3000, () => {
    console.log("Server is running on port 3000");
});