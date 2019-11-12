import React, { Component } from 'react';


export default class ConfirmDelete extends Component {

    constructor(props) {
        super(props);
        this.state = {confirmIsVisible: false};
        this.showConfirm = this.showConfirm.bind(this);
        this.hideConfirm = this.hideConfirm.bind(this);
        this.handleClickOutside = this.handleClickOutside.bind(this);
    }

    componentWillMount() {
        document.addEventListener('mousedown', this.handleClickOutside, false)
    }

    componentWillUnmount() {
        document.removeEventListener('mousedown', this.handleClickOutside, false)
    }

    handleClickOutside(e) {
        if (this.node.contains(e.target)) return;
        this.hideConfirm();
    }

    showConfirm() {
        this.setState({confirmIsVisible: true})
    }

    hideConfirm() {
        this.setState({confirmIsVisible: false})
    }

    render() {
        return (
            <div ref={node => this.node = node} className='confirmDeleteContainer'>
                {this.state.confirmIsVisible ? (

                    <div className='confirmContainer'>

                        <p className='confirmText'>Are you sure?</p>
                        <button
                            className='yesButton buttonWhite'
                            onClick={() => {
                                this.props.deleteFunc();
                                this.hideConfirm();
                            }}>Yes</button>
                        <button
                            className='noButton buttonWhite'
                            onClick={this.hideConfirm}>No</button>

                    </div>

                ) : (

                    <button
                        className='deleteButton buttonBlack'
                        onClick={this.showConfirm}>{this.props.text}</button>

                )}
            </div>
        )
    }
};