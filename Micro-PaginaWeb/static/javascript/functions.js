var numberFixedChallenge = 0;
var numberPeriodicChallenge = 0;
var numberLifes = 3;
var timer;
var imageHeight = 60;
var imageWidth = 60;
var currentLevel = 1;

function createNewFixedChallenge(challengeName)
{
    var newFixedChallenge = document.createElement("h4");
    var challengeImage = document.createElement("img");
    var additionalImage = document.createElement("img");
    if(challengeName == "wires")
    {
        newFixedChallenge.innerHTML = "Coloque os fios na seguinte ordem e aperte o botão para confirmar: Vermelho-Azul, Branco-Marrom, Verde-Amarelo";
        challengeImage.src= "static/images/wires.png";
        additionalImage.src= "static/images/button.png";

    }
    else if(challengeName == "distance")
    {
        newFixedChallenge.innerHTML = "Mantenha sua mão entre 2 e 3 centímetros do sensor de distância";
        challengeImage.src= "static/images/distance.png";
        additionalImage.src= "static/images/hand.png";
    }
    else if(challengeName == "light")
    {
        newFixedChallenge.innerHTML = "Faça o nível de luz no sensor ficar entre 100 e 300";
        challengeImage.src= "static/images/lightSensor.png";
        additionalImage.src= "static/images/hand.png";
    }
    else if(challengeName == "genius")
    {
        newFixedChallenge.innerHTML = "Observe a sequência de LEDs e aperte os botões correspondentes";
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
    newFixedChallenge.id="fixedChallengeId"+ String(numberFixedChallenge);
    numberFixedChallenge = numberFixedChallenge + 1;
    document.getElementById("fixedChallenges").appendChild(newFixedChallenge);
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


function createNewPeriodicChallenge(challengeName)
{ 
    var newPeriodicChallenge = document.createElement("h4");
    var challengeImage = document.createElement("img");
    if(challengeName == "tft")
    {
        newPeriodicChallenge.innerHTML = "Pressione o botão na tela a cada 10 segundos por 30 segundos";
        challengeImage.src= "static/images/tft.png";

    }
    else if(challengeName == "distance")
    {
        newPeriodicChallenge.innerHTML = "Mantenha sua mão entre 2 e 3 centímetros do sensor de distância a cada 10 segundos";
        challengeImage.src= "static/images/distance.png";
    }
    else if(challengeName == "light")
    {
        newPeriodicChallenge.innerHTML = "Faça o nível de luz no sensor ficar entre 100 e 300 a cada 10 segundos por 30 segundos";
        challengeImage.src= "static/images/lightSensor.png";
    }
    newPeriodicChallenge.style.fontSize="20px";
    challengeImage.height = imageHeight;
    challengeImage.width = imageWidth;
    newPeriodicChallenge.appendChild(challengeImage);
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
        challengeCleared("fixedChallengeId",String(numberFixedChallenge-1))
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
    var endMessage = document.getElementById("textLifes");
    if(!hasWon)
    {
        endMessage.innerHTML= "Você perdeu! Clique aqui para tentar novamente."
        endMessage.style.color="red";
		endMessage.onclick = restartlevel();
		
    }
    else if(hasWon)
    {
        endMessage.innerHTML= "Você ganhou! Próximo nível começa em 3 segundos"
        endMessage.style.color="green";
		setTimeout(
			function ()
			{
				restartlevel();
			},3000);
    }
}

function challengeCleared(challengeType,challengeNumber)
{
    setTimeout(
        function ()
        {
            var clearedChallenge=document.getElementById(challengeType+challengeNumber);
            clearedChallenge.parentNode.removeChild(clearedChallenge);
        },3000);
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
	startTimer(1,30);
}


//window.onload=startTimer();
