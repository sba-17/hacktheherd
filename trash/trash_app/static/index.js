//const output = document.getElementById("text");
//    const image = document.getElementById("myImage");
//
//    let milliseconds = 3000;  // Interval to refresh
//    setInterval(reFetch, milliseconds);
//    let iteration = 0;
//    let res = "";
//
//    function reFetch() {
//         fetch("../api")
//             .then((response) => response.json())
//             .then(response => {
//                 // Update text if it has changed
//                 if (response.text !== res) {
//                     res = response.text;
//                     output.classList.add("ai-message")
//                     output.innerHTML = res;
//                     iteration = 0;
//                 }
//
//                 // Refresh the image by updating the `src` with a timestamp to avoid caching
//                 const timestamp = new Date().getTime();  // Unique timestamp for cache busting
//                 image.src = "{% static 'photo.jpg' %}?timestamp=" + timestamp;
//
//             }).catch(error => console.error('Error fetching data:', error));
//
//         console.log(iteration);
//         iteration++;
//    }
//
//const eyelids = document.querySelectorAll('.eyelid');
//function animateEyes() {
//  eyelids.forEach(eyelid => {
//    // constant blink after 2 seconds
//    let eyelidsAreOpen = false; // Track state for each eyelid
//    setInterval(() => {
//        eyelidsAreOpen = !eyelidsAreOpen; // Toggle state
//        eyelid.style.transform = eyelidsAreOpen ? `scale(0.5,1)` : `scale(1,0.1)`; // Apply transformation
//    }, 1000); // Blink every 2 seconds
//  });
//}
//
//animateEyes();