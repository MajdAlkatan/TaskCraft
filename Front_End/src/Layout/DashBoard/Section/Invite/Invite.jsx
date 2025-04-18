import React from 'react';
import './Invite.css';
import DefulteInput from '../../../../Components/Input/DefulteInput/DefulteInput';
import FormButton from '../../../../Components/Button/FormButton/FormButton';
import MemberList from '../../../../Components/MemberList/MemberList';
import ProjectLink from '../../../../Components/ProjectLink/ProjectLink';

function Invite({ onClose }) {
    return (
        <div className="invite-overlay">
            <dialog open className='invite-dialog'>
                <header className='invite-header'>
                    <h2 className='invite-title'>Send an invite to a new member</h2>
                    <button className='invite-close-button' onClick={onClose}>Go Back</button>
                </header>

                <div className="invite-body">
                    <div className="invite-email">
                        <DefulteInput
                            placeholder='neerajgurung99@gmail.com'
                            label='Email'
                            type='email'
                            className='invit-input'
                        />
                        <FormButton label='Send Invite' />
                    </div>

                    <div className="invite-members">
                        <p className="invite-members-title">Members</p>
                        <MemberList />
                    </div>

                    <ProjectLink />
                </div>
            </dialog>
        </div>
    );
}

export default Invite;
