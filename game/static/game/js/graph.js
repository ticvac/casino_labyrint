console.log("graph loaded")

const canvas = document.getElementById("graphCanvas");
const ctx = canvas.getContext("2d");

// Set canvas dimensions
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

// Draw a simple graph
ctx.fillStyle = "lightblue";
ctx.fillRect(0, 0, canvas.width, canvas.height);