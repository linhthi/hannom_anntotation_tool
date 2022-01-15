import React, { useState, useEffect} from 'react'
import PropTypes from 'prop-types'
import lines from '../../lines.json'

function ImageLabelDisplay(props) {
  const {
    svgWidth,
    svgHeight,
    boxes,
    scale,
    drawBoxes,
  } = props

  const [moveable, setMoveable] = useState(false)

  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      xmlnsXlink="http://www.w3.org/1999/xlink"
      className="image-large"
      width={svgWidth}
      height={svgHeight}
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
          <text 
              x={box.x_min * scale +2 }
              y={(box.y_min + box.y_max) * scale / 2 + 2}
              width={(box.x_max - box.x_min) * scale}
              height={(box.y_max - box.y_min) * scale}
              font-size="13" fill="blue"
          > 
            {box.label}
          </text>
        </g>
        :
        <g>
        </g>
      ))}

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
    </svg>
  )
}

ImageLabelDisplay.propTypes = {
  svgWidth: PropTypes.number.isRequired,
  svgHeight: PropTypes.number.isRequired,
  scale: PropTypes.number.isRequired,
  boxes:PropTypes.array.isRequired,
  drawboxes: PropTypes.object.isRequired,
}

export default ImageLabelDisplay
