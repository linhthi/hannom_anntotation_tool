import React from 'react';
import PropTypes from 'prop-types';
import { FaEye, FaCheck, FaEdit, FaTrash } from 'react-icons/fa';
import BoxCoord from '../stateless/BoxCoord';
import BoxEditForm from '../stateless/BoxEditForm';
import Label from '../stateless/Label';
import LabelEditForm from '../stateless/LabelEditForm';

class BoxDetail extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      boxIsDrawn: props.boxIsDrawn,
      editMode: props.editMode || false,
      coords: {
        id: props.box.id,
        label: props.box.label,
        x_min: Math.floor(props.box.x_min),
        y_min: Math.floor(props.box.y_min),
        x_max: Math.floor(props.box.x_max),
        y_max: Math.floor(props.box.y_max),
      },
    };

    this.handleInputChange = this.handleInputChange.bind(this);
    this.handleTrashIconClick = this.handleTrashIconClick.bind(this);
    this.toggleEditMode = this.toggleEditMode.bind(this);
  }

  handleInputChange(e) {
    const { name, value } = e.target;
    const { onInputChange } = this.props;
    this.setState(
      prev => ({
        coords: {
          ...prev.coords,
          [name]: name === 'label' ? value : parseFloat(value) || 0,
        },
      }),
      () => {
        const { coords } = this.state;
        onInputChange(coords)
      }
    )
  }

  handleTrashIconClick() {
    const { onTrashIconClick } = this.props;
    const { coords } = this.state;
    onTrashIconClick(coords.id)
  }

  toggleEditMode() {
    this.setState(prev => ({
      editMode: !prev.editMode,
    }))
  }

  render() {
    const { box } = this.props

    const { boxIsDrawn, editMode, coords } = this.state

    return (
      <div className="segment" key={box.id}>
        <div className="grid">
          <div className="grid-row space-vertical">
            <div className="flex-center space-around">
              <div>
                {editMode ? (
                  <LabelEditForm
                    label={box.label}
                    onInputChange={this.handleInputChange}
                  />
                ) : (
                  <Label label={box.label} />
                )}
              </div>
              <div>
                <span>
                  {editMode ? (
                    <button
                      className="circular primary button"
                      onClick={this.handleCheckIconClick}
                    >
                      <FaCheck />
                    </button>
                  ) : (
                    <button
                      className="circular button"
                      onClick={this.toggleEditMode}
                    >
                      <FaEdit />
                    </button>
                  )}
                  <button
                    className="circular button"
                    onClick={this.handleTrashIconClick}
                  >
                    <FaTrash />
                  </button>
                </span>
              </div>
            </div>
          </div>
          <div className="grid-row space-vertical">
            {editMode ? (
              <BoxEditForm
                coords={coords}
                onInputChange={this.handleInputChange}
              />
            ) : (
              <BoxCoord coords={coords} />
            )}
          </div>
        </div>
      </div>
    )
  }
}

BoxDetail.propTypes = {
  box: PropTypes.object.isRequired,
  boxIsDrawn: PropTypes.bool.isRequired,
  editMode: PropTypes.bool,
  onInputChange: PropTypes.func.isRequired,
  onTrashIconClick: PropTypes.func.isRequired,
}

BoxDetail.defaultProps = {
  editMode: false,
}

export default BoxDetail
