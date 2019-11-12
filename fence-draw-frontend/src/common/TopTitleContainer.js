import React from "react";


const TopTitleContainer = props => (
    <div className="topTitleContainer">

        <p className="title28">F E N C E  D R A W</p>
        <div className="userInfoContainer">

            {(props.username) !== null &&
            <p className="usernameDisplay title18 limitOverflow">
                {`user: ${props.username}`}</p>
            }

            {(props.filename) !== null &&
            <p className="filenameDisplay title18 limitOverflow">
                {`drawing: ${props.filename}`}</p>
            }

        </div>
    </div>
);

export default TopTitleContainer;