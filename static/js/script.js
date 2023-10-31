
function generateResponse() {
    const imageUpload = document.getElementById("imageUpload");
    const file = imageUpload.files[0];

    if (!file) {
        alert("Please select an image.");
        return;
    }

    const formData = new FormData();
    formData.append("image", file);

    // Send the image to the server
    fetch('/generate', {
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
.then(data => {
    const responseElement = document.getElementById("response");
    responseElement.innerHTML = "";
    
    if (data.caption && Array.isArray(data.caption) && data.caption.length > 0) {
        const responseText = data.caption[0].generated_text; // Access the generated_text property
        let i = 0;
        const typingInterval = 50;
        const typingFunction = () => {
            responseElement.innerHTML += responseText.charAt(i);
            i++;
            if (i < responseText.length) {
                setTimeout(typingFunction, typingInterval);
            }
        };
        typingFunction();
    } else {
        console.error('Invalid response structure');
    }
})
.catch(error => {
    console.error('Error:', error);
});
}

function copyResponse() {
    const responseText = document.getElementById("response").innerText;
    const tempTextarea = document.createElement("textarea");
    tempTextarea.value = responseText;
    document.body.appendChild(tempTextarea);
    tempTextarea.select();
    document.execCommand("copy");
    document.body.removeChild(tempTextarea);
    alert("Response copied to clipboard!");
}

