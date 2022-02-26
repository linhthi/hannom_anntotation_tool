import React, { useState } from 'react'
import PropTypes from 'prop-types'
import { Link } from 'react-router-dom'
import { FaClone, FaInfoCircle, FaTrashAlt } from 'react-icons/fa'

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
            src={`http://localhost:5000/api/images/uploads/${image.filename}`}
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
          {/* <div className="description">
            This image may contain:{' '}
            {image.boxes.length > 0 ? (
              [...new Set(image.boxes.map(box => box.label))].map(
                (label, id) => (
                  <span key={id} className="label">
                    {label}
                  </span>
                )
              )
            ) : (
              <div className="label">nothing</div>
            )}
          </div> */}
        </div>
        <div className="extra-content">
          <div>
            Được tải lên bởi{' '}
            <span style={{ color: 'red' }}>{image.user_id}</span>
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
