import React, { useState, useRef, useEffect, useCallback} from 'react'
import { parse } from 'json2csv'
import PropTypes from 'prop-types'
import ImageAnnoDisplay from './ImageAnnoDisplay'
import ImageLabelDisplay from './ImageLabelDisplay'
import {FaEdit, FaTrash } from 'react-icons/fa'
import { Link } from 'react-router-dom'
import { confirmAlert } from 'react-confirm-alert'
import 'react-confirm-alert/src/react-confirm-alert.css'
import axios from 'axios'
import API from '../constant/API'


function ImageDetail({ image, createMessage }) {
  const [drawBoxes, setDrawBoxes] = useState([])
  const [boxes, setBoxes] = useState([])
  const [editModes, setEditModes] = useState([])
  const [scale, setScale] = useState(0.45)
  const [svgWidth, setSvgWidth] = useState(0)
  const [svgHeight, setSvgHeight] = useState(0)
  const [isAddBoundingBox, setIsAddBoundingBox] = React.useState(false)
  const [newListDrawing, setNewListDrawing] = useState([])
  const [isEdit, setEdit] = useState(false)
	const [newLabel, setNewLabel] = useState(drawBoxes.label)
  const [isFullScreen, setIsFullScreen] = useState(false)
  const [page, setPage] = useState({})
  const [loading, setLoading] = useState(true)
  const ref = useRef(null)


  const fetchMyAPI = async () => {
    let response = await axios(`${API.GET_LABEL}/${image.filename}`)
    let res = await response.data.data
    console.log("Respone", res)
    setPage(res)

    if (res.bboxes) {
      setBoxes(res.bboxes.sort((a, b) => a.id - b.id))
      setEditModes(Array(res.bboxes.length).fill(false))
    }
  
    setSvgWidth(window.innerWidth / 2.7)
    setSvgHeight(res.height * (window.innerWidth / 2.7/ res.width))
    setScale(window.innerWidth / 2.7 / res.width)

  }

  useEffect(()=> {
    fetchMyAPI()
    setLoading(false)
  }, [])

  useEffect(() => {
    setSvgWidth(page.width *scale)
    setSvgHeight(page.height *scale)
  }, [scale])

  const callback = useCallback((drawBoxes) => {
    setDrawBoxes(drawBoxes)
  }, [])

  const updateNewListDrawing = useCallback((newListDrawing) => {
    setNewListDrawing(newListDrawing)
  }, [])

  const updateListBox = newListDrawing => {
    newListDrawing.map((a, index) => {
      setBoxes([...boxes, {
        "id": 'id' + (new Date()).getTime(),
        "label": null,
        "x_min": a.startX / scale,
        "x_max": (a.startX + a.width) / scale,
        "y_min": a.startY / scale,
        "y_max": (a.startY + a.height) / scale,
      }])
    });
  }

  const onAddBoxButtonClick = () => {
    setIsAddBoundingBox(!isAddBoundingBox)
    updateListBox(newListDrawing)
    setDrawBoxes({})
  }

  const updateBoxes = (boxes) => {
    setBoxes(boxes)
  }

  


  const downloadBoxesAsCSV = () => {
    const fields = ['label', 'x_min', 'y_min', 'x_max', 'y_max']

    const csv = `data:text/csvcharset=utf-8,${parse(boxes, { fields })}`

    const hiddenElement = document.createElement('a')
    hiddenElement.setAttribute('href', encodeURI(csv))
    hiddenElement.setAttribute('target', '_blank')
    hiddenElement.setAttribute('download', page.filename.replace('jpg', 'csv'))
    hiddenElement.click()
  }


	const toggleEditMode = (e) => {
		setEdit(!isEdit)
	}

	const handleSave = (e) => {
		setEdit(!isEdit)
		const newBox = {
			"id": drawBoxes.id,
			"label": newLabel,
			"x_min": drawBoxes.x_min,
			"x_max": drawBoxes.x_max,
			"y_min": drawBoxes.y_min,
			"y_max": drawBoxes.y_max
		}
    const foundIndex = boxes.findIndex(x => x.id === newBox.id)
    console.log("Index in array", foundIndex)
    boxes[foundIndex] = newBox
    setBoxes([...boxes])
    // setNewListDrawing([])
    onSavePage()
	}

  const handleZoom = (e) => {
    setIsFullScreen(!isFullScreen)
    if (isFullScreen) {
      setScale(window.innerWidth / 2.7 / page.width)
      
    } else {
      setScale(window.innerWidth / 1.7/ page.width)
    }
  }
	
	const onLabelChange = (e) => {
		setNewLabel(e.target.value)
	}

  const handleTrashIconClick = () => {
    const arr = boxes.filter((item) => {
      return item.id !== drawBoxes.id
    })
    setDrawBoxes({})
    setBoxes([...arr])
    // confirmAlert({
    //   message: 'Xác nhận xóa bouding box của ô!',
    //   buttons: [
    //     {
    //       label: 'Có',
    //       onClick: () => {
    //         const arr = boxes.filter((item) => {
    //           return item.id !== drawBoxes.id
    //         })
    //         setDrawBoxes({})
    //         setBoxes([...arr])
    //       }
    //     },
    //     {
    //       label: 'Không',
    //       onClick: () => {}
    //     }
    //   ]
    // })
  }

  const handleSmooth = async () => {
    axios.post(`/api/images/crop/${image.filename}`, drawBoxes)
          .then(response => console.log(response))
    await new Promise(resolve => setTimeout(resolve, 1000))
    window.location.href = `http://localhost:5000/smooth/${image.filename}/img_${drawBoxes.id}`
  }

  const onSavePage = () => {
    page['bboxes'] = boxes
    axios.post(`/api/image/label/${image.filename}`, {'data': page})
         .then(res => console.log(res))
    alert('Đã lưu')
  }

  const renderEdit = () => {
    return (
      <div className='gray'>
        {!isAddBoundingBox ? (
          <>
          <span className="box-label-first">Nhãn </span>
          <input type="text" 
          id="label"
          key={drawBoxes.label}
          defaultValue={drawBoxes.label}
          disabled={!isEdit}
          style={{fontSize: 20, width: "50px", height: "50px"}}
          onChange={onLabelChange}
          >
          
          </input>
          {console.log("Updated label: ", drawBoxes.label)}
          <button
            className="circular button"
            onClick={toggleEditMode}
          >
            <FaEdit />
          </button>
          <button
            className="circular button"
            onClick={handleTrashIconClick}
          >
            <FaTrash />
          </button>
          {/* <Link to={`/smooth_feature/${drawBoxes.id}.png`}>
          <button className="button"
          onClick={handleSmooth}>
            Làm mịn nét chữ
          </button>
          </Link> */}
          {isEdit ?  (
            <button
            className="circular primary button"
            onClick={handleSave}
            >
              Lưu
            </button>
          ) : null}
          </>
        ): null}
      </div>
    )
  }
  return (

    <div className="row space-around">
      <div className="text-center" ref={ref}>
        {console.log("Page 2", image)}
        <ImageAnnoDisplay
          svgWidth={svgWidth || 0}
          svgHeight={svgHeight || 0}
          imageWidth={page.width}
          imageHeight={page.height}
          scale={scale}
          boxes={boxes}
          drawBoxes={drawBoxes}
          filename={image.filename}
          isDrawing={isAddBoundingBox}
          parrentCallback={callback}
          updateNewListDrawing={updateNewListDrawing}
          updateBoxes={updateBoxes}
        />
        {!isFullScreen ? (
          <button
          className="blue button"
          onClick={handleZoom}
          >
            Phóng to
          </button>
        ): (
          <button
          className="blue button"
          onClick={handleZoom}
          >
            Thu nhỏ
          </button>
        )}

        {!isAddBoundingBox ? (
          <button
            className="blue button"
            onClick={onAddBoxButtonClick}
          >
            Thêm 
          </button>
        ): (
          <button
            className="circular primary button"
            onClick={onAddBoxButtonClick}
          >
            Lưu
          </button>
        )}

        <button
          className="blue button"
          onClick={onSavePage}
        >
          Lưu trang
        </button>

        <br></br>
        {renderEdit()}
      </div>
      {!isFullScreen ? (
      <div className="half-width-item text-center">
        <ImageLabelDisplay
          svgWidth={svgWidth || 0}
          svgHeight={svgHeight || 0}
          scale={scale}
          boxes={boxes}
          drawBoxes={drawBoxes}
        />
        {/* <button className="blue button" onClick={downloadBoxesAsCSV}>
          Tải xuống văn bản
        </button> */}
      </div>
      ): (<></>)}

    </div>
  )
}

ImageDetail.propTypes = {
  image: PropTypes.object,
  createMessage: PropTypes.func.isRequired,
}

export default ImageDetail
