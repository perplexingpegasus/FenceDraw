import React, { Component } from 'react';


export default class TextEditorBox extends Component {

    render() {
        const textWrapperStyle = {
            width: this.props.config.width,
            height: this.props.config.height,
            left: this.props.config.x,
            bottom: this.props.config.y,
            padding: this.props.config.padding
        };

        const fontStyle = {
            fontSize: this.props.config.font_size,
            fontWeight: this.props.config.font_weight,
            textAlign: this.props.config.alignment
        };

        return (
            <div className={`textWrapper ${this.props.config.border ? "useBorder" : ""}`}
                 style={textWrapperStyle}>

                {this.props.takesInput ? (
                    <textarea
                        className="pdfTextInput"
                        value={this.props.value}
                        onChange={this.props.handleTextChange}
                        style={fontStyle}/>
                ) : (
                    <p
                        className="fixedText"
                        style={fontStyle}
                        dangerouslySetInnerHTML={{ __html: this.props.config.default_text }}/>
                )}

            </div>
        )
    }
}