import React from 'react'
import PropTypes from 'prop-types'
import { Link } from 'react-router-dom'

function NavBar({ title, isAuthenticated }) {
  return (
    <div className="nav flex-center space-around text-center">
      <div className="nav-header">{title}</div>
      <div className="nav-link">
        <Link to="/">Trang chủ</Link>
      </div>
      {isAuthenticated && (
        <div className="nav-link">
          <Link to="/logout">Đăng xuất</Link>
        </div>
      )}
      {!isAuthenticated && (
        <React.Fragment>
          <div className="nav-link">
            <Link to="/register">Đăng ký</Link>
          </div>
          <div className="nav-link">
            <Link to="/login">Đăng nhập</Link>
          </div>
        </React.Fragment>
      )}
      <div className="nav-link">
        <div className="input-field-dark">
          <input type="text" placeholder="Search tag..." />
        </div>
      </div>
    </div>
  )
}

NavBar.propTypes = {
  title: PropTypes.string.isRequired,
  isAuthenticated: PropTypes.bool.isRequired,
}

export default NavBar
