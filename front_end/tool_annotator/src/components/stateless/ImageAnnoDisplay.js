import React, { useState, useEffect} from 'react'
import PropTypes from 'prop-types'

const initMouse = {
  lastMoveX:0,
  lastMoveY:0,
  width:0,
  height:0,
  offsetX:0,
  offsetY:0,
  startX:0,
  startY:0,
  isDrawing: false
}

const getElOffset = el => {
  const rect = el.getBoundingClientRect()

  return {
    top: rect.top + window.pageYOffset,
    left: rect.left + window.pageXOffset
  }
}

const getCoords = e => {
  if (e.pageX || e.pageY) {
    return { x: e.pageX, y: e.pageY }
  }
  return {
    x: e.clientX,
    y: e.clientY
  }
}

function ImageAnnoDisplay(props) {
  const {
    svgWidth,
    svgHeight,
    imageWidth,
    imageHeight,
    boxes,
    scale,
    filename,
    isDrawing,
    parrentCallback,
    updateNewListDrawing,
  } = props
  
  const [drawings, setDrawings] = React.useState([])
  const [mouseState, setMouseState] = React.useState(initMouse)
  const [drawBoxes, setDrawBoxes] = useState([])

  const searchBox = (x, y) => {
    boxes.map(box => {
      if (x > box.x_min * scale && x < box.x_max*scale && y > box.y_min*scale && y < box.y_max*scale) {
        setDrawBoxes(box)
        parrentCallback(box)
      }
    })
  }

  const handleOnclick = e => {
    var evt = e.target
    var dim = evt.getBoundingClientRect()
    var x = e.clientX - dim.left
    var y = e.clientY - dim.top
    searchBox(x, y)
  }

  const down = e => {
    var mouseCoords = getCoords(e)
    var offset = getElOffset(e.target.parentNode)
    const startX = mouseCoords.x - offset.left
    const startY = mouseCoords.y - offset.top

    setMouseState({
      ...mouseState,
      isDrawing: isDrawing,
      startX: startX,
      startY: startY,
      width: 5,
      height: 5,
      offsetX: offset.left,
      offsetY: offset.top
    })
  }

  const up = e => {
    if (!mouseState.isDrawing) return

    var wid = mouseState.width
    var hei = mouseState.height

    if (wid < 10 || hei < 10) {
      setMouseState({ ...initMouse })
    } else {
      setMouseState({ ...initMouse })
      setDrawings([...drawings, ...[mouseState]])
    }
  }

  const move = e => {
    if (!mouseState.isDrawing) return

    var currX = e.pageX - mouseState.offsetX
    var currY = e.pageY - mouseState.offsetY

    var wid = currX - mouseState.startX
    var hei = currY - mouseState.startY
    if (wid <= 0) {
      wid = Math.abs(wid)
    } else {
      currX = mouseState.startX
    }
    if (hei <= 0) {
      hei = Math.abs(hei)
    } else {
      currY = mouseState.startY
    }

    setMouseState({
      ...mouseState,
      startX: currX,
      startY: currY,
      width: wid,
      height: hei
    })
  }

  const leave = e => {
    if (!mouseState.isDrawing) return
    setMouseState({ ...initMouse })
  }  

  const renderManual = () => {
    return drawings.length > 0 ? (
      <>
        {updateNewListDrawing(drawings)}
        {mouseState.isDrawing ? (
          <rect
            x={mouseState.startX}
            y={mouseState.startY}
            width={mouseState.width}
            height={mouseState.height}
            fill="none"
            style={{ strokeWidth: 1, stroke: "black" }}
          />
        ) : null}
        {drawings.map((a, index) => (
          <g key={index} style={{ cursor: "pointer" }}>
            <rect
              x={a.startX}
              y={a.startY}
              width={a.width}
              height={a.height}
              fill="none"
              style={{ strokeWidth: 0.5, stroke: "red" }}
            />
          </g>
        ))}
      </>
    ) : (
      <>
        {mouseState.isDrawing ? (
          <rect
            x={mouseState.startX}
            y={mouseState.startY}
            width={mouseState.width}
            height={mouseState.height}
            fill="none"
            style={{ strokeWidth: 1, stroke: "black" }}
          />
        ) : null}
      </>
    )
  }

  return (
    <div
      id="svgWrapper"
      onMouseLeave={leave}
      onMouseUp={up}
      onMouseMove={move}
      onMouseDown={down}
    >
      <svg
        xmlns="http://www.w3.org/2000/svg"
        xmlnsXlink="http://www.w3.org/1999/xlink"
        className="image-large"
        width={svgWidth}
        height={svgHeight}
        onClick={handleOnclick}
      >
        
        <image
          xlinkHref={`http://localhost:5000/api/images/uploads/${filename}`}
          width={svgWidth}
          height={svgHeight}
          style={
            imageWidth > imageHeight ? { width: '100%' } : { height: '100%' }
          }
          // onMouseMove={handleMouseMove}
        />
        {boxes.map(box => (
          box.label ?
          <g>
            <rect
                key={box.id}
                x={box.x_min * scale}
                y={box.y_min * scale}
                width={(box.x_max - box.x_min) * scale}
                height={(box.y_max - box.y_min) * scale}
                style={{ fill: 'none', stroke: 'lime', strokeWidth: '1' }}

            />
            </g>
            :
            <g>
            <rect
                key={box.id}
                x={box.x_min * scale}
                y={box.y_min * scale}
                width={(box.x_max - box.x_min) * scale}
                height={(box.y_max - box.y_min) * scale}
                style={{ fill: 'none', stroke: 'red', strokeWidth: '0.5' }}

            />
            </g>

            ))}
        {/* {drawBoxes.length > 0 
          drawBoxes.map(box => ( */}
            <g>
              <rect
                  key={drawBoxes.id}
                  x={drawBoxes.x_min * scale}
                  y={drawBoxes.y_min * scale}
                  width={(drawBoxes.x_max - drawBoxes.x_min) * scale}
                  height={(drawBoxes.y_max - drawBoxes.y_min) * scale}
                  style={{ fill: 'none', stroke: 'yellow', strokeWidth: '2' }}

              />
              </g>
            {/* </g>
          ))} */}
          {console.log("Drawings: ", drawings)}
          {renderManual()}
      </svg>
    </div>
  )
}

ImageAnnoDisplay.propTypes = {
  svgWidth: PropTypes.number.isRequired,
  svgHeight: PropTypes.number.isRequired,
  imageWidth: PropTypes.number.isRequired,
  imageHeight: PropTypes.number.isRequired,
  filename: PropTypes.string.isRequired,
  scale: PropTypes.number.isRequired,
  boxes: PropTypes.array.isRequired,
  isDrawing: PropTypes.bool.isRequired,
  // onImageClick: PropTypes.func.isRequired,
  // createMessage: PropTypes.func.isRequired,
  parrentCallback: PropTypes.func.isRequired,
  updateNewListDrawing: PropTypes.func.isRequired,
}

export default ImageAnnoDisplay
