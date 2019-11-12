import React from 'react';


const CreateDrawingContainer = props => (
    <div className="createDrawingContainer">

        <div className="createDrawingInput">
            <input
                className="createDrawingTextInput"
                type="text"
                name="filename"
                value={props.filenameInput}
                onChange={props.handleFilenameInputChange}
                placeholder="enter drawing name"/>
        </div>

        <div className="createDrawingButtons">
            <button
                className="cancelButton buttonWhite"
                onClick={props.hideCreateDrawingContainer}>Cancel</button>
            <button
                className="createButton buttonWhite"
                onClick={props.createDrawing}>Create Drawing</button>
        </div>

    </div>
);

export default CreateDrawingContainer;