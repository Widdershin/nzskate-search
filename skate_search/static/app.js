$(document).ready(function() {
    $("#submit").click(function( event ) {
        event.preventDefault();
        var results;
        var searchData = {"query": $("#search").val()};

        $.getJSON("/search", searchData, function(data) {
            $results = $("#results")
            $results.html("")
            $results.append('<tr><th>Shop</th><th>Item</th><th>Price</th></tr>');
            
            $.each(data, function(index, listing) {
                // console.log(listing);
                $results.append('<tr><td>'+listing.shop_name+'</td><td><a href="' + listing.url + '">' + listing.name + "</a></td><td>$" + listing.price + "</td></tr>");
            });

            // $("#results").html(data)
        });
    });
});