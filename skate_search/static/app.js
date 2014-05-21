$(document).ready(function() {
    $("#submit").click(function( event ) {
        event.preventDefault();
        var results;
        var searchData = {"query": $("#search").val()};

        $.getJSON("/search", searchData, function(data) {
            $results = $("#results")
            $results.html("")
            $results.append('<thead id="resultsHeader"></thead>');

            $results.append('<tbody>');
            $.each(data, function(index, listing) {
                // console.log(listing);
                $results.append('<tr><td>'+listing.shop_name+'</td><td><a href="' + listing.url + '">' + listing.name + "</a></td><td>$" + listing.price + "</td><td>" + listing.relevance + "%</td></tr>");
            });
            $results.append('</tbody>');
            // $("#results").html(data)
        });
    });
});