import React, { Component } from 'react';

import dims from '../common/dims.js';


const descriptionSelectorStyle = {
    width: dims.col2_w,
    height: '200pt',
    left: (parseInt(dims.x_margin) + parseInt(dims.col1_w)).toString() + 'pt',
    bottom: (parseInt(dims.y_margin) + parseInt(dims.datescale_h) * 2).toString() + 'pt',
    position: 'absolute',
    zIndex: 10
};


export default class DescriptionSelector extends Component {

    constructor(props) {
        super(props);
        this.state = {
            options: [],
            optionsAreVisible: false
        };
        this.handleClickOutside = this.handleClickOutside.bind(this);
        this.showOptions = this.showOptions.bind(this);
        this.hideOptions = this.hideOptions.bind(this);
    }

    componentWillMount() {
        document.addEventListener('mousedown', this.handleClickOutside, false)
    }

    componentWillUnmount() {
        document.removeEventListener('mousedown', this.handleClickOutside, false)
    }

    handleClickOutside(e) {
        if (this.node.contains(e.target)) return;
        this.hideOptions();
    }

    showOptions() {
        this.setState({optionsAreVisible: true})
    }

    hideOptions() {
        this.setState({optionsAreVisible: false})
    }

    render() {
        return (
            <div
                ref={node => this.node = node}
                className='descriptionSelector useBorder'
                style={descriptionSelectorStyle}
            >

                {this.state.optionsAreVisible ? (

                    <div className='selectorList'>
                        <button className='buttonBlack'>All Black System</button>
                        <button className='buttonBlack'>All Galvanized System</button>

                    </div>

                ) : (

                    <button className='buttonGrey' onClick={this.showOptions}>Select Default Description</button>

                )}

            </div>
        )
    }

}