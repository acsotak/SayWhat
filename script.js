const textForm = document.getElementById("textForm");
const promptStart = document.getElementById("promptStart");

textForm.addEventListener("submit", function(event) {
    event.preventDefault();

    const userInput = promptStart.value.trim();

    if (userInput === "") {
        return;
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
        }, 350);
        
    }, 3000);

    exitResponse.addEventListener("click", function() {
        document.body.classList.remove("response-active");
        document.body.classList.remove("results-active");
    });
});