# Project Report for MusicStacks Application

### yunfanh2, rzieg3, tianyih5, ericjm4



**Executive Summary:** The MusicStack project aimed to develop a comprehensive music platform that allowed users to search for albums, rate them, follow other users, and manage playlists. This report outlines the project's accomplishments, shortcomings, design changes, functionalities, technical challenges, and recommendations for future improvements.

----------------

### Achievements and Shortcomings

**Achievements:**

1. **Search Engine for Albums:** The application successfully integrated a robust search engine, enabling users to efficiently search for albums using various criteria. This functionality enhances user experience by facilitating easy access to desired content.
2. **Rating System:** A dynamic rating system was implemented, allowing users to rate albums and tracks. This feature not only engages users but also helps in curating personalized content based on preferences.
3. **User Following and Followers:** The platform supports a social component where users can follow others and see who follows them, fostering a community environment.
4. **User Edit Playlist:** Users can create and manage their playlists, which enhances personalization and user engagement with the platform.
5. **Markov Chain Algorithm for Recommendations:** Leveraging a Markov chain algorithm, the application provides personalized album recommendations, enhancing user experience by suggesting content aligned with their tastes.

**Shortcomings:**

1. **Lack of Playlist Page:** The application did not implement a dedicated page for managing individual playlists, which limits user interaction with playlists.
2. **No Functionality for Adding or Removing Tracks in Playlists:** Users are unable to modify their playlists by adding or removing tracks, which could restrict user satisfaction and engagement.

-------------

### Design Changes and Table Implementations

**ER Diagram and Table Implementations:**

- The underlying database schema did not undergo significant structural changes during the project. The initial design effectively supported the required functionalities.
- **Addition of Procedures and Triggers:** To enhance the rating functionality, the database was equipped with additional stored procedures and triggers. These elements ensured reliable and efficient processing of user ratings for albums and tracks, maintaining data integrity and performance.

**Data source changes:**

- we **didn't** changed the schema or source of the data for our application

---------

### Functionalities Added or Removed

**Added Functionalities:**

- The project focused on adding robust features such as album search, user ratings, social following, and dynamic playlists to ensure a rich user experience and extensive user interaction capabilities.

**Removed or Unimplemented Functionalities:**

- Functionality to modify playlists (adding/removing tracks) was planned but not implemented due to time constraints and prioritization of foundational features that support the core objectives of the platform.

-------

### Complementation of advanced database programs

In our project design, we have found the integration of stored procedures and transactions to be extremely beneficial. These tools have added a vital layer of abstraction to our database functionality, enhancing both the robustness and efficiency of our systems. By encapsulating complex operations into stored procedures, we’ve streamlined process execution and maintenance, while transactions ensure data integrity and consistency even under concurrent access scenarios. This approach has significantly improved our project's performance and reliability.

### Technical Challenges and Solutions

**Technical Challenge Encountered:**

### Tass Hu

1. Integration of a User Profile System

- **Challenge:** Setting up a user profile page that dynamically displays user data, including followers, following, and playlists. 

- **Solution:** Implemented AJAX calls to fetch data from the backend dynamically using JavaScript. Ensured that elements like followers, following, and playlists were dynamically updated by fetching user-specific data upon loading the profile page.

2. Debugging JavaScript Execution Issues

- **Challenge:** JavaScript functions not executing as expected due to issues with DOMContentLoaded event not triggering. 
- **Solution:** Advised moving script tags to the bottom of the HTML document and using `window.onload` to ensure all elements are loaded before scripts execute, resolving issues with JavaScript functionality being unavailable at runtime.

### Tianyi Huang

1. Store procedure and transaction design

+ **Challenge**: My goal include design and implement stored procedures and transactions, while maintaining data integrity and handling potential errors gracefully. The operations involved multiple steps, including updating various tables and handling conditions where the operation could fail (e.g., trying to rate an album that doesn’t exist). Designing them hence become tricky.
+ **Solution**: Each stored procedure was designed to execute within a database transaction. This approach ensured that all steps within a procedure would either complete successfully or completely roll back in case of an error, thus maintaining data integrity.

2. Distributing Frontend Workload Among Team Members to Avoid Dependency Issues

+ **Chanllenge**: In the development of the music platform, multiple frontend features needed to be implemented simultaneously, such as user profiles, search functionalities, playlists, and recommendations. These features were interdependent; for example, the playlist functionality might depend on user authentication, and the recommendation system might need data from user profiles.
+ **Solution:** To effectively address these challenges, I implemented a strategy to split the frontend tasks into smaller, more atomic components that could be developed independently. Each major feature was broken down into the smallest possible independent tasks. For example, instead of one large task to build the user profile system, it was divided into sub-tasks such as creating the user profile UI, fetching data from the backend, and handling user inputs.

### Eric Modesitt

- **Challenge**: Connecting two mostly independent components (initial front end and extensively SQL code) 
- **Solution**: Carefully seek out and read documentation related to how to design and connect these components. Challenge: Integrating a rating system with an incomplete album or track details page Solution: Make a separate page for rating, so that both tasks can be done asynchronously

### Taylor Ziegler

1. Recommendation system design:

    - **Challenge**: design a recommendation system that can take into account shared taste between users. 
- **Solution:** By representing a user with a vector of their reviews, I was able to calculate the similarity of two users based on the cosine similarity of these reviews (i.e. reviews_a * reviews_b / |reviews_a| * |reviews_b|). Once I had established this technique for similarity between two users, I created a covariance matrix that represented the relationship between all users. Every time the user wanted to generate a list of recommendations for a user, a markov chain would determine a list of users that were most similar to the ones I wanted to generate reviews for. Finally, I got a list of the albums that these similar users rated well and used those as recommended albums. 

2. Recommendation system: optimization:

- **Challenge**: The recommendation system runs slowly due to the number of DB calls being made.
- **Solution:** The recommendation system runs slowly due to the number of DB calls being made Solution: when generating the markov chain, make all DB queries at the very start, representing them as a dictionary (user ID -> review). Then, calculate the covariance matrix. This sped up the algorithm to a reasonable time. Worked on: recommendation system.

----------

### Comparison with Original Proposal and Future Work

**Changes from Original Proposal:**

- The final implementation closely aligns with the original proposal, with minor deviations in playlist management functionalities due to prioritization decisions.

**Recommendations for Future Improvements:**

1. **Playlist Page Development:** Implementing a dedicated playlist management page would significantly enhance user interaction.
2. **Advanced Playlist Editing Features:** Enabling users to add and remove tracks from playlists would offer more flexibility and control over their music experience.
3. **Enhanced Recommendation Algorithms:** Further refinement and sophistication of the recommendation algorithms could provide more accurate and personalized content suggestions.
4. **User Interface Improvements:** Continuous improvement of the user interface to make it more intuitive and engaging.
5. **Scalability Considerations:** As the platform grows, scaling the database and backend to handle increased load and data volume will be crucial.

---

### Work Distribution

| Work                  | people                              |
| --------------------- | ----------------------------------- |
| Database Design       | yunfanh2, tianyih5                  |
| Recommendation System | rzieg3                              |
| Frontend              | ericjm4, yunfanh2, tianyih5         |
| Backend router Design | tianyih5, yunfanh2                  |
| CRUD Implement        | yunfanh2, tianyih5,ericjm4          |
| API Implement         | tianyih5, yunfanh2, rzieg3, ericjm4 |

### How well you managed teamwork

We have successfully managed teamwork in various settings. We focus on clear communication, setting shared goals, and ensuring everyone's voice is heard, which has led to high-performing teams and successful project outcomes. 