const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");

let x = canvas.width / 2; 
let y = canvas.height / 2; 
let v = 0; 
let vxl = 0; 
let vxr = 0; 
let angle = 0; 

const img = new Image();
img.src = '/static/boat.png';

let islandsCoordinates = [];
const islands = JSON.parse(document.getElementById('islands-data').textContent);

const islandImages = {
    1: '/static/ile1.png',
    2: '/static/ile3.png'
};

function drawIslands() {
    if (Array.isArray(islandsCoordinates) && islandsCoordinates.length > 0) {
        islandsCoordinates.forEach(island => {
            let iswidth, isheight;
            if (island[0] == 1) {
                iswidth = 100;
                isheight = 100;
            } else {
                iswidth = 200;
                isheight = 200;
            }        
            
            const size = island[0];
            const islandImg = new Image();
            islandImg.src = islandImages[size];
            ctx.drawImage(islandImg, island[1], island[2], iswidth, isheight); 
        });
    } else {
        islands.forEach(island => {
            let iswidth, isheight;
            if (island[0] == 1) {
                iswidth = 50;
                isheight = 50;
            } else {
                iswidth = 100;
                isheight = 100;
            }
            const size = island[0];
            let islandx = Math.random() * (canvas.width - iswidth);
            let islandy = Math.random() * (canvas.height - isheight);
            const islandImg = new Image();
            islandImg.src = islandImages[size];
            ctx.drawImage(islandImg, islandx, islandy, iswidth, isheight);
            islandsCoordinates.push([island[0], islandx, islandy, island[1]]);
        });
    }
}

function checkCollision() {
    const boatWidth = img.width;
    const boatHeight = img.height;

    islandsCoordinates.forEach(island => {
        let iswidth, isheight;
        if (island[0] == 1) {
            iswidth = 50;
            isheight = 50;
        } else {
            iswidth = 100;
            isheight = 100;
        }

        if (
            x < island[1] + iswidth &&
            x + boatWidth > island[1] &&
            y < island[2] + isheight &&
            y + boatHeight > island[2]
        ) {
            window.location.href = `/chat/${island[3]}`;
        }
    });
}

function update() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    drawIslands();
    
    v += vxl - vxr;
    x += Math.cos(angle * Math.PI / 180) * v;
    y += Math.sin(angle * Math.PI / 180) * v;

    ctx.save();
    ctx.translate(x, y);
    ctx.rotate(angle * Math.PI / 180);
    ctx.drawImage(img, -img.width / 2, -img.height / 2, img.width, img.height);
    ctx.restore();

    checkCollision();

    requestAnimationFrame(update);
}



canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

update();
