// Function to submit answers from questions
function submitAnswer(questionNumber) {
    var responses = [];
    var checkboxes = document.querySelectorAll('input[name="response' + questionNumber + '[]"]:checked');

    checkboxes.forEach(function(checkbox) {
        responses.push(checkbox.value);
    });

    if (responses.length > 0) {
        var xhr = new XMLHttpRequest();
        xhr.open('POST', '/process_answers', true);
        xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded;charset=UTF-8');
        xhr.onload = function () {
            if (xhr.status >= 200 && xhr.status < 400) {
                var data = JSON.parse(xhr.responseText);
                if (data.status === 'success') {
                    var currentQuestion = document.getElementById('question' + questionNumber);
                    var nextQuestion = document.getElementById('question' + (data.next_question));

                    currentQuestion.style.display = 'none';
                    nextQuestion.style.display = 'block';
                } 
                else if (data.status == 'completed') {
                    window.location.replace('/recommendation');
                }
                else {
                    console.error('Server response status is not success:', data.status);
                }
            } else {
                console.error('Error:', xhr.status);
            }
        };

        var params = 'question_number=' + questionNumber + '&answer=' + responses.join('&answer=');
        xhr.send(params);
    } else {
        console.error("No option selected for Question " + questionNumber);
    }
}

// Function to regenerate a movie recommendation
function regenerateMovie() {
    // Create a new XMLHttpRequest object
    var xhr = new XMLHttpRequest();

    // Configure the request to make a GET request to '/regenerate_movie' asynchronously
    xhr.open('GET', '/regenerate_movie', true);

    // Define what happens on successful data retrieval
    xhr.onload = function() {
        if (xhr.status >= 200 && xhr.status < 400) {
            // Parse the JSON response
            var data = JSON.parse(xhr.responseText);

            if (data.status === 'success') {
                // Extract data from the response
                var poster = data.poster;
                var title = data.title;
                var overview = data.overview;
                var trailer = data.trailer;

                // Select elements from the DOM
                var posterElement = document.querySelector('img');
                var titleElement = document.querySelector('h2');
                var infoElement = document.querySelector('label');
                var urlButtonElement = document.querySelector('#trailer-button');
                var urlElement = document.querySelector('#url');

                // Update the DOM with the retrieved data
                posterElement.src = poster;
                infoElement.innerText = overview;
                titleElement.innerText = title;

                // Conditionally handle the trailer element
                if (trailer === "None") {
                    urlButtonElement.style.display = 'none';
                } else {
                    urlButtonElement.style.display = 'inline-block';
                    urlElement.src = trailer;
                }

            } else if (data.status === 'no_movies') {
                // Redirect to '/error' if there are no movies
                window.location.replace('/error');
            } 
            else {
                console.error('Server response status is not success:', data.status);
            }
        } else {
            console.error('Error:', xhr.status);
        }
    };

    // Send the request
    xhr.send();
}

// Add an event listener to the 'Regenerate Movie' button
document.getElementById('regenerateButton').addEventListener('click', regenerateMovie);

// Modal functionality for displaying trailers
const url = document.querySelector('#url')
const video = document.querySelector('#video')

document.querySelector('#trailer-button').addEventListener('click', function() {
    modal.style.display = 'flex';
    video.src = url.src
});

document.querySelector('.close').addEventListener('click', function() {
    modal.style.display = 'none';
    video.src = ""
});

window.addEventListener('click', function(event) {
    if (event.target == modal) {
        modal.style.display = 'none';
        video.src = ""
    }
});
