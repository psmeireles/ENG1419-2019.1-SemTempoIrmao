var numberFixedChallenge = 0;
var numberPeriodicChallenge = 0;
var numberLifes = 3;
var timer;
var imageHeight = 60;
var imageWidth = 60;
var currentLevel = 1;

function createNewFixedChallenge(challengeName,wireList)
{
    wireList=wireList.map(function(wire)
    {
        if(wire=="1")
        return " Vermelho" //fio 1
        else if(wire=="2")
            return " Verde" //fio 2
        else if(wire=="3")
        return " Azul" //fio 3
    })
    var newFixedChallenge = document.createElement("h4");
    var challengeImage = document.createElement("img");
    var additionalImage = document.createElement("img");
    if(challengeName == "wires")
    {
        newFixedChallenge.innerHTML = "Coloque os fios na seguinte ordem e aperte o botão para confirmar:" + wireList[0]+"-Azul,"+wireList[1]+"-Marrom,"+ wireList[1] +"-Amarelo";
        challengeImage.src= "static/images/wires.png";
        additionalImage.src= "static/images/button.png";

    }
    else if(challengeName == "genius")
    {
        newFixedChallenge.innerHTML = "Observe os LEDs e aperte os botões correspondentes!";
        challengeImage.src= "static/images/led.png";
        additionalImage.src= "static/images/button.png";

    }
    newFixedChallenge.style.fontSize="20px";
    challengeImage.height = imageHeight;
    challengeImage.width = imageWidth;
    additionalImage.height = imageHeight;
    additionalImage.width = imageWidth;
    newFixedChallenge.appendChild(challengeImage);
    newFixedChallenge.appendChild(additionalImage);
    //newFixedChallenge.id="fixedChallengeId"+ String(numberFixedChallenge);
    newFixedChallenge.id=challengeName;
    numberFixedChallenge = numberFixedChallenge + 1;
    document.getElementById("fixedChallenges").appendChild(newFixedChallenge);
}

function createNewPeriodicChallenge(challengeName,params)
{ 

    var newPeriodicChallenge = document.createElement("h4");
    var challengeImage = document.createElement("img");
    var additionalImage = document.createElement("img");
    additionalImage.src = "";
    if(challengeName == "distance")
    {
        newPeriodicChallenge.innerHTML = "Use o sensor de distância para ficar entre " +params[0]+ " e "+ params[1]+ " por " +params[2] +"s!";
        challengeImage.src= "static/images/distance.png";
        additionalImage.src= "static/images/hand.png";
    }
    else if(challengeName == "light")
    {
        newPeriodicChallenge.innerHTML = "Use o sensor de luz para ficar entre " +params[0]+ " e "+ params[1] + " por " +params[2]+"s!";
        challengeImage.src= "static/images/lightSensor.png";
        additionalImage.src= "static/images/hand.png";
    }
    else if(challengeName == "countdown")
    {
        newPeriodicChallenge.innerHTML = "Pressione o botão na tela a cada" + params[0]+ "s por " + params[1] +"s";
        challengeImage.src= "static/images/tft.png";

    }
    newPeriodicChallenge.style.fontSize="20px";
    challengeImage.height = imageHeight;
    challengeImage.width = imageWidth;
    additionalImage.height = imageHeight;
    additionalImage.width = imageWidth;
    newPeriodicChallenge.appendChild(challengeImage);
    if(additionalImage.src !="")
        newPeriodicChallenge.appendChild(additionalImage);
    newPeriodicChallenge.id=challengeName;
    numberPeriodicChallenge = numberPeriodicChallenge + 1;
    document.getElementById("periodicChallenges").appendChild(newPeriodicChallenge);
}

function startTimer(minutes,seconds)
{
    var endCountdown = new Date();
    endCountdown.setTime(endCountdown.getTime() + (minutes * 60 * 1000));
    endCountdown.setSeconds(endCountdown.getSeconds() + seconds + 1);
    timer = setInterval
    (
        function() 
        {
            var startCountdown = new Date().getTime();
            var elapsedTime = endCountdown - startCountdown;
    
            // Conversoes
            var minutes = Math.floor((elapsedTime % (1000 * 60 * 60)) / (1000 * 60));
            var seconds = Math.floor((elapsedTime % (1000 * 60)) / 1000);
            document.getElementById("clock").innerHTML = ("0"+minutes).slice(-2) + ":" + ("0"+seconds).slice(-2);
    
            // Contagem chegou a zero
            if (elapsedTime < 0) 
            {
                document.getElementById("clock").innerHTML = "00:00"
               //gameOver(false);
            }
        }
    , 1000);
}




function correctFixedChallenge(challengeName,isCorrect)
{    
    var challenge = document.getElementById(challengeName);
    if(!isCorrect)
    {
        challenge.style.color="red";
    }
    else
    {	
        challenge.style.color="green";
        challengeCleared(challengeName)
    }
}



function correctPeriodicChallenge(numChallenge,isCorrect)
{
    var periodicChallenge = document.getElementById("periodicChallengeId"+ String(numChallenge));
	if(isCorrect)
		periodicChallenge.style.color="red";
	else if(!isCorrect)
        periodicChallenge.style.color="green";
    challengeCleared("periodicChallengeId",String(numChallenge));
    
}

function loseLife()
{
    numberLifes = numberLifes -1;
    if(numberLifes == 2 )
        document.getElementById("hearts").innerHTML=" ♥ ♥ ";
    else if(numberLifes ==1)
        document.getElementById("hearts").innerHTML=" ♥ ";
    //else
    //{
    //    gameOver(false);
    //}

}

function gameOver(hasWon)
{
    clearInterval(timer);
    var endMessage = document.getElementById("hearts");
    if(!hasWon)
    {
        endMessage.style.fontFamily="Game";
        endMessage.innerHTML= "Você perdeu! Aperte o botão para jogar outra vez"
        endMessage.style.color="red";
		//endMessage.onclick = restartlevel;
		//endMessage.style.cursor = "pointer";
		//endMessage.onmoueover = changeColor(endMessage,'darkred');
		//endMessage.onmouseout = changeColor(endMessage,'red');
	}
    else if(hasWon)
    {
        endMessage.innerHTML= "Você ganhou! Aperte o botão para jogar outra vez"
        endMessage.style.color="green";
		// setTimeout(
		// 	function ()
		// 	{
		// 		restartlevel();
		// 	},3000);
    }
}

function challengeCleared(challengeName)
{
    setTimeout(
        function ()
        {
            var clearedChallenge=document.getElementById(challengeName);
            clearedChallenge.parentNode.removeChild(clearedChallenge);
        },3000);
}


function changeColor(elem,color)
{
	endMessage.style.color=color;
}

function restartlevel()
{
	const fixedChallenges = document.getElementById("fixedChallenges");
	while (fixedChallenges.firstChild) 
	{
		fixedChallenges.firstChild.remove();
	}
	const periodicChallenges = document.getElementById("periodicChallenges");
	while (periodicChallenges.firstChild) 
	{
		periodicChallenges.firstChild.remove();
	}
	numberFixedChallenge = 0;
	numberPeriodicChallenge = 0;
	startTimer(2,00);
}


//window.onload=startTimer();
