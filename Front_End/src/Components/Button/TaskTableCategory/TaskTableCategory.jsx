import React from 'react';
import './TaskTableCategory.css'; // Import your CSS file for styling

const TaskTableCategory = () => {
    const tasks = [
        { id: 1, status: 'Completed' },
        { id: 2, status: 'In Progress' },
        { id: 3, status: 'Not Started' },
    ];

    const handleEdit = (id) => {
        console.log(`Edit task with ID: ${id}`);
    };

    const handleDelete = (id) => {
        console.log(`Delete task with ID: ${id}`);
    };

    return (
        <div className="task-status-container">
            <div className="task-stat-header">
                <h2>Task Status</h2>
                <button className="add-task-button"><span>+</span> Add Task Status</button>
            </div>
            <table className="task-status-table">
                <thead>
                    <tr>
                        <th>SN</th>
                        <th>Task Status</th>
                        <th>Action</th>
                    </tr>
                </thead>
                <tbody>
                    {tasks.map((task, index) => (
                        <tr key={task.id}>
                            <td>{index + 1}</td>
                            <td>{task.status}</td>
                            <td>
                                <button onClick={() => handleEdit(task.id)} className="edit-button">Edit</button>
                                <button onClick={() => handleDelete(task.id)} className="delete-button">Delete</button>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default TaskTableCategory;