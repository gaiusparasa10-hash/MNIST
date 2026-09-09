// // Wait for DOM content to load before attaching event listeners
// document.addEventListener('DOMContentLoaded', () => {
//     const canvas = document.getElementById('canvas');
//     const ctx = canvas.getContext('2d');
//     const predictBtn = document.getElementById('predict-btn');
//     const clearBtn = document.getElementById('clear-btn');
//     const predictionText = document.getElementById('prediction-text');
//     const confidenceText = document.getElementById('confidence-text');

//     let isDrawing = false;

//     // Initialize canvas background to solid black (MNIST format standard)
//     function clearCanvas() {
//         ctx.fillStyle = '#000000';
//         ctx.fillRect(0, 0, canvas.width, canvas.height);
//         predictionText.textContent = '-';
//         confidenceText.textContent = '-';
//     }

//     // Set initial stroke properties for drawing white digits
//     ctx.lineWidth = 18;
//     ctx.lineCap = 'round';
//     ctx.lineJoin = 'round';
//     ctx.strokeStyle = '#ffffff';

//     clearCanvas();

//     // Helper to get coordinates for mouse and touch events
//     function getCoordinates(e) {
//         const rect = canvas.getBoundingClientRect();
//         if (e.touches && e.touches.length > 0) {
//             return {
//                 x: e.touches[0].clientX - rect.left,
//                 y: e.touches[0].clientY - rect.top
//             };
//         } else {
//             return {
//                 x: e.clientX - rect.left,
//                 y: e.clientY - rect.top
//             };
//         }
//     }

//     // Start drawing
//     function startDrawing(e) {
//         isDrawing = true;
//         const coords = getCoordinates(e);
//         ctx.beginPath();
//         ctx.moveTo(coords.x, coords.y);
//     }

//     // Draw lines as user moves mouse/finger
//     function draw(e) {
//         if (!isDrawing) return;
//         e.preventDefault(); // Prevent scrolling on touch devices
//         const coords = getCoordinates(e);
//         ctx.lineTo(coords.x, coords.y);
//         ctx.stroke();
//     }

//     // Stop drawing
//     function stopDrawing() {
//         if (isDrawing) {
//             isDrawing = false;
//             ctx.beginPath();
//         }
//     }

//     // Event listeners for Mouse input
//     canvas.addEventListener('mousedown', startDrawing);
//     canvas.addEventListener('mousemove', draw);
//     canvas.addEventListener('mouseup', stopDrawing);
//     canvas.addEventListener('mouseleave', stopDrawing);

//     // Event listeners for Touch input (Mobile support)
//     canvas.addEventListener('touchstart', startDrawing);
//     canvas.addEventListener('touchmove', draw);
//     canvas.addEventListener('touchend', stopDrawing);

//     // Clear button action
//     clearBtn.addEventListener('click', clearCanvas);

//     // Predict button action - Send drawing to Flask backend
//     predictBtn.addEventListener('click', async () => {
//         // Convert canvas drawing to base64 Data URL
//         const dataUrl = canvas.toDataURL('image/png');

//         // Update UI to show loading status
//         predictionText.textContent = '...';
//         confidenceText.textContent = '...';

//         try {
//             const response = await fetch('/predict', {
//                 method: 'POST',
//                 headers: {
//                     'Content-Type': 'application/json'
//                 },
//                 body: JSON.stringify({ image: dataUrl })
//             });

//             if (!response.ok) {
//                 throw new Error('Prediction request failed.');
//             }

//             const data = await response.json();
            
//             // Display prediction and formatted confidence score
//             predictionText.textContent = data.prediction;
//             confidenceText.textContent = `${data.confidence.toFixed(1)}%`;
//         } catch (error) {
//             console.error('Error during prediction:', error);
//             predictionText.textContent = 'Error';
//             confidenceText.textContent = 'Error';
//         }
//     });
// });
