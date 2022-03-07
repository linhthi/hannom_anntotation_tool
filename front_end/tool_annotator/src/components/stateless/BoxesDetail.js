import React, { useState } from 'react'
import PropTypes from 'prop-types'
import BoxDetail from '../statefull/BoxDetail'
// import ReactPaginate from 'react-paginate'

function BoxesDetail({
  boxes,
  editModes,
  drawList,
  onInputChange,
  onTrashIconClick,
}) {
  const firstPage = boxes.slice(0,3)
  const [currentBoxes, setCurrentBoxes] = useState()
  // const handlePageClick = (e) => {
  //   const currentBoxes = boxes.slice(e.selected*3, e.selected*3 +3)
  //   setCurrentBoxes(currentBoxes)
  // }
  const newBox = currentBoxes ? currentBoxes : firstPage
  return (
    <div className="ui segments">
      
      <div>
      {newBox.map((box, i) => (
        <BoxDetail
          key={box.id}
          box={box}
          boxIsDrawn={drawList.includes(box.id)}
          editMode={editModes[i]}
          onTrashIconClick={onTrashIconClick}
          onInputChange={onInputChange}
        />
      ))}
      </div>

      {/* <div style={{display: 'inline-block'}}>
      <ReactPaginate
        breakLabel="..."
        nextLabel="next >"
        onPageChange={handlePageClick}
        pageRangeDisplayed={4}
        pageCount={boxes.length/3}
        previousLabel="< previous"
        renderOnZeroPageCount={null}
        pageClassName="page-item"
        pageLinkClassName="page-link"
        previousClassName="page-item"
        previousLinkClassName="page-link"
        nextClassName="page-item"
        nextLinkClassName="page-link"
        breakLabel="..."
        breakClassName="page-item"
        breakLinkClassName="page-link"
        containerClassName="pagination"
        activeClassName="active"
      />
      </div> */}
    </div>
  )
}

BoxesDetail.propTypes = {
  boxes: PropTypes.array.isRequired,
  drawList: PropTypes.array.isRequired,
  editModes: PropTypes.array.isRequired,
  onInputChange: PropTypes.func.isRequired,
  onTrashIconClick: PropTypes.func.isRequired,
}

export default BoxesDetail
