export function renderRadar(canvas, data) {

    const ctx = canvas.getContext("2d");

    const h = data.length;

    const w = data[0].length;

    canvas.width = w;

    canvas.height = h;

    const img = ctx.createImageData(w, h);

    for(let y=0;y<h;y++){

        for(let x=0;x<w;x++){

            const v = data[y][x];

            const i = (y*w+x)*4;

            img.data[i] = v * 4;

            img.data[i+1] = 255-v*4;

            img.data[i+2] = 0;

            img.data[i+3] = 255;
        }
    }

    ctx.putImageData(img,0,0);
}