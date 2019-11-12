import React, { Component } from 'react';
import TopTitleContainer from '../common/TopTitleContainer'
import CreateDrawingContainer from './CreateDrawingContainer'
import DrawingListItem from './DrawingListItem'
import './DrawingList.css'
import axios from "axios";


export default class DrawingList extends Component {

    constructor(props) {
        super(props);
        this.state = {
            messageText: "",
            filenameInput: "",
            createDrawingIsVisible: false,
            drawingNames: []
        };

        this.showCreateDrawingContainer = this.showCreateDrawingContainer.bind(this);
        this.hideCreateDrawingContainer = this.hideCreateDrawingContainer.bind(this);
        this.createDrawing = this.createDrawing.bind(this);
        this.handleFilenameInputChange = this.handleFilenameInputChange.bind(this);
        this.switchUser = this.switchUser.bind(this);
    };

    componentDidMount() {
        axios.get(`${this.props.apiUrl}/users/${this.props.username}/drawings`).then(response => {

            response.data.map(drawing =>
                this.setState({drawingNames: [...this.state.drawingNames, drawing.filename]}));
            console.log(response.data);

            if (this.state.drawingNames.length === 0) {
                this.setState({messageText: `no drawings to display<br/>press "New Drawing" to make a drawing`});
            }

        }).catch(error => console.log(error));
    }

    showCreateDrawingContainer() {
        this.setState({createDrawingIsVisible: true})
    }

    hideCreateDrawingContainer() {
        this.setState({createDrawingIsVisible: false})
    }

    handleFilenameInputChange(e) {
        this.setState({filenameInput: e.target.value})
    }

    createDrawing() {
        const filename = this.state.filenameInput;
        if (filename === "") return;

        axios.post(`${this.props.apiUrl}/users/${this.props.username}/drawings`,
            {filename: filename, pages: []}).then(response => {

                this.editDrawing(filename);
                console.log(response.data);

        }).catch(error => console.log(error))
    }

    editDrawing(filename) {
        this.props.setFilename(filename);
    }

    deleteDrawing(filename) {
        axios.delete(`${this.props.apiUrl}/users/${this.props.username}/drawings/${filename}`).then(response => {

            this.setState({drawingNames: this.state.drawingNames.filter(name => name !== filename)});
            this.setState({messageText: `drawing ${filename} deleted`});
            console.log(response.data);

        }).catch(error => console.log(error))
    }

    switchUser() {
        this.props.setUsername(null);
    }

    render() {
        return (
            <div className="drawingList">
                <div className="drawingListTopContainer drawingListContent useBorder">
                    <div className="drawingListTopBox topBox">

                        <TopTitleContainer username={this.props.username} filename={null}/>

                        <div className="drawingListButtonContainer topButtonContainer">
                            <button
                                className="newDrawingButton buttonGrey"
                                onClick={this.showCreateDrawingContainer}>New Drawing</button>
                            <button
                                className="switchUserButton buttonGrey"
                                onClick={this.switchUser}>Switch User</button>
                        </div>

                    </div>
                </div>

                <div className="drawingListMainContent drawingListContent useBorder">

                    {this.state.createDrawingIsVisible && (
                        <CreateDrawingContainer
                            filenameInput={this.state.filenameInput}
                            handleFilenameInputChange={this.handleFilenameInputChange}
                            hideCreateDrawingContainer={this.hideCreateDrawingContainer}
                            createDrawing={this.createDrawing}
                        />
                    )}

                    <p className="message" dangerouslySetInnerHTML={{ __html: this.state.messageText }}/>

                    <div className="drawings">{this.state.drawingNames.map(drawingName =>
                        <DrawingListItem
                            key={drawingName}
                            filename={drawingName}
                            editDrawing={this.editDrawing.bind(this, drawingName)}
                            deleteDrawing={this.deleteDrawing.bind(this, drawingName)}/>
                    )}</div>

                </div>

            </div>

        )
    }
}