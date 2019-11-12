import React, { Component } from 'react';
import axios from "axios";
import dims from '../common/dims.js';


const imageSelectorStyle = {
    width: dims.col3_w,
    height: '396pt',
    top: '164pt',
    right: dims.x_margin,
    position: 'absolute',
    zIndex: 10
};

export default class ImageSelector extends Component {

    constructor(props) {
        super(props);

        this.state = {
            uniqueHeights: [],
            uniqueCategories: [],
            fenceImgs: []
        };

        this.handleHeightChange = this.handleHeightChange.bind(this);
        this.handleImgTypeChange = this.handleImgTypeChange.bind(this);
    }

    componentDidMount() {
        axios.get(`${this.props.apiUrl}/fence_images`).then(response => {

            this.setState(response.data);
            this.setState({
                height: response.data.uniqueHeights[0],
                imgType: response.data.uniqueCategories[0]
            });

        }).catch(error => console.log(error));
    }

    handleHeightChange(e) {
        this.setState({height: e.target.value})
    }

    handleImgTypeChange(e) {
        this.setState({imgType: e.target.value})
    }

    render() {
        return (
            <div className='imageSelector useBorder' style={imageSelectorStyle}>

                <div className='imageSelectorDropdowns'>

                    <p className='selectLabel'>Height (ft):</p>

                    <select
                        className='buttonWhite'
                        onChange={this.handleHeightChange}>
                        {this.state.uniqueHeights.map(height =>
                            <option key={height} value={height}>{height}</option>)}
                    </select>

                    <p className='selectLabel'>Category:</p>

                    <select
                        className='buttonWhite' onChange={this.handleImgTypeChange}>
                        {this.state.uniqueCategories.map(category =>
                            <option key={category} value={category}>{category}</option>)}
                    </select>

                </div>

                <div className='selectorList'>
                    {this.state.fenceImgs.map(fenceImg =>
                        (fenceImg.height == this.state.height) &&
                        (fenceImg.category === this.state.imgType) &&
                        <button
                            key={fenceImg.id}
                            className='buttonGrey'
                            onClick={() => this.props.handleImageChange(fenceImg.id, fenceImg.height)}
                            value={fenceImg.id}
                        >{fenceImg.name}</button>
                    )}
                </div>

            </div>
        )
    }

}