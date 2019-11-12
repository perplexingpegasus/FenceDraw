import React from "react";
import dims from '../common/dims.js';
import ConfirmDelete from "../common/ConfirmDelete"
import TopTitleContainer from "../common/TopTitleContainer";


const editorTopContainerStyle = {
    width: dims.border_width,
    height: '146pt',
    top: dims.y_margin,
    left: dims.x_margin,
    zIndex: 10
};

const PdfEditorTopContainer = props => (
    <div className="editorTopContainer" style={editorTopContainerStyle}>

        <div className="editorTopBox topBox useBorder">

            <TopTitleContainer username={props.username} filename={props.filename}/>

            <div className="editorButtonContainer topButtonContainer">

                <div className="editorButtonGroup">
                    <button
                        className="switchDrawing-button buttonWhite"
                        onClick={props.goToDrawingList}>Go To Drawing List</button>

                    <button
                        className="saveDrawing-button buttonWhite"
                        onClick={props.savePage}>Save Drawing</button>

                    <button
                        className="downloadPdfButton buttonWhite"
                        onClick={props.downloadPdf}>Download PDF</button>
                </div>

                <div className="editorButtonGroup">

                    {(props.nPages > 1) && <ConfirmDelete deleteFunc={props.deletePage} text={'Delete Page'}/>}

                    <button className="newPageButton buttonBlack" onClick={props.createPage}>New Page</button>

                    <p className='selectLabel'>Page:</p>

                    <select className="pageSelect buttonBlack"
                            onChange={props.selectPage}
                            value={props.currentPage}>

                        {Array.from({length: props.nPages}, (value, key) => key + 1)
                            .map(pageN => (
                            <option key={pageN} value={pageN}>{pageN}</option>
                        ))}

                    </select>

                </div>

            </div>

        </div>

    </div>
);

export default PdfEditorTopContainer;