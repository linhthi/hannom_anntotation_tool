import React, { useState, useEffect} from 'react'
import PropTypes from 'prop-types'
import lines from '../../lines.json'

function ImageLabelDisplay(props) {
  const {
    svgWidth,
    svgHeight,
    boxes,
    scale,
    newBox,
    createMessage,
    parrentCallback,
  } = props;

  const [moveable, setMoveable] = useState(false)
  const [box, setBox] = useState()
  const [drawBoxes, setDrawBoxes] = useState([])

  // const numberLines = 17
  // var x = 0
  // var y = 0
  // const [lines, setLines] = useState([]);

  // useEffect(()=> {
  //   newBoxIndex = boxes.findIndex((obj => obj.label == newBox.x_min and ne))
  // }, [])

  const searchBox = (x, y) => {
    boxes.map(box => {
      if (x > box.x_min * scale && x < box.x_max*scale && y > box.y_min*scale && y < box.y_max*scale) {
        // return <label>{box.label}</label>
        setBox(box)
        // alert("box: "+box.label+" x: "+x+" y:"+y)
        setDrawBoxes(box)
        parrentCallback(box)
      }
    })
  }

  // for (let index = 0; index < numberLines; index++) {
  //   x = x * index + 20
  //   lines.push({
  //     x1: x,
  //     y1: y,
  //     x2: x,
  //     y2: svgHeight
  //   })
  // }
  // console.log("Lines", lines)

  const handleOnclick = e => {
    var evt = e.target
    var dim = evt.getBoundingClientRect()
    var x = e.clientX - dim.left
    var y = e.clientY - dim.top

    searchBox(x, y)
  }

  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      xmlnsXlink="http://www.w3.org/1999/xlink"
      className="image-large"
      width={svgWidth}
      height={svgHeight}
      onClick={handleOnclick}
      parrentCallback={parrentCallback}
    >
      <g>
        <rect 
          x={10}
          y={10}
          width={svgWidth-12}
          height={svgHeight-12}
          style={{ fill: 'none', stroke: 'black', strokeWidth: '1' }}
        />
      </g>

      {lines.map(line => (
        <g>
          <line 
          x1={line.x*scale*1.45} 
          y1={line.y1*scale*1.3+10} 
          x2={line.x*scale*1.45} 
          y2={line.y2*scale*1.3} 
          style={{ stroke: 'black', strokeWidth: '0.5' }}
          />
        </g>
      ))}

      {boxes.map(box => (
        box.label ? 
        <g>
          {/* <rect
              key={box.id}
              x={box.x_min * scale}
              y={box.y_min * scale}
              width={(box.x_max - box.x_min) * scale}
              height={(box.y_max - box.y_min) * scale}
              style={{ fill: 'none', stroke: 'lime', strokeWidth: '1' }}

          /> */}
          <text 
              x={box.x_min * scale}
              y={(box.y_min + box.y_max) * scale / 2}
              width={(box.x_max - box.x_min) * scale}
              height={(box.y_max - box.y_min) * scale}
              font-size="13" fill="blue"
          > 
            {box.label}
          </text>
        </g>
        :
        <g>
          {/* <rect
              key={box.id}
              x={box.x_min * scale}
              y={box.y_min * scale}
              width={(box.x_max - box.x_min) * scale}
              height={(box.y_max - box.y_min) * scale}
              style={{ fill: 'none', stroke: 'black', strokeWidth: '1' }}

          /> */}
          {/* <text 
              x={box.x_min * scale}
              y={box.y_min * scale}
              width={(box.x_max - box.x_min) * scale}
              height={(box.y_max - box.y_min) * scale}
              font-size="14" fill="blue"
          > 
            {box.label}
          </text> */}
        </g>
        ))}

          {/* <g>
            <rect
                key={box.id}
                x={box.x_min * scale}
                y={box.y_min * scale}
                width={(box.x_max - box.x_min) * scale}
                height={(box.y_max - box.y_min) * scale}
                style={{ fill: 'none', stroke: 'red', strokeWidth: '2' }}

            />
            </g> */}
    </svg>
  )
}

ImageLabelDisplay.propTypes = {
  svgWidth: PropTypes.number.isRequired,
  svgHeight: PropTypes.number.isRequired,
  scale: PropTypes.number.isRequired,
  boxes:PropTypes.array.isRequired,
  newBox: PropTypes.object.isRequired,
  createMessage: PropTypes.func.isRequired,
  parrentCallback: PropTypes.func.isRequired,
}

export default ImageLabelDisplay;
