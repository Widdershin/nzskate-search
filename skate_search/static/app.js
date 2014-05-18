$(document).ready(function() {
    $("#submit").click(function( event ) {
        event.preventDefault();
        alert("Clicked search");
        $("#results").append("<li>A result!</li>")
    });
});