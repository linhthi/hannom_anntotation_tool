import React from 'react'
import PropTypes from 'prop-types'
import Card from './Card'
import Loader from './Loader'

function CardList(props) {
  const { selectedTab, images, isLoading } = props

  let cards
  if (selectedTab === 'all') {
    cards = images
      .sort((a, b) => b.id - a.id)
      .map(image => (
        <Card
          key={image.id}
          image={image}
          onDeleteImage={props.onDeleteImage}
        />
      ))
  
  }

  return (
    <React.Fragment>
      {isLoading && (
        <div className="grid-item">
          <Loader />
        </div>
      )}
      {cards}
    </React.Fragment>
  )
}

CardList.propTypes = {
  isLoading: PropTypes.bool.isRequired,
  selectedTab: PropTypes.string.isRequired,
  images: PropTypes.array.isRequired,
  onDeleteImage: PropTypes.func.isRequired,
}

export default CardList
