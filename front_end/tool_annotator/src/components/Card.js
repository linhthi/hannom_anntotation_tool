import React, { useState } from 'react'
import PropTypes from 'prop-types'
import { Link } from 'react-router-dom'
import { FaClone, FaInfoCircle, FaTrashAlt } from 'react-icons/fa'
import API from '../constant/API'

function Card({ image, onDeleteImage }) {
  const [detectImage, toggleDetectImage] = useState(true)

  return (
    <div className="grid-item" style={{ textAlign: 'left' }}>
      <div className="card">
        <Link
          to={`/images/${image.filename}`}
          className="image"
        >
          <img
            src={`${API.GET_IMAGE}/${image.filename}`}
            alt="detect result or original"
          />
        </Link>
        <div className="content">
          <div>
            <FaClone
              color={detectImage ? '#33ff33' : ''}
              onClick={() => toggleDetectImage(!detectImage)}
            />
            <Link
              to={`/images/${image.filename}`}
              className="ui image"
            >
              <FaInfoCircle color="#33ff33" />
            </Link>
              <FaTrashAlt
                color="red"
                onClick={() => onDeleteImage(image.filename)}
              />
          </div>
          
        </div>
        <div className="extra-content">
          <div>
            Image id{' '}
            <span style={{ color: 'red' }}>{image.id}</span>
          </div>
        </div>
      </div>
    </div>
  )
}

Card.propTypes = {
  image: PropTypes.object.isRequired,
  onDeleteImage: PropTypes.func.isRequired,
}

export default Card
