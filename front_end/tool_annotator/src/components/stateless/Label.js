import React from 'react'
import PropTypes from 'prop-types'

function Label({ label }) {
  return (
    <div >
    <span className="box-label-first">Nhãn</span>
    <br/>
    <span className="box-label">{label}</span>
  </div>
  )
}

Label.propTypes = {
  label: PropTypes.string.isRequired,
}

export default Label
