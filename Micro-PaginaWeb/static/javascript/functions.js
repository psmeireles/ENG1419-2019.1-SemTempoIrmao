
var numberLifes = 3;
var timer;
var imageHeight = 60;
var imageWidth = 60;


function restartChallenges()
{
    sound = document.getElementById("start");
    sound.autoplay = true;
    promise = sound.play();
    if (promise !== undefined) {
        promise.then(_ => {
            // Autoplay started!
        }).catch(error => {
            console.log("Audio not started")
            // Autoplay was prevented.
        });
    }
    var lifesMessage = document.getElementById("hearts");
    numberLifes= 3;
    lifesMessage.innerHTML = "♥ ♥ ♥ ";
    lifesMessage.style.color = "red";    
}

function clearChallenges(){
    var fixedChallenges = document.getElementById("fixedChallenges");
	while (fixedChallenges.firstChild) 
	{
		fixedChallenges.firstChild.remove();
	}
	var periodicChallenges = document.getElementById("periodicChallenges");
	while (periodicChallenges.firstChild) 
	{
		periodicChallenges.firstChild.remove();
	}
}

function createNewFixedChallenge(challengeName,wireList)
{


    var newFixedChallenge = document.createElement("h4");
    newFixedChallenge.style.marginLeft="20px";

    if(challengeName == "wires")
    {
        wireList=wireList.map(function(wire)
        {
            if(wire=="1")
            return "green" //fio 1
            else if(wire=="2")
                return "yellow" //fio 2
            else if(wire=="3")
            return "blue" //fio 3
        })

        randomSquare1=document.createElement("div");
        randomSquare1.classList.add("square");
        randomSquare1.style.backgroundColor = wireList[0]

        randomSquare2=document.createElement("div");
        randomSquare2.classList.add("square");
        randomSquare2.style.backgroundColor = wireList[1]

        randomSquare3=document.createElement("div");
        randomSquare3.classList.add("square");
        randomSquare3.style.backgroundColor = wireList[2]

        fixedSquare1=document.createElement("div");
        fixedSquare1.classList.add("square");
        fixedSquare1.style.backgroundColor = "grey"

        fixedSquare2=document.createElement("div");
        fixedSquare2.classList.add("square");
        fixedSquare2.style.backgroundColor = "red"

        fixedSquare3=document.createElement("div");
        fixedSquare3.classList.add("square");
        fixedSquare3.style.backgroundColor = "orange"


        newFixedChallenge.innerHTML = "Coloque os fios na ordem abaixo e aperte o botão para confirmar   ";
        newFixedChallenge.appendChild(document.createElement("br"));
        newFixedChallenge.appendChild(randomSquare1);
        newFixedChallenge.appendChild(fixedSquare1);
        newFixedChallenge.appendChild(document.createElement("br"));

        newFixedChallenge.appendChild(randomSquare2);
        newFixedChallenge.appendChild(fixedSquare2);
        newFixedChallenge.appendChild(document.createElement("br"));

        newFixedChallenge.appendChild(randomSquare3);
        newFixedChallenge.appendChild(fixedSquare3);


    }
    else if(challengeName == "genius")
    {
        var challengeImage = document.createElement("img");
        var additionalImage = document.createElement("img");
        newFixedChallenge.innerHTML = "Observe os LEDs e aperte os botões correspondentes    ";
        challengeImage.src= "static/images/led.png";
        additionalImage.src= "static/images/button.png";
        challengeImage.height = imageHeight;
        challengeImage.width = imageWidth;
        additionalImage.height = imageHeight;
        additionalImage.width = imageWidth;
        newFixedChallenge.appendChild(challengeImage);
        newFixedChallenge.appendChild(additionalImage);

    }

    newFixedChallenge.style.fontSize="30px";
    newFixedChallenge.style.fontFamily="Roboto";

    newFixedChallenge.id=challengeName;
    document.getElementById("fixedChallenges").appendChild(newFixedChallenge);
}

function createNewPeriodicChallenge(challengeName,params)
{ 

    var newPeriodicChallenge = document.createElement("h4");
    newPeriodicChallenge.style.marginRight="80px";
    var challengeImage = document.createElement("img");
    var additionalImage = document.createElement("img");
    var hasAdditionalImage = false;
    if(challengeName == "distance")
    {
        newPeriodicChallenge.innerHTML = "Mantenha a distância entre " + params[0]+ " e " + params[1]+ " por " +params[2] +" segundos   ";
        challengeImage.src= "static/images/distance.png";
        additionalImage.src= "static/images/hand.png";
        hasAdditionalImage = true;
    }
    else if(challengeName == "light")
    {
        newPeriodicChallenge.innerHTML = `Mantenha a luz entre ${params[0]} e ${params[1]} por ${params[2]} segundos      `;
        challengeImage.src= "static/images/lightSensor.png";
        additionalImage.src= "static/images/hand.png";
        hasAdditionalImage = true;

    }
    else if(challengeName == "countdown")
    {
        newPeriodicChallenge.innerHTML = "Pressione o botão a cada " + params[0]+ " segundos por " + params[1] +" segundos      ";
        challengeImage.src= "static/images/tft.png";
       
    }
    newPeriodicChallenge.style.fontFamily="Roboto"
    newPeriodicChallenge.style.fontSize="30px";
    challengeImage.height = imageHeight;
    challengeImage.width = imageWidth;
    additionalImage.height = imageHeight;
    additionalImage.width = imageWidth;
    newPeriodicChallenge.appendChild(challengeImage);
    if(hasAdditionalImage)
        newPeriodicChallenge.appendChild(additionalImage);
    
    newPeriodicChallenge.id=challengeName;
    document.getElementById("periodicChallenges").appendChild(newPeriodicChallenge);
}

function startTimer(minutes,seconds)
{
    restartChallenges();
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
                clearInterval(timer);
            }
        }
    , 1000);
}




function correctFixedChallenge(challengeName,isCorrect)
{    
    var challenge = document.getElementById(challengeName);
    console.log(isCorrect)
    if(isCorrect)
    {
        challenge.style.color="green";
        challengeCleared(challengeName)
    }
    else
    {	
        challenge.style.color="red";
       
    }
}



function correctPeriodicChallenge(challengeName,isCorrect)
{
    var periodicChallenge = document.getElementById(challengeName);
	if(isCorrect)
		periodicChallenge.style.color="green";
	else
        periodicChallenge.style.color="red";
    challengeCleared(challengeName);
    
}

function loseLife()
{
    numberLifes = numberLifes -1;
    if(numberLifes == 2 )
        document.getElementById("hearts").innerHTML=" ♥ ♥ ";
    else if(numberLifes ==1)
        document.getElementById("hearts").innerHTML=" ♥ ";

}

function gameOver(hasWon)
{
    clearInterval(timer);   
    var sound;
    var promise;
    var endMessage = document.getElementById("hearts");
    endMessage.style.fontFamily="Game";
    if(!hasWon)
    {
        sound = document.getElementById("defeat"); 
        endMessage.innerHTML= "Você perdeu! Aperte o botão para jogar outra vez";
        endMessage.style.color="red";
	}
    else if(hasWon)
    {
        sound = document.getElementById("victory"); 
        endMessage.style.color="green";
        endMessage.innerHTML= "Você ganhou! Aperte o botão para jogar outra vez";

    }
    sound.autoplay = true;
    promise = sound.play();
    if (promise !== undefined) {
        promise.then(_ => {
            // Autoplay started!
        }).catch(error => {
            console.log("Audio not started")
            // Autoplay was prevented.
        });
    }
    clearChallenges()
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

function changeButtonColor(state,elementId)
{
    var button = document.getElementById(elementId);
    if(state == true)
        button.style.color="green";
    else
        button.style.color="white";

}
