import React, {useState, useEffect} from "react";
import {Link} from 'react-router-dom';
import bookService from "../services/book.service";
import {getAPI} from '../common/APICaller';
import axios from "axios";

function ListBook() {
    const [books, setBooks] = useState([]);
    const [imageStream, setImageStream] = useState('');

    useEffect(()=>{
        getAPI('/books', function(res){
            setBooks(res.data.results);
        })
        // const imageUrl = await (axios.get('/book/1. 55-13 (03-165).png'));
        // setImageStream(imageUrl);
        // getImageUrl();
    },[]);
    console.log(books);
    console.log(imageStream);

    // const getImageUrl = () => {
    //     axios.get('/book/uploads/1. 55-13 (03-165).png').then(
    //         (res) => {
    //             setImageStream(res.data);
    //         }
    //     )
    // }


    return (
        <div>
            {books.map(book => (
                <div className="list-inline-item" key={book.book_id}>
                
                    <div className="card" style={{width: "10rem", height: "15rem", margin: "20px"}}>
                        <img className="card-img-top" style={{width:"8rem", height: "10rem", margin: "0 auto"}}
                             src={`http://localhost:5000/book/uploads/Lien_Phai.jpg`} alt="Card image cap" />
                        {/* <Link to={`/book/${book.book_id}`}>
                            <div className="card-body" style={{margin: "0 auto"}}>
                                <a href="#" className="btn btn-primary">Xem chi tiết</a>
                            </div>
                        </Link> */}
                    </div>
                </div>
            ))}
        </div>
    );

}

export default ListBook;