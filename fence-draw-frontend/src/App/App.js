import React, { Component } from 'react';
import DrawingList from '../DrawingList/DrawingList';
import PdfEditor from '../PdfEditor/PdfEditor';
import UserLogin from '../UserLogin/UserLogin';
import './App.css'


let apiUrl = 'http://127.0.0.1:5000/api/v1';

class App extends Component {

    constructor(props) {
        super(props);
        this.state = {
            username: null,
            filename: null,
        };
        this.setUsername = this.setUsername.bind(this);
        this.setFilename = this.setFilename.bind(this);
    }

    setUsername(value) {
        this.setState({username: value});
    }

    setFilename(value) {
        this.setState({filename: value});
    }

    render() {
        return (
            <div>

                {(this.state.filename === null) || (this.state.username === null) ? (

                    (this.state.username === null) ? (

                        <UserLogin
                            apiUrl={apiUrl}
                            setUsername={this.setUsername}/>

                    ) : (

                        <DrawingList
                            apiUrl={apiUrl}
                            username={this.state.username}
                            setUsername={this.setUsername}
                            setFilename={this.setFilename}/>)

                ) : (
                    <PdfEditor
                        apiUrl={apiUrl}
                        username={this.state.username}
                        filename={this.state.filename}
                        setFilename={this.setFilename}/>)
                }

            </div>
        );
    }

}

export default App;
