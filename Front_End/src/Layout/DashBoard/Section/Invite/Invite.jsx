import React from 'react';
import './Invite.css'; // Import the CSS file
import DefulteInput from "../../../../Components/Input/DefulteInput/DefulteInput";
import FormButton from '../../../../Components/Button/FormButton/FormButton';

function Invite({ onClose }) {
    return (
        <dialog className='invite-dialog'>
            <header className='invite-header'>
                <h2 className='invite-title'>Send an invite to a new member</h2>
                <button className='invite-close-button' onClick={onClose}>Go Back</button>
            </header>
            <div className="invite-body">
                <div className="invite-email">
                    <DefulteInput
                        placeholder='example@gmail.com'
                        label={'Email'}
                        type='Email'
                        className='invit-input'

                    />
                    <FormButton
                        label='Send Invite'
                    />
                </div>
                <div className="invite-members">
                    <p className="invite-members-title">Members</p>
                </div>
            </div>
        </dialog>
    );
}

export default Invite;