import React, { useState } from 'react';
import Card from "../../Components/Card/Card";
import Sidebar from './Section/SideBar/SideBar';
import Header from './Section/Header/Header';
import { FaList, FaPlus } from 'react-icons/fa';
import Statistics from "../../Components/Statistics/Statistics";
import "./DashBoard.css";
import WelcomeBack from './Section/WelcomeBack/WelcomeBack';
import Invite from './Section/Invite/Invite';

function DashBoard() {
    const [isInviteOpen, setInviteOpen] = useState(false); // State to manage dialog visibility
    const handleInviteClick = () => {
        setInviteOpen(true); // Open the invite dialog
    };

    const handleCloseInvite = () => {
        setInviteOpen(false); // Close the invite dialog
    };

    return (
        <div className='dashboard'>
            <WelcomeBack onInviteClick={handleInviteClick} />
            {isInviteOpen && <Invite onClose={handleCloseInvite} />}
            <div className="main-workspace">
                <div className="To-Do">
                    <div className="up">
                        <div className="title-To-Do">
                            <FaList />
                            <h1> To Do</h1>
                        </div>
                        <button className='addtask'>
                            <FaPlus />
                            add task
                        </button>
                    </div>
                    <Card
                        title="Attend Nischal’s Birthday Party"
                        description="Buy gifts on the way and pick up cake from the bakery. (6 PM | Fresh Elements)"
                        priority="Moderate"
                        status="Not Started"
                        date="created on : 20/06/2023"
                        image="birthday.jpg"
                        statusColor="red"
                    />
                    <Card
                        title="Attend Nischal’s Birthday Party"
                        description="Buy gifts on the way and pick up cake from the bakery. (6 PM | Fresh Elements)"
                        priority="Moderate"
                        status="in progress"
                        date=" created on :20/06/2023"
                        image="birthday.jpg"
                        statusColor="red"
                    />
                </div>

                {/* Right Workspace */}
                <div className='right-workspace-section'>
                    <div className="statistics">
                        <Statistics
                            title="Chart 1"
                            values={[Math.floor(Math.random() * 10) + 5, Math.floor(Math.random() * 10) + 5]} // Dynamic values
                            colors={['#FF0000', '#cfcfcfbe']} // Red and Gray
                        />

                        <Statistics
                            title="Chart 2"
                            values={[Math.floor(Math.random() * 10) + 5, Math.floor(Math.random() * 10) + 5]}
                            colors={['#0000FF', '#cfcfcfbe']} // Blue and Gray
                        />

                        <Statistics
                            title="Chart 3"
                            values={[Math.floor(Math.random() * 10) + 5, Math.floor(Math.random() * 10) + 5]}
                            colors={['#008000', '#cfcfcfbe']} // Green and Gray
                        />


                    </div>
                    <div className="completed-task">
                        <Card
                            title="Attend Nischal’s Birthday Party"
                            description="Buy gifts on the way and pick up cake from the bakery. (6 PM | Fresh Elements)"
                            status="Completed"
                            date="Completed 2 days ago"
                            image="birthday.jpg"
                            statusColor="green"
                        />
                        <Card
                            title="Attend Nischal’s Birthday Party"
                            description="Buy gifts on the way and pick up cake from the bakery. (6 PM | Fresh Elements)"
                            status="Completed"
                            date="Completed 2 days ago"
                            image="birthday.jpg"
                            statusColor="green"

                        />
                    </div>
                </div>
            </div>
        </div>
    )
}

export default DashBoard;
