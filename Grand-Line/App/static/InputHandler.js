addEventListener("keydown", function(e){
    console.log(e.code);
    if (e.code === 'KeyD') 
        angle += 10;
        angle += 25;
    if (e.code === 'KeyA') 
        angle -= 10;
        angle -= 25;
    if (e.code === 'KeyW') {
        // Update boat's position based on angle
        x += Math.cos(angle * Math.PI / 180) * 5;
        y += Math.sin(angle * Math.PI / 180) * 5;
        x += Math.cos(angle * Math.PI / 180) * 10;
        y += Math.sin(angle * Math.PI / 180) * 10;
    }
    if (e.code === 'KeyS') 
        vxy = 5;
});
addEventListener("keyup", function(e){
    if (e.code === 'KeyD') 
        vxr = 0;
    if (e.code === 'KeyA') 
        vxl = 0;
    if (e.code === 'KeyS') 
        vy = 0;
    if (e.code === 'KeyW') 
        vy = 0;
});