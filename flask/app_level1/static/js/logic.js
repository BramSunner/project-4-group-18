$(document).ready(function() {
    console.log("Page Loaded");

    $("#filter").click(function() {
        // alert("button clicked!");
        makePredictions();
    });
});

// call Flask API endpoint
function makePredictions() {
    var movie_name = $("#movie_name").val();


  // create the payload
  var payload = {
    "movie": movie_name,

}

    // Perform a POST request to the query URL
    $.ajax({
        type: "POST",
        url: "/makePredictions",
        contentType: 'application/json;charset=UTF-8',
        data: JSON.stringify({ "data": payload }),
        success: function(returnedData) {
            // print it
            console.log(returnedData);

            // if (returnedData["prediction"] == 1) {
            //     $("#output").text("You Survived!");
            // } else {
            //     $("#output").text("You did not survive, sorry. :(");
            // }
        },
        error: function(XMLHttpRequest, textStatus, errorThrown) {
            alert("Status: " + textStatus);
            alert("Error: " + errorThrown);
        }
    });

}
