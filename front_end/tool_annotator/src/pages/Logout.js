import React from "react";
import AuthService from "../services/auth.service";
import {useHistory} from 'react-router-dom';

function Logout() {
    const history = useHistory();
    AuthService.logout();
    history.push('/');


    return (
        <div></div>
    );
}

export default Logout;