import React, { Component } from 'react';
import axios from "axios";

import PdfEditorTopContainer from './PdfEditorTopContainer'
import DescriptionSelector from './DescriptionSelector'
import ImageSelector from './ImageSelector'
import TextEditorBox from './TextEditorBox'
import dims from '../common/dims.js';
import text_config from '../common/text_config.js'
import './PdfEditor.css'


const editorStyle = {
    width: dims.total_width,
    height: dims.total_height
};

const editorBorderStyle = {
    width: dims.border_width,
    height: dims.border_height,
    left: dims.x_margin,
    bottom: dims.y_margin
};

const fenceImgContainerStyle = {
    width: dims.col1_w,
    // border_height - top container height - (desc_h + title_h)
    height: '418pt',
    left: dims.x_margin,
    // desc_h + title_h + y_margin
    bottom: '210pt'
};

const logoImgContainerStyle = {
    width: dims.logo_w,
    height: dims.logo_h,
    left: dims.logo_x,
    bottom: dims.logo_y
};


export default class PdfEditor extends Component {

    constructor(props) {
        super(props);

        const state = {
            apiUrl: `${props.apiUrl}/users/${props.username}/drawings/${props.filename}`,
            currentPage: 1,
            nPages: 1,
            fenceImgId: null,
        };
        text_config.textarea_configs.map((config) =>
            state[config.id] = "");

        this.state = state;

        this.goToDrawingList = this.goToDrawingList.bind(this);
        this.getPage = this.getPage.bind(this);
        this.selectPage = this.selectPage.bind(this);
        this.createPage = this.createPage.bind(this);
        this.deletePage = this.deletePage.bind(this);
        this.savePage = this.savePage.bind(this);
        this.savePageBefore = this.savePageBefore.bind(this);
        this.handleImageChange = this.handleImageChange.bind(this);
        this.handleDescriptionChange = this.handleDescriptionChange.bind(this);
        this.downloadPdf = this.downloadPdf.bind(this);
    }

    componentDidMount() {
        this.getPage(this.state.currentPage);
    }

    getRequestData(newPage) {
        const requestData = {new_page: newPage};

        if (this.state.fenceImgId !== null) requestData['fence_image_id'] = this.state.fenceImgId;

        for (let i = 0; i < text_config.textarea_configs.length; i++) {
            let id = text_config.textarea_configs[i].id;
            requestData[id] = this.state[id];}
        return requestData;
    }

    getPage(pageNumber) {
        axios.get(`${this.state.apiUrl}/pages/${pageNumber}`).then(response => {

            this.setState(response.data);
            this.setState({currentPage: pageNumber});

            axios.get(this.state.apiUrl).then(response => {
                this.setState({nPages: response.data.n_pages});
            }).catch(error => console.log(error));

        }).catch(error => console.log(error));
    }

    selectPage(e) {
        const pageNumber = e.target.value;
        this.savePageBefore(() => this.getPage(pageNumber));
    }

    createPage() {
        this.savePageBefore(() => {

            const postData = this.getRequestData(true);
            axios.post(`${this.state.apiUrl}/pages`, postData).then(response => {

                this.setState({nPages: this.state.nPages + 1});
                this.getPage(response.data.page_number);

            }).catch(error => console.log(error));

        })
    }

    deletePage() {
        if (this.state.nPages <= 1) return;

        axios.delete(`${this.state.apiUrl}/pages/${this.state.currentPage}`).then(response => {

            this.setState({nPages: this.state.nPages - 1});
            this.getPage(this.state.currentPage === 1 ? 1 : this.state.currentPage - 1);

        }).catch(error => console.log(error));
    }

    savePage() {
        this.savePageBefore(null)
    }

    savePageBefore(after) {
        const putData = this.getRequestData(false);
        axios.put(`${this.state.apiUrl}/pages/${this.state.currentPage}`, putData).then(response => {

            if (after !== null) after();

        }).catch(error => console.log(error));
    }

    handleTextChange(id, e) {
        this.setState({...this.state, [id]: e.target.value})
    }

    goToDrawingList() {
        this.props.setFilename(null);
    }

    handleImageChange(id, height) {
        console.log(height);
        let titleString = this.state.title;
        const digitIdx = titleString.search(/\d/);
        if (digitIdx >= 0) { this.setState({
            title: titleString.substring(0, digitIdx) + height.toString() + titleString.substring(digitIdx + 1)
        })}
        this.setState({fenceImgId: id});
    }

    handleDescriptionChange(title, description) {
        this.setState({
            title: title,
            desc1: description
        })
    }

    // make its own component

    downloadPdf() {
        this.savePageBefore(() => {
            axios.get(`${this.state.apiUrl}/pdf`, {responseType: 'blob'}).then(response => {

                const blob = new Blob([response.data], {type: "application/pdf"});
                const downloadUrl = URL.createObjectURL(blob);
                const downloadLink = document.createElement('a');

                downloadLink.style['display'] = 'none';
                downloadLink.href = downloadUrl;
                downloadLink.download = `${this.props.filename}.pdf`;

                document.body.appendChild(downloadLink);
                downloadLink.click();
                URL.revokeObjectURL(downloadUrl);

            }).catch(error => console.log(error));
        });
    }

    //

    render() {
        return (
            <div className="editor" style={editorStyle}>

                <PdfEditorTopContainer
                    username={this.props.username}
                    filename={this.props.filename}
                    currentPage={this.state.currentPage}
                    nPages={this.state.nPages}
                    selectPage={this.selectPage}
                    createPage={this.createPage}
                    deletePage={this.deletePage}
                    savePage={this.savePage}
                    goToDrawingList={this.goToDrawingList}
                    downloadPdf={this.downloadPdf}
                />

                <DescriptionSelector handleDescriptionChange={this.handleDescriptionChange}/>

                <ImageSelector
                    apiUrl={this.props.apiUrl}
                    handleImageChange={this.handleImageChange}
                />

                <div className="editorBorder useBorder" style={editorBorderStyle}/>

                <div className="imgContainer" style={fenceImgContainerStyle}>
                    <img className="fenceImg" alt="fence" src={
                        this.state.fenceImgId === null ? (
                            require('../images/placeholder.png')
                        ) : (
                            require(`../images/${this.state.fenceImgId}.jpg`)
                        )
                    }/>
                </div>

                <div className="imgContainer" style={logoImgContainerStyle}>
                    <img
                        className="logoImg"
                        alt="logo"
                        src={require('../images/logo.png')}
                    />
                </div>

                {[text_config.textarea_configs, text_config.fixedtext_configs].map((group, group_index) =>
                    group.map((config) =>
                        <TextEditorBox
                            key={config.id}
                            config={config}
                            takesInput={group_index === 0}
                            value={this.state[config.id]}
                            handleTextChange={this.handleTextChange.bind(this, config.id)}
                        />
                ))}

            </div>
        );
    }
}