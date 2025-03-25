import React from 'react';
import Card from "../../Components/Card/Card";
import Sidebar from './Section/SideBar/SideBar';
import Header from './Section/Header/Header';
import { FaList, FaPlus } from 'react-icons/fa';
import Statistics from "../../Components/Statistics/Statistics";
import "./DashBoard.css";

function DashBoard() {
    return (
        <div className='dashboard'>
            <Header />

            <div className='main-content'>
                <Sidebar />
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
                            <Statistics title="Tasks Completed" />
                            <Statistics title="Tasks In Progress" />
                            <Statistics title="Tasks Pending" />
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
        </div>
    )
}

export default DashBoard;
