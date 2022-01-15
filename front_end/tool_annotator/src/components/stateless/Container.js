import React from 'react'
import { Route } from 'react-router-dom'
import PropTypes from 'prop-types'
import AddImageForm from '../statefull/AddImageForm'
import CardList from './CardList'
import ImageTabNavBar from './ImageTabNavBar'
import ImageDetail from './ImageDetail'

function Container(props) {
  return (
    <div className="container" style={{ margin: '30px auto' }}>
      <Route
        path="/images/:imageName"
        render={({ match }) => (
          <ImageDetail
            image={props.images.find(
              image => image.filename === `${match.params.imageName}.jpg`
            )}
            createMessage={props.createMessage}
          />
        )}
      />
      <Route
        exact
        path="/images"
        render={() => (
          <div className="grid space-around">
            <div className="grid-row">
                <AddImageForm onButtonClick={props.onButtonClick} />
            </div>
            <div className="grid-row">
              <ImageTabNavBar
                onTabChange={props.onTabChange}
              />
            </div>
            <CardList
              images={props.images}
              isLoading={props.isLoading}
              selectedTab={props.selectedTab}
              onDeleteImage={props.onDeleteImage}
            />
          </div>
        )}
      />
    </div>
  )
}

Container.propTypes = {
  images: PropTypes.array.isRequired,
  onButtonClick: PropTypes.func.isRequired,
  isLoading: PropTypes.bool.isRequired,
  selectedTab: PropTypes.string.isRequired,
  onTabChange: PropTypes.func.isRequired,
  onDeleteImage: PropTypes.func.isRequired,
  createMessage: PropTypes.func.isRequired,
}

export default Container
