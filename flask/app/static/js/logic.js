$(document).ready(function() {
    console.log("Page Loaded");

    $("#filter").click(function() {
        // alert("button clicked!");
        makePredictions();
    });
});


// call Flask API endpoint
function makePredictions() {
    var title = $("#title").val();
    // var overview = $("#overview").val();


    // check if inputs are valid

    // create the payload
    var payload = {
        "title": title,
        // "overview": overview,
    }

    // Perform a POST request to the query URL
    $.ajax({
        type: "POST",
        url: "/makePredictions",
        contentType: 'application/json;charset=UTF-8',
        data: JSON.stringify({ "data": payload }),
        success: function(returnedData) {
            // Return as a recommendation list table.
            // console.log(returnedData);
            // var prob = parseFloat(returnedData["prediction"]);

            // if (prob > 0.5) {
            //     $("#output").text(`You Survived with probability ${prob}!`);
            // } else {
            //     $("#output").text(`You did not survive with probability ${prob}, sorry. :(`);
            // }

        },
        error: function(XMLHttpRequest, textStatus, errorThrown) {
            alert("Status: " + textStatus);
            alert("Error: " + errorThrown);
        }
    });

}