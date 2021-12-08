import React, { useState } from "react";
import BookService from '../services/book.service';
import {useHistory} from 'react-router-dom';

function UploadBook() {

    const [file, setFile] = useState();
    const [title, setTittle] = useState('');
    const [description, setDescription] = useState('');
    const history = useHistory();

    const changeDescription = (e) => {
        setDescription(e.target.value);
    };

    const changeTittle = (e) => {
        setTittle(e.target.value);
    };

    const changeFile = (e) => {
        setFile(e.target.files[0]);
    };


    const handleSubmit = () => {
        // TODO: add user_id, now for simple use default user_id
        BookService.uploadBook(file, title, 1, null);
        history.push('/')
    };


    return (
        <div>
            <h3>Tải sách mới</h3>

            <label class="form-label" for="customFile">Tên sách</label>
            <input type="text" class="form-control" id="customFile" onChange={changeTittle}/>
            
            <label class="form-label" for="customFile">Chọn file sách</label>
            <input type="file" class="form-control" id="customFile" onChange={changeFile}/>

            <label class="form-label" for="customFile">Mô tả</label>
            <textarea class="form-control" id="customFile" onChange={changeTittle}></textarea>

            <button type="submit" className="btn btn-primary btn-block" onClick={handleSubmit}>
                Submit
            </button>
            
        </div>
    )

}

export default UploadBook;