$( document ).ready(function() {

    $('#autocomplete').autocomplete({
        serviceUrl: "/games",
        onSelect: function (suggestion) {
            console.log(suggestion);
            window.location.replace(suggestion.url);
        }
    });
});