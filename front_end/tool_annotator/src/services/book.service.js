import axios from "axios";

const API_URL = '/book/upload'

const uploadBook = (filename, title, user_id, annotation) => {
    const formData = new FormData();
    formData.append('inputFile', filename)
    // TODO: add user_id, now for simple use default user_id
    formData.append('user_id', user_id);
    formData.append('title', title)
    return axios.post(API_URL, formData);
}

const getAllBook = () => {
    axios.get('/books').then(
        (response) => {
            return response.data.results;
        }
    )
}

const getPage = (filename) => {
    axios.get(`/api/image/getlabel/${filename}`).then(
        (res) => {
            return res.data.data;
        }
    )
}

export default {
    getAllBook,
    uploadBook,
    getPage
};