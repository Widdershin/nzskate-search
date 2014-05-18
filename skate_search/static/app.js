$(document).ready(function() {
    $("#submit").click(function( event ) {
        event.preventDefault();
        var results;
        var searchData = {"query": $("#search").val()};

        $.getJSON("/search", searchData, function(data) {
            $results = $("#results")

            $.each(data, function(index, listing) {
                console.log(listing)
                $results.append('<li><a href="' + listing.url + '">' + listing.name + " - $" + listing.price + "</a></li>")
            });

            // $("#results").html(data)
        });
    });
});