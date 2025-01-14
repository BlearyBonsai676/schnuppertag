let canvas = document.querySelector('canvas')

canvas.style.backgroundColor = "#302c2c"

let ctx = canvas.getContext('2d')

let startBtn = document.querySelector('#start')
let restartBtn = document.querySelector('#restart')
let gameover = false;
let intervalid = null;
let circleX = 100, circleY = 80, radius = 20
let incrX = 5, incrY = 5
let paddleX = 200, paddleheight = 150, paddlewidth = 20
let isLeft = false, isRight = false
let score = 0;
let startAudio = new Audio('./startmusic.m4a')

function drawcircle(){
    ctx.beginPath()
    ctx.fillStyle = '#edbd39'
    ctx.arc(circleX, circleY, radius, 0, 2*Math.PI)
    ctx.fill() 
    ctx.closePath()
}

function drawpaddle(){
    ctx.beginPath()
    ctx.fillStyle = '#64fa4d'
    ctx.fillRect(paddleX, canvas.height - paddlewidth, paddleheight, paddlewidth)
    ctx.closePath()

}



function collision()
{

    /// check if the ball is hitting the right wall
    if(circleX + radius > canvas.width)
    {
        incrX = -incrX
    }

    if(circleY + radius > canvas.height)
    {
        /// check if the ball is hitting the paddle
        if(circleX > paddleX && circleX < paddleX + paddleheight)
        {
            /// ball is hitting the paddle
            incrY = -incrY
            score++
        }
        else
        {
            gameover = true       
        }
    }
    /// check if the ball is hitting the left wall
    if(circleX - radius < 0)
    {
        incrX = -incrX
    }

    /// check if the ball is hitting the top wall
    if(circleY - radius < 0)
    {
        incrY = -incrY
    }
}

function animate(){
    console.log('entering animate')
    ctx.clearRect(0, 0, canvas.width, canvas.height)


    ctx.fillStyle = 'white'
    ctx.font = '24px Verdana'
    ctx.fillText(`Score: ${score}` , 30, 30)



    if(isRight && paddleX + paddleheight < canvas.width){
        paddleX = paddleX + 5
    }
    if(isLeft && paddleX > 0){
        paddleX = paddleX - 5
    }

    drawpaddle()
    collision()
    drawcircle()
    circleX = circleX + incrX
    circleY = circleY + incrY
    if(gameover){
        cancelAnimationFrame(intervalid)
        canvas.style.display = "none"
        restartBtn.style.display = "block"
    }
    else{
        intervalid = requestAnimationFrame(animate)
    }
}



function start(){
    canvas.style.display = 'block'
    restartBtn.style.display = 'none'
    startBtn.style.display = 'none'
    animate()
}



window.addEventListener('load', () => {
    canvas.style.display = 'none'
    restartBtn.style.display = 'none'
    start()

    document.addEventListener('keydown', (event) => {
        if (event.code == "ArrowRight"){
            isRight = true
            isLeft = false
        }
        if (event.code == "ArrowLeft"){
            isLeft = true
            isRight = false
    }
    })

    document.addEventListener('keyup', (event) => {
        if (event.code == "ArrowRight"){
            isRight = false
        }
        if (event.code == "ArrowLeft"){
            isLeft = false
        }
    })
    startBtn.addEventListener('click', () => {
    start()
    })

    restartBtn.addEventListener('click', () => {
        gameover = false
        circleX = 50;
        circleY = 50;
        score = 0;
        start()
    })
})










//ctx.fillStyle = 'red'
//ctx.fillRect(50, 60, 100, 200)

//ctx.fillStyle = 'blue'
//ctx.fillRect(180, 60, 100, 200)

//ctx.clearRect(0, 0, canvas.width, canvas.height)

//ctx.strokeStyle = 'yellow'
//ctx.strokeRect(50, 60, 100, 200)




