import React from 'react';
import ConfirmDelete from '../common/ConfirmDelete'


const DrawingListItem = props => (
    <div className='drawingListItemContainer'>

        <p className='drawingLabel limitOverflow'>{props.filename}</p>
        <div className='editDeleteButtonContainer'>

            <ConfirmDelete deleteFunc={props.deleteDrawing}
                           text={'Delete'}/>
            <button className='editButton buttonBlack' onClick={props.editDrawing}>Edit</button>

        </div>
    </div>
);

export default DrawingListItem;