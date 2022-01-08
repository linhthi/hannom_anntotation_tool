import React, { useState} from 'react';
import PropTypes from 'prop-types';

function ImageAnnoDisplay(props) {
  const {
    svgWidth,
    svgHeight,
    imageWidth,
    imageHeight,
    boxes,
    scale,
    filename,
    onImageClick,
    createMessage,
    parrentCallback
  } = props;

  const [moveable, setMoveable] = useState(false)
  const [box, setBox] = useState()
  const [drawBoxes, setDrawBoxes] = useState([])

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

  const handleOnclick = e => {
    var evt = e.target
    var dim = evt.getBoundingClientRect()
    var x = e.clientX - dim.left
    var y = e.clientY - dim.top

    searchBox(x, y)
  }

  const handleMouseMove = e => {
    if (!moveable) return;
    // // if (drawBoxes.length > 1) {
    // //   createMessage(
    // //     'error',
    // //     'Only one box can be editted by clicking at a time.'
    // //   );
    // //   return;
    // // }
    // // if (drawBoxes.length === 0) {
    // //   return;
    // // }
    // const rect = e.target.getBoundingClientRect();
    // const clickX = (e.clientX - rect.x) / scale;
    // const clickY = (e.clientY - rect.y) / scale;
    // const newBox = { ...drawBoxes[0] };
    // if (
    //   Math.abs(clickX - drawBoxes[0].x_min) >
    //   Math.abs(clickX - drawBoxes[0].x_max)
    // ) {
    //   newBox.x_max = clickX;
    // } else {
    //   newBox.x_min = clickX;
    // }
    // if (
    //   Math.abs(clickY - drawBoxes[0].y_min) >
    //   Math.abs(clickY - drawBoxes[0].y_max)
    // ) {
    //   newBox.y_max = clickY;
    // } else {
    //   newBox.y_min = clickY;
    // }
    // onImageClick(newBox);
  }

  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      xmlnsXlink="http://www.w3.org/1999/xlink"
      className="image-large"
      width={svgWidth}
      height={svgHeight}
      onClick={handleOnclick}
    >
      {
        console.log("DrawBoxes Child 2", drawBoxes)
      }
      <image
        xlinkHref={`http://localhost:5000/api/images/uploads/${filename}`}
        width={svgWidth}
        height={svgHeight}
        style={
          imageWidth > imageHeight ? { width: '100%' } : { height: '100%' }
        }
        onMouseMove={handleMouseMove}
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
                style={{ fill: 'none', stroke: 'red', strokeWidth: '2' }}

            />
            </g>
          {/* </g>
        ))} */}
    </svg>
  );
}

ImageAnnoDisplay.propTypes = {
  svgWidth: PropTypes.number.isRequired,
  svgHeight: PropTypes.number.isRequired,
  imageWidth: PropTypes.number.isRequired,
  imageHeight: PropTypes.number.isRequired,
  filename: PropTypes.string.isRequired,
  scale: PropTypes.number.isRequired,
  boxes: PropTypes.array.isRequired,
  onImageClick: PropTypes.func.isRequired,
  createMessage: PropTypes.func.isRequired,
  parrentCallback: PropTypes.func.isRequired,
};

export default ImageAnnoDisplay;
