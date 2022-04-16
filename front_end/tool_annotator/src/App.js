import React from 'react'
import { Redirect } from 'react-router-dom'
import { BrowserRouter as Router, Switch, Route } from "react-router-dom"
import Container from './components/Container'
import Message from './components/Message'
import axios from 'axios'
import API from './constant/API'
import NavBar from './components/NavBar'
import RegisterLoginForm from './components/RegisterLoginForm'

class App extends React.Component {
  constructor(props) {
    super(props)
    this.state = {
      images: [],
      currentUser: '',
      isAuthenticated: false,
      isLoading: false,
      selectedTab: 'all',
      message: {
        type: null,
        text: null,
      },
    }

    this.getImages = this.getImages.bind(this)
    this.handleImageUpload = this.handleImageUpload.bind(this)
    this.handleDeleteImage = this.handleDeleteImage.bind(this)
    this.handleTabChange = this.handleTabChange.bind(this)
    this.createMessage = this.createMessage.bind(this)
    this.resetMessage = this.resetMessage.bind(this)
  }

  componentDidMount() {
    this.getImages()
  }

  getImages() {
    // Get images from api
    axios.get(`${API.GET_ALL_IMAGES}`).then(
      (res) => {
        this.setState({ images: res.data.data, isLoading: false })
      }
    )
  }

  handleImageUpload({ image_url, image_file }) {
    const data = new FormData()
    data.append('image_file', image_file)
    data.append('image_url', image_url)
    this.setState({ isLoading: true })
    fetch(`${process.env.REACT_APP_API_URL}/api/images/`, {
      method: 'POST',
      body: data,
      // headers: {
      //   Authorization: `Bearer ${authToken}`,
      // },
    })
      .then(res => res.json())
      .then(res => {
        this.getImages()
        if (res.status === 'fail') {
          throw new Error('Upload failed')
        }
        this.createMessage('success', 'Image has been successfully uploaded.')
      })
      .catch(err => {
        this.createMessage('error', 'Something went wrong with the uploading.')
        this.setState({ isLoading: false })
      })
  }

  handleDeleteImage(imageName) {
    // const { authToken } = window.localStorage
    fetch(`${process.env.REACT_APP_API_URL}/api/images/${imageName}`, {
      method: 'DELETE',
      // headers: {
      //   Authorization: `Bearer ${authToken}`,
      // },
    })
      .then(res => res.json())
      .then(res => {
        if (res.status === 'success') {
          this.getImages()
        }
      })
  }

  handleTabChange(selectedTab) {
    this.setState({ selectedTab })
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
          this.resetMessage()
        }, 5000)
    )
  }

  resetMessage() {
    this.setState({
      message: {
        type: null,
        text: null,
      },
    })
  }


  render() {
    const {
      images,
      isLoading,
      isAuthenticated,
      message,
      selectedTab,
    } = this.state
    return (
      <Router>
      <React.Fragment>
        {/* <div className="nav-link">
          <Link to="/">Home</Link>
        </div> */}
        {message.type && message.text && (
          <Message type={message.type} text={message.text} />
        )}
        <NavBar
          title={"Công cụ gán nhãn Hán Nôm"}
          isAuthenticated={false}
        />
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
          <Route 
            exact path='/register' 
            render={() => (
              <RegisterLoginForm
              isAuthenticated={isAuthenticated}
              formType="register"
              onButtonClick={this.handleRegisterLoginUser}
              />
            )} 
          />
          <Route
            exact
            path="/login"
            render={() => (
              <RegisterLoginForm
                isAuthenticated={isAuthenticated}
                formType="login"
                onButtonClick={this.handleRegisterLoginUser}
              />
            )}
          />
        </Switch>
      </React.Fragment>
      </Router>
    )
  }
}

export default App
