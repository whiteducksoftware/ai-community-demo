# Requirements: Simple Task Management Web Application

## Functional Requirements

* **FR1: Create Task:**
    * As a user, I want to be able to add a new task.
    * A task must have a title (mandatory, max 100 characters).
    * A task can optionally have a description (max 500 characters).
* **FR2: View Tasks:**
    * As a user, I want to see a list of all active tasks.
    * Each task in the list should display its title and completion status.
* **FR3: Mark Task as Complete:**
    * As a user, I want to be able to mark an incomplete task as complete.
    * Completed tasks should be visually distinguishable (e.g., strike-through).
* **FR4: Delete Task:**
    * As a user, I want to be able to delete a task permanently.
    * A confirmation prompt should appear before deletion.

## Non-Functional Requirements

* **NFR1: Performance:**
    * The application should respond to user actions within 1 second under normal load (single user).
* **NFR2: Usability:**
    * The user interface should be intuitive and easy to navigate.
    * Form fields should have clear labels.
* **NFR3: Maintainability:**
    * The codebase should be well-structured and commented.
    * Follow standard coding conventions for React, Node.js, and Express.
* **NFR4: Security (Basic):**
    * Prevent basic XSS attacks (e.g., by sanitizing user input).
    * No authentication/authorization required for this demo.

## User Interface (UI) Requirements

* **UIR1: Task Input Form:** A clear input field for the task title and a textarea for the description. A "Add Task" button.
* **UIR2: Task List Display:** Tasks should be displayed as a list (e.g., `<ul><li>`). Each list item should contain the task title, a checkbox/button for completion, and a delete button.
* **UIR3: Visual Feedback:** Provide visual feedback on task completion (e.g., strikethrough, change of color).
* **UIR4: Responsive Design:** The application should be usable on common desktop browser sizes (basic responsiveness, no complex mobile layouts required for this demo).