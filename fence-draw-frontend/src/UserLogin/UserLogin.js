import React, { Component } from 'react';
import './UserLogin.css'
import axios from "axios";


export default class UserLogin extends Component {

    constructor(props) {
        super(props);
        this.state = {
            messageText: "",
            usernameInput: ""
        };
        this.registerUser = this.registerUser.bind(this);
        this.loginUser = this.loginUser.bind(this);
        this.handleUsernameInputChange = this.handleUsernameInputChange.bind(this);
    };

    registerUser() {
        const username = this.state.usernameInput;
        if (username === "") return;

        axios.post(`${this.props.apiUrl}/users`, {username: username}).then(response => {

            this.setState({
                messageText: `registered user <i>${username}</i><br/>click "Login" to go to drawings`
            });
            console.log(response.data);

        }).catch(error => {

            this.setState({
                messageText: `user <i>${username}</i> already exists<br/>click "Login" to go to drawings`
            });
            console.log(error.response.data);

        })
    }

    loginUser() {
        const username = this.state.usernameInput;
        if (username === "") return;

        axios.get(`${this.props.apiUrl}/users/${username}`).then(response => {

            this.props.setUsername(username);
            console.log(response.data);

        }).catch(error => {

            this.setState({
                messageText: `user <i>${username}</i> does not exist`
            });
            console.log(error.message);

        })
    }

    handleUsernameInputChange(e) {
        this.setState({usernameInput: e.target.value})
    }

    render() {
        return (
            <div className="userLoginContainer useBorder">

                <div className="titleContainer">
                    <p className="title28">F E N C E  D R A W</p>
                </div>

                <div className="userLoginSection useBorder">
                    <input
                        className="userLoginTextInput"
                        type="text"
                        name="username"
                        value={this.state.usernameInput}
                        onChange={this.handleUsernameInputChange}
                        placeholder="enter username"
                    />
                </div>

                <div className="userLoginSection useBorder">
                    <button
                        className="registerUserButton buttonBlack"
                        onClick={this.registerUser}>Register User</button>
                    <button
                        className="loginUserButton buttonBlack"
                        onClick={this.loginUser}>Login</button>
                </div>

                <div>
                    <p className="message" dangerouslySetInnerHTML={{ __html: this.state.messageText }}/>
                </div>

            </div>
        )
    }
}