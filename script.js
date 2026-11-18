const textForm = document.getElementById("textForm");
const promptStart = document.getElementById("promptStart");
const saveButton = document.getElementById("saveButton");
const inputHeading = document.getElementById("inputHeading");
const exitButton = document.getElementById("exitButton");
const recognized = true;

textForm.addEventListener("submit", function(event) {
    event.preventDefault();

    const userInput = promptStart.value.trim();

    if (userInput === "") {
        return;
    }

    if (recognized) {
        document.body.classList.remove("unrecognized");
        saveButton.textContent = "♡ Save this phrase";

        document.getElementById("resultDefinition").textContent = 
        `A Southern American idiom that has two meanings depending on context:

        An offer of sympathy for someone facing a difficult time, or a backhanded
        compliment used to imply someone is acting naive.`;

        document.getElementById("toneTags").innerHTML =
        "<span>Affectionate</span>" +
        "<span>Condescending</span>";

        document.getElementById("exampleText").textContent =
        `Positive: "You lost your job? Bless your heart."
        Negative: "Oh, you tried fixing the printer with the paper still jammed inside? Bless your heart."`;
    }

    else {
        document.body.classList.add("unrecognized");
        saveButton.textContent = "+ Suggest this phrase";
    }

    inputHeading.textContent = userInput;

    document.body.classList.add("response-active");

    setTimeout(function() {
        document.body.classList.add("loading-finish");

        setTimeout(function() {
            const responseLabel = document.getElementById("responseLabel");
            
            responseLabel.style.opacity = "0";
            responseLabel.textContent = "RESULTS READY";
            responseLabel.classList.add("label-pop");

            document.body.classList.add("results-active");
        }, 800);
        
    }, 3000);
});

exitButton.addEventListener("click", function() {
        document.body.classList.remove("response-active");
        document.body.classList.remove("results-active");
        document.body.classList.remove("loading-finish");
        document.body.classList.remove("unrecognized");

        const responseLabel = document.getElementById("responseLabel");

        responseLabel.textContent = "INVESTIGATING";
        responseLabel.style.opacity = "1";
        responseLabel.classList.remove("label-pop");

        promptStart.value = "";
    });