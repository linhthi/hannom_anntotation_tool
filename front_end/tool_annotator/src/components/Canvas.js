import React, {useEffect, useRef, useState} from "react";
import PropTypes from 'prop-types';

function Canvas({draw, height, width, src}) {
    const canvas = React.useRef();
    const ctx = null;

    useEffect(() => {
        const ctx = canvas.current.getContext('2d');
        draw(ctx);
        // const r1Info = { x: 20, y: 30, w: 150, h: 100 };
        // const r1Style = { borderColor: 'red', borderWidth: 10 };
        // drawRect(r1Info, r1Style);
    });

    // // draw Rectangle
    // const drawRect = (info, style = {}) => {
    //     const { x, y, w, h } = info;
    //     const { borderColor = 'black', borderWidth = 1 } = style;
     
    //     ctx.beginPath();
    //     ctx.strokeStyle = borderColor;
    //     ctx.lineWidth = borderWidth;
    //     ctx.rect(x, y, w, h);
    //     ctx.stroke();
    // }

    return (
        <canvas ref={canvas} height={height} width={width} onLoad={draw}>
            <img src={src}/>
        </canvas>
    )
}

Canvas.propTypes = {
    draw: PropTypes.func.isRequired,
    height: PropTypes.number.isRequired,
    width: PropTypes.number.isRequired,
}

export default Canvas;