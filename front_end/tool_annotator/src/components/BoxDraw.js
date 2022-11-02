import React from "react"
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

function BoxDraw() {
  const [drawings, setDrawings] = React.useState([])
  const [mouseState, setMouseState] = React.useState(initMouse)

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
      isDrawing: true,
      startX: startX,
      startY: startY,
      width: 0,
      height: 0,
      offsetX: offset.left,
      offsetY: offset.top
    })
  }

  const up = e => {
    if (!mouseState.isDrawing) return

    var wid = mouseState.width
    var hei = mouseState.height

//     if (wid < 5 || hei < 5) {
//       setMouseState({ ...initMouse })
//     } else {
//       setMouseState({ ...initMouse })
//       setDrawings([...drawings, ...[mouseState]])
//     }
    setMouseState({ ...initMouse })
    setDrawings([...drawings, ...[mouseState]])
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
              style={{ strokeWidth: 1, stroke: "black" }}
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

}
