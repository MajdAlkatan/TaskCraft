import React from 'react';
import './MemberList.css';

const members = [
    { name: 'Upashna Gurung', email: 'upgavygrg332@gmail.com', role: 'Can edit', avatar: '/avatars/upashna.png' },
    { name: 'Jeremy Lee', email: 'jeremylee1996@gmail.com', role: 'Can edit', avatar: '/avatars/jeremy.png' },
    { name: 'Thomas Park', email: 'parkth0123@gmail.com', role: 'Owner', avatar: '/avatars/thomas.png' },
    { name: 'Rachel Takahasi', email: 'takahasirae32@gmail.com', role: 'Can edit', avatar: '/avatars/rachel.png' },
];

const MemberList = () => {
    return (
        <ul className="member-list">
            {members.map((member, index) => (
                <li key={index} className="member-item">
                    <img src={member.avatar} alt={member.name} className="member-avatar" />
                    <div className="member-info">
                        <span className="member-name">{member.name}</span>
                        <span className="member-email">{member.email}</span>
                    </div>
                    <span className="member-role">{member.role}</span>
                </li>
            ))}
        </ul>
    );
};

export default MemberList;
