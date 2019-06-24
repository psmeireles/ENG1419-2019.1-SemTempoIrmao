var numberFixedChallenge = 0;
var numberPeriodicChallenge = 0;
var numberLifes = 3;
var timer;

function createNewFixedChallenge(challengeName)
{
    var newFixedChallenge = document.createElement("h4");
    newFixedChallenge.innerHTML = challengeName;
    newFixedChallenge.id="fixedChallengeId"+ String(numberFixedChallenge);
    numberFixedChallenge = numberFixedChallenge + 1;
    document.getElementById("fixedChallenges").appendChild(newFixedChallenge);
}


function startTimer()
{
    var endCountdown = new Date();
    endCountdown.setTime(endCountdown.getTime() + (2 * 60 * 1000));
    endCountdown.setSeconds(endCountdown.getSeconds() + 1);
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
                gameOver(false);
            }
        }
    , 1000);
}


function createNewPeriodicChallenge(challengeName)
{ 
    var newPeriodicChallenge = document.createElement("h4");
    newPeriodicChallenge.innerHTML = challengeName
    newPeriodicChallenge.id="periodicChallengeId"+ String(numberPeriodicChallenge);
    numberPeriodicChallenge = numberPeriodicChallenge + 1;
    document.getElementById("periodicChallenges").appendChild(newPeriodicChallenge);
}

function correctFixedChallenge(isCorrect)
{    
    var challenge = document.getElementById("fixedChallengeId" + String(numberFixedChallenge-1));
    if(!isCorrect)
    {
        challenge.style.color="red";
    }
    else
    {	
        challenge.style.color="green";
        if(numberFixedChallenge == 6)
        {
            gameOver(true)
            return;
        }
    }
}



function correctPeriodicChallenge(numChallenge,isCorrect)
{
	console.log(numChallenge);
	console.log(isCorrect);
    var periodicChallenge = document.getElementById("periodicChallengeId"+ String(numChallenge));
	if(isCorrect)
		periodicChallenge.style.color="red";
	else if(!isCorrect)
		periodicChallenge.style.color="green";
}

function loseLife()
{
    numberLifes = numberLifes -1;
    if(numberLifes == 2 )
        document.getElementById("hearts").innerHTML=" ♥ ♥ ";
    else if(numberLifes ==1)
        document.getElementById("hearts").innerHTML=" ♥ ";
    else
    {
        gameOver(false);
    }
}

function gameOver(hasWon)
{
    clearInterval(timer);
    var endMessage = document.getElementById("textLifes");
    if(!hasWon)
    {
        endMessage.innerHTML= "Você perdeu!"
        endMessage.style.color="red";
    }
    else if(hasWon)
    {
        endMessage.innerHTML= "Você ganhou!"
        endMessage.style.color="green";
    }
}

//window.onload=startTimer();



