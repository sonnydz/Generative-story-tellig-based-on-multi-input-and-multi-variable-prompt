// JavaScript functions for handling icon clicks
async function handleCameraClick() {
    // Replace this with your logic for generating a story
    const generatedStory = await generateStoryBasedOnPrompt("A beautiful sunny day...");

    // Update the story content in the HTML
    document.getElementById('storyContent').innerText = generatedStory;

    // Show the story container
    document.getElementById('storyContainer').style.display = 'block';
}

// Function to make a request to the /generate_story endpoint
async function generateStoryBasedOnPrompt(prompt) {
    const response = await fetch('http://localhost:5000/generate_story', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            input_text: prompt,
        }),
    });

    const data = await response.json();

    // Extract the generated story from the response
    const generatedStory = data.generated_story;

    return generatedStory;
}