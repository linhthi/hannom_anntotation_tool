import React from 'react';
import { Redirect } from 'react-router-dom';
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import Container from './components/stateless/Container';
import Message from './components/Message';
// import images from './books.json';
import axios from 'axios';

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      images: [],
      isLoading: false,
      selectedTab: 'all',
      message: {
        type: null,
        text: null,
      },
    };

    this.getImages = this.getImages.bind(this);
    this.handleImageUpload = this.handleImageUpload.bind(this);
    this.handleDeleteImage = this.handleDeleteImage.bind(this);
    this.handleTabChange = this.handleTabChange.bind(this);
    this.createMessage = this.createMessage.bind(this);
    this.resetMessage = this.resetMessage.bind(this);
  }

  componentDidMount() {
    this.getImages();
  }

  getImages() {
    // this.setState({ images: images, isLoading: false })
    // Get images from api
    axios.get('/api/images').then(
      (res) => {
        this.setState({ images: res.data.data, isLoading: false })
      }
    )
  }

  handleImageUpload({ image_url, image_file }) {
    const data = new FormData();
    data.append('image_file', image_file);
    data.append('image_url', image_url);
    this.setState({ isLoading: true });
    fetch(`${process.env.REACT_APP_API_URL}/api/images/`, {
      method: 'POST',
      body: data,
      // headers: {
      //   Authorization: `Bearer ${authToken}`,
      // },
    })
      .then(res => res.json())
      .then(res => {
        this.getImages();
        if (res.status === 'fail') {
          throw new Error('Upload failed');
        }
        this.createMessage('success', 'Image has been successfully uploaded.');
      })
      .catch(err => {
        this.createMessage('error', 'Something went wrong with the uploading.');
        this.setState({ isLoading: false });
      });
  }

  handleDeleteImage(imageName) {
    // const { authToken } = window.localStorage;
    fetch(`${process.env.REACT_APP_API_URL}/api/images/${imageName}`, {
      method: 'DELETE',
      // headers: {
      //   Authorization: `Bearer ${authToken}`,
      // },
    })
      .then(res => res.json())
      .then(res => {
        if (res.status === 'success') {
          this.getImages();
        }
      });
  }

  handleTabChange(selectedTab) {
    this.setState({ selectedTab });
  }

  createMessage(type, text) {
    this.setState(
      {
        message: {
          type,
          text,
        },
      },
      () =>
        setTimeout(() => {
          this.resetMessage();
        }, 5000)
    );
  }

  resetMessage() {
    this.setState({
      message: {
        type: null,
        text: null,
      },
    });
  }


  render() {
    const {
      images,
      isLoading,
      message,
      selectedTab,
    } = this.state;
    return (
      <Router>
      <React.Fragment>
        {/* <div className="nav-link">
          <Link to="/">Home</Link>
        </div> */}
        {message.type && message.text && (
          <Message type={message.type} text={message.text} />
        )}
        <Switch>
          <Route
            path="/images"
            render={() => (
              <Container
                onButtonClick={this.handleImageUpload}
                images={images}
                isLoading={isLoading}
                selectedTab={selectedTab}
                onTabChange={this.handleTabChange}
                onDeleteImage={this.handleDeleteImage}
                createMessage={this.createMessage}
              />
            )}
          />

          <Route exact path="/" render={() => <Redirect to="/images" />} />
        </Switch>
      </React.Fragment>
      </Router>
    );
  }
}

export default App;
