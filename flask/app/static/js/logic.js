$(document).ready(function() {
    console.log("Page Loaded");

    $("#filter").click(function() {
        alert("button clicked!");
        makePredictions();
    });
});


// call Flask API endpoint
function makePredictions() {
    var list_length = $("#list_length").val();
    var title = $("#title").val();
    // var overview = $("#overview").val();


    // Check if inputs are valid.

    // Create the payload.
    var payload = {
        "list_length": list_length,
        "movie": {
            "name": title,
            // "feature": overview
        }
    }

    // Perform a POST request to the query URL
    $.ajax({
        type: "POST",
        url: "/makePredictions",
        contentType: 'application/json;charset=UTF-8',
        data: JSON.stringify({ "data": payload }),
        success: function(returnedData) {
            // Return as a recommendation list table.
            console.log(returnedData);

            // Make table.
            var $table = $('<table>');

            // Make table head.
            $table.append('<caption></caption>')
            .append('<thead>').children('thead')
            .append('<tr />').children('tr').append('<th>Title</th><th>Rating</th>');

            // Make table body.
            var $tbody = $table.append('<tbody/>').children('tbody');

            results = returnedData['results']
            for (var i = 0; i < results.length; i++) {
                $tbody.append('<tr/>').children('tr:last')
                .append(`<td>${results[i]['title']}</td>`)
                .append(`<td>${results[i]['rating']}</td>`)
            }

            // Add table to document.
            $table.appendTo('#target');

        },
        error: function(XMLHttpRequest, textStatus, errorThrown) {
            alert("Status: " + textStatus);
            alert("Error: " + errorThrown);
        }
    });

}