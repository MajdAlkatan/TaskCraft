import React, { useState } from "react";
import Card from "../../Components/Card/Card"; // Import the Card component
import IconButton from "../../Components/Button/IconButton/IconButton"; // Import IconButton
import { FaTrash, FaEdit } from "react-icons/fa"; // Import icons
import "./MyTask.css";

const tasks = [
  {
    id: 1,
    title: "Submit Documents",
    description: "Make sure to submit all the necessary documents...",
    priority: "Extreme",
    status: "Not Started",
    date: "20/06/2023",
    image: "https://via.placeholder.com/100",
    details: `**Task Title:** Document Submission.
    
**Objective:** To submit required documents for something important.

**Task Description:** Review the list of documents required for submission and ensure all necessary documents are ready. Organize the documents accordingly and scan them if physical copies need to be submitted digitally. Rename the scanned files appropriately for easy identification and verify the accepted file formats. Upload the documents securely to the designated platform, double-check for accuracy, and obtain confirmation of successful submission. Follow up if necessary to ensure proper processing.

**Additional Notes:**
- Ensure that the documents are authentic and up-to-date.
- Maintain confidentiality and security of sensitive information during the submission process.
- If there are specific guidelines or deadlines for submission, adhere to them diligently.

**Deadline for Submission:** End of Day`,
  },
  {
    id: 2,
    title: "Complete Assignments",
    description: "The assignments must be completed to pass final year...",
    priority: "Moderate",
    status: "In Progress",
    date: "20/06/2023",
    image: "https://via.placeholder.com/100",
    details: `**Task Title:** Assignment Completion.

**Objective:** To complete assignments for final year.

**Task Description:** Ensure all assignments are completed and submitted before the final deadline. Double-check the requirements for each subject and review any feedback from instructors.

**Deadline:** 25/06/2023`,
  },
];

function MyTask() {
  const [selectedTask, setSelectedTask] = useState(tasks[0]); // Default task

  return (
    <div className="my-task-container">
      {/* Left Side: Task List */}
      <div className="task-list">
        <h2>My Tasks</h2>
        {tasks.map((task) => (
          <div
            key={task.id}
            onClick={() => setSelectedTask(task)}
            className={`task-item ${selectedTask.id === task.id ? "active" : ""}`}
          >
            <Card
              title={task.title}
              description={task.description}
              priority={task.priority}
              status={task.status}
              date={task.date}
              image={task.image}
            />
          </div>
        ))}
      </div>

      {/* Right Side: Task Details */}
      <div className="task-details">
        <div className="main-title-task-details">
          <img src={selectedTask.image} alt="" className="task-detail-image" />
          <div className="main-grid-task-detailes">
            <h5>{selectedTask.title}</h5>
            <p><b>Priority:</b> {selectedTask.priority}</p>
            <p><b>Status:</b> {selectedTask.status}</p>
            <p><b>Created on:</b> {selectedTask.date}</p>
          </div>
        </div>

        <div className="task-full-details">
          <p className="detailes-task-full" dangerouslySetInnerHTML={{ __html: selectedTask.details.replace(/\n/g, "<br>") }}></p>
        </div>

        {/* Icon Buttons: Edit & Delete */}
        <div className="task-actions">
          <IconButton icon={FaEdit} onClick={() => alert("Edit task")} />
          <IconButton icon={FaTrash} onClick={() => alert("Delete task")} />
        </div>
      </div>
    </div>
  );
}

export default MyTask;
