import React, {useLayoutEffect, useState} from "react";
import Canvas from "./Canvas";

// const draw = (context) => {
//     // context.fillStyle = "rgb(200, 0, 0)";
//     // context.fillRect(10, 10, 50, 50);
  
//     // context.fillStyle = "rgba(0, 0, 200, 0.5)";
//     // context.fillRect(30, 30, 50, 50);
// }

function Annotation() {
  
  useLayoutEffect(() => {
    const canvas = document.getElementById('canvas');
    const ctx = canvas.getContext('2d');

    ctx.fillStyle = 'gree';
    ctx.fillRect(10, 10, 150, 100);
  })

  return (
    <canvas
      id="canvas"
      style={{backgroundColor: "white"}}
      width={window.innerWidth}
      height={window.innerHeight}
  >
        Canvas
    </canvas>
      // <img src={`http://localhost:5000/book/uploads/Lien_Phai.jpg`} />
  )
  // <Canvas draw={draw} height={200} width={200} src={`http://localhost:5000/book/uploads/Lien_Phai.jpg`} />

}

export default Annotation;