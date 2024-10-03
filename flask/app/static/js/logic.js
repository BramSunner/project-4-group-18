$(document).ready(function() {
    console.log("Page Loaded");

    $("#filter").click(function() {
        // alert("button clicked!");
        makePredictions();
    });
});


// call Flask API endpoint
function makePredictions() {
    var list_length = $("#list_length").val();
    var title = $("#title").val();
    var overview = $("#overview").val();


    // Check if inputs are valid.
    if (title == '') {
        title = 'Forrest Gump';
    }

    // Create the payload.
    var payload = {
        "list_length": list_length,
        "movie": {
            "title": title,
            "feature": overview
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
            results = returnedData['results']

            // Do it a different route.
            var table = $('<table class="col-md-10 text-white" style="padding: 20px; margin: 10px;"></table>');
            var thead = $("<thead></thead>");
            var headerRow = $("<tr></tr>");
            headerRow.append(`<th>No.</th>`);
            headerRow.append(`<th>Title</th>`);
            headerRow.append(`<th>Rating</th>`);
            thead.append(headerRow);
            table.append(thead);

            var tbody = $("<tbody></tbody>");

            for (var i = 0; i < results.length; i++) {
                var row = $("<tr></tr>");
                if (i == 0) {
                    row.addClass("bg-warning")
                    .append(`<td>${"Target"}</td>`)
                    .append(`<td>${results[i]['title']}</td>`)
                    .append(`<td>${results[i]['rating']}</td>`);
                } else if (i % 2 == 0) {
                    row.addClass("bg-dark")
                    .append(`<td>${"Target"}</td>`)
                    .append(`<td>${results[i]['title']}</td>`)
                    .append(`<td>${results[i]['rating']}</td>`);
                } else {
                    row.addClass("bg-primary")
                    .append(`<td>${"Target"}</td>`)
                    .append(`<td>${results[i]['title']}</td>`)
                    .append(`<td>${results[i]['rating']}</td>`);
                }

                tbody.append(row);
            }

            table.append(tbody);



            // // Make table.
            // var $table = $('<table class="col-md-12 bg-primary text-white">');

            // // Make table head.
            // $table.append('<thead>').children('thead')
            // .append('<tr/>')
            // .children('tr')
            // .append('<th>No.</th>')
            // .append('<th>Title</th>')
            // .append('<th>Rating</th>');

            // // Make table body.
            // var $tbody = $table.append('<tbody/>').children('tbody');

            // results = returnedData['results']
            // for (var i = 0; i < results.length; i++) {
            //     if (i == 0) {
            //         $tbody.append('<tr/>').addClass('bg-warning').children('tr:last')
            //         .append(`<td>${"Target"}</td>`)
            //         .append(`<td>${results[i]['title']}</td>`)
            //         .append(`<td>${results[i]['rating']}</td>`);
            //     } else {
            //         $tbody.append('<tr/>').addClass('bg-dark').children('tr:last')
            //         .append(`<td>${i}</td>`)
            //         .append(`<td>${results[i]['title']}</td>`)
            //         .append(`<td>${results[i]['rating']}</td>`);
            //     }

            //     tbody.append(row);
            // }

            // table.append(tbody);

            // Delete old contents and add table to document.
            $("#target").empty().append(table);
        },
        error: function(XMLHttpRequest, textStatus, errorThrown) {
            alert("Status: " + textStatus);
            alert("Error: " + errorThrown);
        }
    });

}