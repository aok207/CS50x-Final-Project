# Pick a Movie Website

#### Video Demo:  <https://youtu.be/2DWyaSFVLIA>

#### Description:

The "Pick a Movie" website is a movie recommendation platform designed to help users discover their next favorite film. It provides personalized movie suggestions based on user preferences, such as genre, release year, and rating.

## Files Overview

### `layout.html`

This file contains the basic structure and layout for the website. It defines the header, navigation menu, and main content area. It also includes links to external CSS stylesheets and JavaScript files.

### `index.html`

This is the homepage of the website. It extends the layout from `layout.html` and provides an introduction to the service, encouraging users to get started with the movie recommendation process.

### `error.html`

This page is displayed when no results are found based on the user's preferences. It extends the layout and provides an option to retake the quiz.

### `movies.html`

This page displays a list of trending movies. It extends the layout and dynamically populates the content based on the data provided by TMDb API.

### `questions.html`

This file contains the quiz questions that help in generating personalized movie recommendations. It extends the layout and includes a series of questions with multiple-choice answers.

### `recommendation.html`

This page displays the recommended movie along with its poster, title, overview, and an option to watch the trailer. It extends the layout and dynamically updates the content based on the recommendation data.

### `series.html`

Similar to `movies.html`, this page displays a list of trending TV series. It extends the layout and dynamically populates the content based on the data provided by TMDb API.

### `script.js`

This JavaScript file contains functions for handling user interactions, submitting quiz answers, and dynamically updating the content on the recommendation page.

### `styles.css`

This CSS file contains the styles and layout rules for the website. It defines the appearance of various elements, such as fonts, colors, and positioning.

## Design Choices

- **AJAX Requests**: The website uses AJAX to make asynchronous requests to the server for processing quiz answers and generating recommendations without refreshing the entire page.

- **Modular Layout**: The use of HTML templates and extending layouts allows for consistent design and easy updates across different pages.

- **Responsive Design**: The website is designed to be mobile-friendly, ensuring a seamless user experience on various devices.

- **External Libraries**: The project utilizes external resources like Font Awesome for icons and Google Fonts for typography to enhance the visual appeal.
