$(document).ready(function() {
    $("#submit").click(function( event ) {
        event.preventDefault();
        var results;
        var searchData = {"query": $("#search").val()};

        results = $.get("/search", searchData, function(data) {
            $("#results").html(data)    
        });
    });
});