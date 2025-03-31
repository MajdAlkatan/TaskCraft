import React from 'react'
import FormButton from '../../Components/Button/FormButton/FormButton'
import TaskTableCategory from '../../Components/Button/TaskTableCategory/TaskTableCategory'
import "./TaskCategories.css"
function TaskCategories() {
    return (
        <div className='taskCategoriesss'>
            <section className='catHeadr'>
                <h2>Task Categries</h2>
                <FormButton label='Add Category' />

            </section>
            <section>
                <TaskTableCategory />
            </section>
        </div>
    )
}

export default TaskCategories