import axios from "axios";

const API_URL = '/user/';

const register = (first_name, last_name, email, password) => {
    return axios.post(API_URL + 'signup' , {
        first_name: first_name,
        last_name: last_name,
        email: email,
        password: password
    });
};

const login = (email, password) => {
    return axios.post(API_URL + 'signin', {
        email: email,
        password: password,
    })
    .then ((reponse) => {
        if (reponse.data.access_token) {
            localStorage.setItem('user', JSON.stringify(reponse.data));
        }

        return reponse.data;
    });
};

const logout = () => {
    localStorage.removeItem('user');
};

const getCurrentUser = () => {
    return JSON.parse(localStorage.getItem('user'));
};

export default {
    register,
    login,
    logout,
    getCurrentUser,
};