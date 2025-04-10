import React from 'react'
import DefulteInput from "../../../../Components/Input/DefulteInput/DefulteInput"
import FormButton from '../../../../Components/Button/FormButton/FormButton'
function Invite() {
    return (
        <dialog className='Invite-dialog'>
            <header>
                <h2>Send an invite to a new member</h2>
                <button>Go Back</button>
            </header>
            <div className="invite-body">
                <div className="invite-email">
                    <DefulteInput
                        placeholder='example@gmail.com'
                        label={'Email'}
                        type='Email'
                    />
                    <FormButton
                        label='Send Invite'
                    />
                </div>
                <div>
                    <p>Members</p>

                </div>
            </div>


        </dialog>
    )
}

export default Invite